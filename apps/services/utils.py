import os.path
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, DefaultDict, Dict, List, Set, Tuple, Union

from sqlalchemy.engine.row import Row
import xlrd
from fastapi import UploadFile
from fastapi import status as http_status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.exceptions import BackendException
from apps.users.services import student_list_service


def create_faculty_dict(specialties: List) -> DefaultDict[str, Dict[str, int]]:
    faculty_dict = defaultdict(dict)
    for specialty in specialties:
        faculty_dict[specialty.shortname]["faculty_id"] = specialty.faculty_id
        faculty_dict[specialty.shortname][specialty.name_1] = specialty.speciality_id
    return faculty_dict


def create_speciality_dict(specialties: List) -> Dict[int, str]:
    speciality_dict = {}
    for specialty in specialties:
        speciality_dict[specialty.speciality_id] = specialty.name_1
    return speciality_dict


def create_faculty_list(faculties: List) -> List:
    faculty_list = []
    for faculty in faculties:
        faculty_list.append(faculty.name)
    return faculty_list


async def create_telephone_set(
    session: AsyncSession, filters: Dict[str, int]
) -> Set[str]:
    students = await student_list_service.list(session=session, filters=filters)
    return {student.telephone_number for student in students}


def get_worksheet_cell_col_row(
    file: UploadFile,
) -> Tuple[xlrd.sheet.Sheet, Callable, int, int]:
    workbook = xlrd.open_workbook(file_contents=file.file.read())
    worksheet = workbook.sheet_by_name("список студентів")
    row, col = 0, 0
    for i, elem in enumerate(worksheet.col(1)):
        if elem.value:
            row = i + 1
            break
        if i > 100:
            raise BackendException(
                message=(
                    "Empty second column. Please, check the correctness of the file"
                    " content."
                ),
                code=http_status.HTTP_406_NOT_ACCEPTABLE,
            )
    for j, elem in enumerate(worksheet.row(row - 1)):
        if elem.value == "Прізвище":
            col = j
            break
        if j > 100:
            raise BackendException(
                message=(
                    "Can't find cell with content 'Прізвище'. Please, check the"
                    " correctness of the file content."
                ),
                code=http_status.HTTP_406_NOT_ACCEPTABLE,
            )
    return worksheet, worksheet.cell_value, col, row


def check_faculty_existence(
    cell: Callable, col: int, i: int, faculty_dict: DefaultDict[str, Dict[str, int]]
) -> None:
    if cell(i, col + 7) not in faculty_dict:
        raise BackendException(
            message=f"Row {i + 1}. There is no such faculty name.",
            code=http_status.HTTP_406_NOT_ACCEPTABLE,
        )


def check_specialty_existence(
    cell: Callable, col: int, i: int, specialties_dict: Dict[str, int]
) -> None:
    if cell(i, col + 6) not in specialties_dict:
        raise BackendException(
            message=(
                f"Row {i + 1}. There is no such speciality in"
                f" {cell(i, col + 7)} faculty"
            ),
            code=http_status.HTTP_406_NOT_ACCEPTABLE,
        )


def check_telephone_number_existence(
    cell: Callable, col: int, i: int, telephone_set: Set[str]
) -> None:
    tel = cell(i, col + 3)
    if not tel:
        raise BackendException(
            message=f"Cell {i + 1} of column 'Phone number' is empty",
            code=http_status.HTTP_406_NOT_ACCEPTABLE,
        )
    if not tel.isdigit() or len(tel) != 12:
        raise BackendException(
            message=f"Cell {i + 1} of column 'Phone number' is not valid"
        )
    if cell(i, col + 3) in telephone_set:
        raise BackendException(
            message=(
                f"Row {i + 1}. The student with telephone number {cell(i, col + 3)} is"
                " already exist"
            ),
            code=http_status.HTTP_409_CONFLICT,
        )


def check_for_empty_value(value: Any, value_name: str = "") -> None:
    if not value:
        raise BackendException(
            message=f"Input {value_name} is incorrect",
            code=http_status.HTTP_404_NOT_FOUND,
        )


def check_file_existing(path: str) -> None:
    if not os.path.exists(path):
        raise BackendException(
            message=f"File with path {path} was removed or deleted",
            code=http_status.HTTP_409_CONFLICT,
        )


def update_user_booking_hostel_data_by_user_request(
    user_request_data: dataclass, user_booking_hostel_data: Row
) -> Dict[str, Union[int, str]]:

    updated_user_booking_hostel_data = dict(user_booking_hostel_data)

    updated_user_booking_hostel_data.update(user_request_data.dict())
    updated_user_booking_hostel_data.update(
        full_name={
            "last_name": user_request_data.dict()["student_last_name"],
            "first_name": user_request_data.dict()["student_first_name"],
            "middle_name": user_request_data.dict()["student_middle_name"],
        },
        rector_full_name={
            "last_name": user_request_data.dict()["rector_last_name"],
            "first_name": user_request_data.dict()["rector_first_name"],
            "middle_name": user_request_data.dict()["rector_middle_name"],
        },
    )
    return updated_user_booking_hostel_data
