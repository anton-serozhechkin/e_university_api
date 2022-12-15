from apps.common.exceptions import BackendException
from apps.users.services import student_list_service

from collections import defaultdict
from fastapi import UploadFile, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Callable, DefaultDict, Dict, List, Set, Tuple
import xlrd


def create_faculty_dict(specialties: List) -> DefaultDict[str, Dict[str, int]]:
    faculty_dict = defaultdict(dict)
    for specialty in specialties:
        faculty_dict[specialty.shortname]["faculty_id"] = specialty.faculty_id
        faculty_dict[specialty.shortname][specialty.name_1] = specialty.speciality_id
    return faculty_dict


async def create_telephone_set(session: AsyncSession, filters: Dict[str, int]) -> Set[str]:
    students = await student_list_service.list(session=session, filters=filters)
    return {student.telephone_number for student in students}


def get_worksheet_cell_col_row(file: UploadFile) -> Tuple[xlrd.sheet.Sheet, Callable, int, int]:
    workbook = xlrd.open_workbook(file_contents=file.file.read())
    worksheet = workbook.sheet_by_name("список студентів")
    row, col = 0, 0
    for i, elem in enumerate(worksheet.col(1)):
        if elem.value:
            row = i + 1
            break
        if i > 100:
            raise BackendException(
                message="Empty second column. Please, check the correctness of the file content.",
                code=http_status.HTTP_406_NOT_ACCEPTABLE
            )
    for j, elem in enumerate(worksheet.row(row - 1)):
        if elem.value == "Прізвище":
            col = j
            break
        if j > 100:
            raise BackendException(
                message="Can't find cell with content 'Прізвище'. Please, check the correctness of the file content.",
                code=http_status.HTTP_406_NOT_ACCEPTABLE
            )
    return worksheet, worksheet.cell_value, col, row


def check_faculty_existence(cell: Callable,
                            col: int,
                            i: int,
                            faculty_dict: DefaultDict[str, Dict[str, int]]) -> None:
    if cell(i, col + 7) not in faculty_dict:
        raise BackendException(
            message=f"Row {i + 1}. There is no such faculty name.",
            code=http_status.HTTP_406_NOT_ACCEPTABLE
        )


def check_specialty_existence(cell: Callable,
                              col: int,
                              i: int,
                              specialties_dict: Dict[str, int]) -> None:
    if cell(i, col + 6) not in specialties_dict:
        raise BackendException(
            message=f"Row {i + 1}. There is no such speciality in {cell(i, col + 7)} faculty",
            code=http_status.HTTP_406_NOT_ACCEPTABLE
        )


def check_telephone_number_existence(cell: Callable, col: int, i: int, telephone_set: Set[str]) -> None:
    tel = cell(i, col + 3)
    if not tel:
        raise BackendException(
            message=f"Cell {i + 1} of column 'Phone number' is empty",
            code=http_status.HTTP_406_NOT_ACCEPTABLE
        )
    if not tel.isdigit() or len(tel) != 12:
        raise BackendException(
            message=f"Cell {i + 1} of column 'Phone number' is not valid"
        )
    if cell(i, col + 3) in telephone_set:
        raise BackendException(
            message=f"Row {i + 1}. The student with telephone number {cell(i, col + 3)} is already exist",
            code=http_status.HTTP_409_CONFLICT


def check_for_empty_value(value: Any, value_name: str = '') -> None:
    if not value:
        raise BackendException(
            message=f'Input {value_name} is incorrect',
            code=http_status.HTTP_404_NOT_FOUND
        )
