from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Tuple, Union

from fastapi import File, Request, UploadFile
from pytz import utc
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.file_managers import file_manager
from apps.services.models import STATUS_MAPPING, UserDocument
from apps.services.schemas import (
    CancelRequestIn,
    CountHostelAccommodationCostIn,
    CountHostelAccommodationCostOut,
    CreateUserRequestOut,
    HostelAccomodationViewOut,
    UserDocumenstListOut,
    UserRequestBookingHostelOut,
    UserRequestDetailsViewOut,
    UserRequestExistenceOut,
    UserRequestHostelAccommodationWarrantViewOut,
    UserRequestReviewIn,
    UserRequestReviewOut,
    UserRequestsListOut,
    RequestForHostelAccommodationIn,
    RequestForHostelAccommodationOut,
)
from apps.services.services import (
    bed_place_service,
    get_specialties_list,
    hostel_accommodation_service,
    hostel_service,
    request_existence_service,
    service_service,
    user_document_service,
    user_documents_list_service,
    user_faculty_service,
    user_request_booking_hostel_service,
    user_request_detail_service,
    user_request_hostel_accommodation_warrant_view_service,
    user_request_list_service,
    user_request_review_service,
    user_request_service,
    get_faculty_list,
)
from apps.services.utils import (
    check_faculty_existence,
    check_file_existing,
    check_for_empty_value,
    check_specialty_existence,
    check_telephone_number_existence,
    check_user_request_status,
    create_faculty_dict,
    create_telephone_set,
    get_worksheet_cell_col_row,
    update_user_booking_hostel_data_by_user_request,
    create_faculty_list,
    create_speciality_dict,
)
from apps.users.schemas import CreateStudentIn, CreateStudentsListOut, UserOut
from apps.users.services import student_service
from settings import (
    HOSTEL_BOOKING_TEMPLATE,
    HOSTEL_WARRANT_TEMPLATE,
    SETTLEMENT_HOSTEL_PATH,
    TEMPLATES_PATH,
    WARRANT_HOSTEL_ACCOMMODATION_PATH,
    Settings,
)


class ServiceHandler:
    @classmethod
    async def validate_faculty_name(cls, faculty_name: str, university_id: int) -> bool:
        faculties = await get_faculty_list(university_id)
        if not faculty_name in create_faculty_list(faculties):
            raise ValueError(f"Wrong '{faculty_name}' name. This faculty doesn't exist")
        return True

    @classmethod
    async def validate_speciality_code(
        cls, speciality_code: int, university_id: int
    ) -> bool:
        specialities = await get_specialties_list(university_id)
        if not speciality_code in create_speciality_dict(specialities).keys():
            raise ValueError(
                f"Wrong '{speciality_code}' code. This speciality doesn't exist"
            )
        return True

    @classmethod
    async def validate_speciality_name(
        cls, speciality_name: str, university_id: int
    ) -> bool:
        specialities = await get_specialties_list(university_id)
        if not speciality_name in create_speciality_dict(specialities).values():
            raise ValueError(
                f"Wrong '{speciality_name}' speciality name. This speciality doesn't exist"
            )
        return True

    @classmethod
    async def validate_speciality_name_and_speciality_code_correspondence(
        cls, speciality_name: str, speciality_code: int, university_id: int
    ) -> bool:
        specialities = await get_specialties_list(university_id)
        if not (
            (speciality_code, speciality_name)
            in create_speciality_dict(specialities).items()
        ):
            raise ValueError(
                f"Speciality code '{speciality_code}' "
                f"doesn't correspondence with exists "
                f"'{speciality_name}' speciality name"
            )
        return True

    @classmethod
    async def check_speciality_and_faculty_validation_result(
        cls,
        faculty_name: str,
        speciality_name: str,
        speciality_code: int,
        university_id: int,
    ) -> bool:
        if (
            await cls.validate_faculty_name(faculty_name, university_id)
            and await cls.validate_speciality_name(speciality_name, university_id)
            and await cls.validate_speciality_code(speciality_code, university_id)
            and await cls.validate_speciality_name_and_speciality_code_correspondence(
                speciality_name,
                speciality_code,
                university_id,
            )
        ):
            return True
        else:
            return False

    @classmethod
    async def create_request_for_hostel_accommodation(
        cls,
        *,
        request: Request,
        university_id: int,
        user_request: RequestForHostelAccommodationIn,
        user: UserOut,
        session: AsyncSession,
    ) -> RequestForHostelAccommodationOut:

        if await cls.check_speciality_and_faculty_validation_result(
            user_request.faculty_name,
            user_request.speciality_name,
            user_request.speciality_code,
            university_id,
        ):
            user_faculty = await user_faculty_service.read(
                data={"user_id": user.user_id}, session=session
            )
            data = {
                "created_at": datetime.now(utc),
                "comment": user_request.comment,
                "user_id": user.user_id,
                "service_id": 1,
                "faculty_id": user_faculty.faculty_id,
                "university_id": university_id,
                "status_id": STATUS_MAPPING.get("Розглядається"),
            }
            user_request_booking_hostel = (
                await user_request_booking_hostel_service.read(
                    session=session,
                    data={"user_id": user.user_id, "university_id": university_id},
                )
            )
            user_request_service_response = await user_request_service.create(
                session=session, data=data
            )
            prepared_data = {
                "context": update_user_booking_hostel_data_by_user_request(
                    user_request, user_request_booking_hostel
                ),
                "service_id": user_request_service_response.service_id,
                "user_request_id": user_request_service_response.user_request_id,
            }
            await cls.__create_user_document(session, **prepared_data)
            return user_request_service_response

    @staticmethod
    async def read_user_documents_list(
        *,
        request: Request,
        university_id: int,
        user: UserOut,
        session: AsyncSession,
    ) -> Optional[List[UserDocumenstListOut]]:
        return await user_documents_list_service.list(
            session=session,
            filters={"university_id": university_id, "user_id": user.user_id},
        )

    @staticmethod
    async def read_user_request_existence(
        *,
        request: Request,
        university_id: int,
        service_id: int,
        user: UserOut,
        session: AsyncSession,
    ) -> UserRequestExistenceOut:
        user_request_result = await request_existence_service.read(
            session=session,
            data={
                "university_id": university_id,
                "service_id": service_id,
                "user_id": user.user_id,
            },
        )
        if user_request_result:
            return UserRequestExistenceOut(
                user_request_id=user_request_result.user_request_id,
                status=user_request_result.status,
                user_request_exist=True,
            )
        return UserRequestExistenceOut(
            user_request_id=None,
            status=None,
            user_request_exist=False,
        )

    @staticmethod
    async def read_user_request_list(
        *,
        request: Request,
        university_id: int,
        user: UserOut,
        session: AsyncSession,
    ) -> List[UserRequestsListOut]:
        return await user_request_list_service.list(
            session=session,
            filters={"university_id": university_id, "user_id": user.user_id},
        )

    @staticmethod
    async def read_user_request_booking_hostel(
        *,
        request: Request,
        university_id: int,
        user: UserOut,
        session: AsyncSession,
    ) -> UserRequestBookingHostelOut:
        return await user_request_booking_hostel_service.read(
            session=session,
            data={"user_id": user.user_id, "university_id": university_id},
        )

    @staticmethod
    async def cancel_request(
        *,
        request: Request,
        user_request_id: int,
        cancel_request: CancelRequestIn,
        session: AsyncSession,
    ) -> CreateUserRequestOut:
        CancelRequestIn(status_id=cancel_request.status_id)
        user_request = await user_request_service.update(
            session=session,
            data={"user_request_id": user_request_id},
            obj=cancel_request,
        )
        return user_request

    @staticmethod
    async def create_user_request_review(
        *,
        request: Request,
        university_id: int,
        user_request_id: int,
        user_request_review: UserRequestReviewIn,
        user: UserOut,
        session: AsyncSession,
    ) -> UserRequestReviewOut:
        created_user_request_review = await user_request_review_service.create(
            session=session,
            data={
                "university_id": university_id,
                "user_request_id": user_request_id,
                "created_at": datetime.now(utc),
                "reviewer": user.user_id,
                "hostel_id": user_request_review.hostel_id,
                "room_number": user_request_review.room_number,
                "start_accommodation_date": user_request_review.start_accommodation_date,
                "end_accommodation_date": user_request_review.end_accommodation_date,
                "total_sum": user_request_review.total_sum,
                "payment_deadline_date": user_request_review.payment_deadline_date,
                "remark": user_request_review.remark,
                "bed_place_id": user_request_review.bed_place_id,
            },
        )
        await user_request_service.update(
            session=session,
            data={"user_request_id": user_request_id},
            obj={"status_id": user_request_review.status_id},
        )
        return created_user_request_review

    @staticmethod
    async def read_hostel_accommodation(
        *,
        request: Request,
        university_id: int,
        user_request_id: int,
        session: AsyncSession,
    ) -> Optional[HostelAccomodationViewOut]:
        response = await hostel_accommodation_service.read(
            session=session,
            data={"university_id": university_id, "user_request_id": user_request_id},
        )
        # TODO AttributeError: 'NoneType' object has no attribute 'documents'
        # (it's happened only if user request doesn't have review)
        return response

    @staticmethod
    async def read_request_details(
        *,
        request: Request,
        university_id: int,
        user_request_id: int,
        session: AsyncSession,
    ) -> UserRequestDetailsViewOut:
        return await user_request_detail_service.read(
            session=session,
            data={"university_id": university_id, "user_request_id": user_request_id},
        )

    @staticmethod
    async def read_user_document(
        *,
        request: Request,
        university_id: int,
        user_document_id: int,
        user: UserOut,
        session: AsyncSession,
    ) -> str:
        user_document = await user_document_service.read(
            session=session, data={"user_document_id": user_document_id}
        )
        return file_manager.get(user_document.content)

    async def download_user_document(
        self,
        *,
        request: Request,
        university_id: int,
        user_document_id: int,
        user: UserOut,
        session: AsyncSession,
    ) -> Tuple[str, str]:
        user_document = await user_document_service.read(
            session=session, data={"user_document_id": user_document_id}
        )
        check_for_empty_value(user_document, "user_document_id")
        check_file_existing(user_document.content)
        file_name = await self.__generate_user_document_name_for_download(
            user_document.name, user.user_id, session
        )
        return user_document.content, file_name

    async def count_hostel_accommodation_cost(
        self,
        *,
        request: Request,
        university_id: int,
        data: CountHostelAccommodationCostIn,
        session: AsyncSession,
    ) -> CountHostelAccommodationCostOut:
        hostel = await hostel_service.read(
            session=session, data={"hostel_id": data.hostel_id}
        )

        bed_place = await bed_place_service.read(
            session=session, data={"bed_place_id": data.bed_place_id}
        )

        months_count = self.calculate_difference_between_dates_in_months(
            data.end_accommodation_date, data.start_accommodation_date
        )
        month_price = self.get_month_price_by_bed_place(
            hostel.month_price, bed_place.bed_place_name
        )

        response = self.calculate_total_hostel_accommodation_cost(
            month_price, months_count
        )
        return CountHostelAccommodationCostOut(total_hostel_accommodation_cost=response)

    @classmethod
    def calculate_difference_between_dates_in_months(
        cls, end_date: date, start_date: date
    ) -> int:
        return (
            end_date.month - start_date.month + 12 * (end_date.year - start_date.year)
        ) + 1

    @classmethod
    def get_month_price_by_bed_place(
        cls, hostel_month_price: Decimal, bed_place_name: str
    ) -> Decimal:
        return Decimal(hostel_month_price) * Decimal(bed_place_name)

    @classmethod
    def calculate_total_hostel_accommodation_cost(
        cls, month_price: Decimal, month_difference: int
    ) -> Decimal:
        return month_price * month_difference

    @classmethod
    async def __create_user_document(
        cls, session: AsyncSession, **kwargs
    ) -> UserDocument:
        service_id = kwargs.get("service_id")
        name = await cls.__generate_user_document_name(service_id, session)
        created_at = datetime.strptime(
            datetime.now(utc).strftime(Settings.DATETIME_FORMAT),
            Settings.DATETIME_FORMAT,
        )
        kwargs["created_at"] = created_at
        content = await cls.__create_user_document_content_hostel_settlement_service(
            **kwargs
        )
        user_document_record = await user_document_service.create(
            session=session,
            data={
                "name": name,
                "content": content,
                "user_request_id": kwargs.get("user_request_id"),
            },
        )
        return user_document_record

    @classmethod
    async def __create_user_document_content_hostel_settlement_service(
        cls, **kwargs
    ) -> str:
        context = kwargs.get("context")
        rendered_template = file_manager.render(
            TEMPLATES_PATH, HOSTEL_BOOKING_TEMPLATE, context
        )
        file_date_created = (
            str(kwargs.get("created_at")).replace(":", "-").replace(" ", "_")
        )
        document_name = (
            f"hostel_settlement_{file_date_created}_"
            f"{kwargs.get('user_request_id')}.docx"
        )
        DOCUMENT_PATH = SETTLEMENT_HOSTEL_PATH / str(context.user_id)
        Path(DOCUMENT_PATH).mkdir(exist_ok=True)
        document_path = file_manager.create(
            document_path, document_name, rendered_template
        )
        return document_path

    @classmethod
    async def __generate_user_document_name(
        cls, service_id: int, session: AsyncSession
    ) -> str:
        service = await service_service.read(
            session=session, data={"service_id": service_id}
        )
        return f"Заява на {service.service_name.lower()}"

    @staticmethod
    async def create_students_list_from_file(
        *,
        request: Request,
        university_id: int,
        file: UploadFile = File(...),
        session: AsyncSession,
    ) -> Union[List[CreateStudentsListOut], None]:
        specialties, students = await get_specialties_list(university_id), []

        faculty_dict = create_faculty_dict(specialties)

        telephone_set = await create_telephone_set(
            session=session, filters={"university_id": university_id}
        )

        worksheet, cell, col, row = get_worksheet_cell_col_row(file)

        for i in range(row, len(worksheet.col(1))):
            check_faculty_existence(cell, col, i, faculty_dict)
            specialties_dict = faculty_dict.get(cell(i, col + 7))
            check_specialty_existence(cell, col, i, specialties_dict)
            check_telephone_number_existence(cell, col, i, telephone_set)
            student = CreateStudentIn(
                last_name=cell(i, col),
                first_name=cell(i, col + 1),
                middle_name=cell(i, col + 2),
                telephone_number=cell(i, col + 3),
                course_id=cell(i, col + 4),
                faculty_id=specialties_dict.get("faculty_id"),
                speciality_id=specialties_dict.get(cell(i, col + 6)),
                gender=cell(i, col + 8),
            )
            students.append(student)
        return await student_service.create_many(session=session, objs=students)

    @classmethod
    async def download_warrant_document(
        cls,
        *,
        request: Request,
        user_request_review_id: int,
        session: AsyncSession,
    ) -> Tuple[str, str]:
        warrant_view_data: UserRequestHostelAccommodationWarrantViewOut = (
            await user_request_hostel_accommodation_warrant_view_service.read(
                session=session, data={"user_request_review_id": user_request_review_id}
            )
        )
        check_user_request_status(warrant_view_data.status_id)
        warrant_file_path = await cls.__create_user_warrant_content(warrant_view_data)
        file_name = await cls.__generate_user_document_name_for_download(
            "Ордер на поселення в гуртожиток", warrant_view_data.user_id, session
        )
        return warrant_file_path, file_name

    @classmethod
    async def __create_user_warrant_content(
        cls, context: UserRequestHostelAccommodationWarrantViewOut
    ) -> str:
        rendered_template = file_manager.render(
            TEMPLATES_PATH, HOSTEL_WARRANT_TEMPLATE, context
        )
        created_at = datetime.strptime(
            context.created_at.strftime(Settings.DATETIME_FORMAT),
            Settings.DATETIME_FORMAT,
        )
        file_date_created = str(created_at).replace(":", "-").replace(" ", "_")
        document_name = (
            f"hostel_warrant_{file_date_created}_{context.user_request_id}.docx"
        )

        Path(WARRANT_HOSTEL_ACCOMMODATION_PATH).mkdir(exist_ok=True)

        document_path = file_manager.create(
            WARRANT_HOSTEL_ACCOMMODATION_PATH, document_name, rendered_template
        )

        return document_path

    @classmethod
    async def __generate_user_document_name_for_download(
        cls, document_name: str, user_id: int, session: AsyncSession
    ) -> str:
        student = await student_service.read(session=session, data={"user_id": user_id})
        return (
            f"{document_name.replace(' ', '_')}_{student.first_name}_"
            f"{student.last_name}.docx"
        )


service_handler = ServiceHandler()
