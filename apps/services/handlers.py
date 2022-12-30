from apps.common.file_managers import file_manager
from apps.services.models import STATUS_MAPPING
from apps.services.schemas import (CancelRequestIn, CountHostelAccommodationCostIn,
                                   CreateUserRequestIn, UserRequestReviewIn, CreateCustomHostelAccommodationIn)
from apps.services.services import (
    bed_place_service, get_specialties_list, hostel_accommodation_service, hostel_service,
    request_existence_service, user_document_service, service_service, user_request_list_service,
    user_faculty_service, user_request_service, user_request_booking_hostel_service,
    user_request_review_service, user_request_detail_service
)
from apps.services.utils import (
    create_faculty_dict, create_telephone_set, get_worksheet_cell_col_row, check_faculty_existence,
    check_specialty_existence, check_telephone_number_existence, check_for_empty_value, check_file_existing
)
from apps.users.schemas import CreateStudentIn, UserOut
from apps.users.services import student_service
from settings import (Settings, TEMPLATES_PATH, SETTLEMENT_HOSTEL_PATH, HOSTEL_BOOKING_TEMPLATE)

from datetime import datetime, date
from decimal import Decimal
from fastapi import File, Request, UploadFile
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceHandler:

    async def create_custom_hostel_accommodation(
            self,
            *,
            request: Request,
            university_id: int,
            user_request: CreateCustomHostelAccommodationIn,
            user: UserOut,
            session: AsyncSession
    ):
        user_faculty_result = await user_faculty_service.read(data={"user_id": user.user_id}, session=session)
        data = {"date_created": datetime.now(),
                "comment": user_request.comment,
                "user_id": user.user_id,
                "service_id": 1,
                "faculty_id": user_faculty_result.faculty_id,
                "university_id": university_id,
                "status_id": STATUS_MAPPING.get("Розглядається")}

        response = await user_request_booking_hostel_service.read(session=session,
                                                                  data={"user_id": user.user_id,
                                                                        "university_id": university_id})
        result = dict(response)
        result.update(full_name={'last_name': user_request.student_last_name.capitalize(),
                                 'first_name': user_request.student_first_name.capitalize(),
                                 'middle_name': user_request.student_middle_name.capitalize()},
                      rector_full_name={'last_name': user_request.rector_last_name.capitalize(),
                                        'first_name': user_request.rector_first_name.capitalize(),
                                        'middle_name': user_request.rector_middle_name.capitalize()},
                      speciality_name=user_request.speciality_name,
                      speciality_code=user_request.speciality_code,
                      course=user_request.course,
                      faculty_name=user_request.faculty_name,
                      educ_level=user_request.educ_level)
        user_request = await user_request_service.create(session=session, data=data)
        prepared_data = {
            "context": result,
            "service_id": user_request.service_id,
            "user_request_id": user_request.user_request_id
        }

        await self.__create_user_document(session, **prepared_data)

        return {
            "status_id": STATUS_MAPPING.get("Розглядається"),
            "user_request_id": user_request.user_request_id
        }
    async def read_user_request_existence(
            self,
            *,
            request: Request,
            university_id: int,
            service_id: int,
            user: UserOut,
            session: AsyncSession
    ):
        user_request_result = await request_existence_service.read(
            session=session,
            data={"university_id": university_id, "service_id": service_id, "user_id": user.user_id}
        )
        if user_request_result:
            return {
                "user_request_id": user_request_result.user_request_id,
                "status": user_request_result.status,
                "user_request_exist": True
            }
        return {
            "user_request_id": None,
            "status": None,
            "user_request_exist": False
        }

    async def read_user_request_list(
            self,
            *,
            request: Request,
            university_id: int,
            user: UserOut,
            session: AsyncSession
    ):
        return await user_request_list_service.list(
            session=session,
            filters={"university_id": university_id, "user_id": user.user_id}
        )

    async def create_user_request(
            self,
            *,
            request: Request,
            university_id: int,
            user_request: CreateUserRequestIn,
            user: UserOut,
            session: AsyncSession
    ):
        user_faculty_result = await user_faculty_service.read(data={"user_id": user.user_id}, session=session)
        data = {"date_created": datetime.now(),
                "comment": user_request.comment,
                "user_id": user.user_id,
                "service_id": user_request.service_id,
                "faculty_id": user_faculty_result.faculty_id,
                "university_id": university_id,
                "status_id": STATUS_MAPPING.get("Розглядається")}
        user_request = await user_request_service.create(session=session, data=data)
        result = await user_request_booking_hostel_service.read(
            session=session,
            data={"user_id": user.user_id, "university_id": university_id})
        prepared_data = {
            "context": result,
            "service_id": user_request.service_id,
            "user_request_id": user_request.user_request_id
        }
        await self.__create_user_document(session, **prepared_data)
        return {
            "status_id": STATUS_MAPPING.get("Розглядається"),
            "user_request_id": user_request.user_request_id
        }

    async def read_user_request_booking_hostel(
            self,
            *,
            request: Request,
            university_id: int,
            user: UserOut,
            session: AsyncSession
    ):
        return await user_request_booking_hostel_service.read(
            session=session,
            data={"user_id": user.user_id, "university_id": university_id})

    async def cancel_request(
            self,
            *,
            request: Request,
            user_request_id: int,
            cancel_request: CancelRequestIn,
            session: AsyncSession):
        CancelRequestIn(status_id=cancel_request.status_id)
        await user_request_service.update(
            session=session,
            data={"user_request_id": user_request_id},
            obj=cancel_request)
        return {
            "user_request_id": user_request_id,
            "status_id": cancel_request.status_id
        }

    async def create_user_request_review(
            self,
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            user_request_review: UserRequestReviewIn,
            user: UserOut,
            session: AsyncSession):
        created_user_request_review = await user_request_review_service.create(
            session=session,
            data={
                "university_id": university_id,
                "user_request_id": user_request_id,
                "date_created": datetime.now(),
                "reviewer": user.user_id,
                "hostel_id": user_request_review.hostel_id,
                "room_number": user_request_review.room_number,
                "start_date_accommodation": user_request_review.start_date_accommodation.now(),
                "end_date_accommodation": user_request_review.end_date_accommodation.now(),
                "total_sum": user_request_review.total_sum,
                "payment_deadline": user_request_review.payment_deadline.now(),
                "remark": user_request_review.remark,
                "bed_place_id": user_request_review.bed_place_id
            })
        await user_request_service.update(
            session=session,
            data={"user_request_id": user_request_id},
            obj={"status_id": user_request_review.status_id}
        )
        return {
            "status_id": user_request_review.status_id,
            "user_request_review_id": created_user_request_review.user_request_review_id
        }

    async def read_hostel_accommodation(
            self,
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            session: AsyncSession):
        response = await hostel_accommodation_service.read(
            session=session,
            data={
                "university_id": university_id,
                "user_request_id": user_request_id
            })
        # TODO AttributeError: 'NoneType' object has no attribute 'documents' (it's happened only if user request doesn't have review)
        return response

    async def read_request_details(
            self,
            *,
            request: Request,
            university_id: int,
            user_request_id: int,
            session: AsyncSession):
        return await user_request_detail_service.read(
            session=session,
            data={
                "university_id": university_id,
                "user_request_id": user_request_id
            })

    async def read_user_document(
            self,
            *,
            request: Request,
            university_id: int,
            user_document_id: int,
            user: UserOut,
            session: AsyncSession):
        user_document = await user_document_service.read(session=session, data={"user_document_id": user_document_id})
        return file_manager.get(user_document.content)

    async def download_user_document(
            self,
            *,
            request: Request,
            university_id: int,
            user_document_id: int,
            user: UserOut,
            session: AsyncSession):
        user_document = await user_document_service.read(
            session=session, data={"user_document_id": user_document_id})
        check_for_empty_value(user_document, 'user_document_id')
        check_file_existing(user_document.content)
        file_name = await self.__generate_user_document_name_for_download(user_document.name, user.user_id, session)
        return user_document.content, file_name

    async def count_hostel_accommodation_cost(
            self,
            *,
            request: Request,
            university_id: int,
            data: CountHostelAccommodationCostIn,
            session: AsyncSession):
        hostel = await hostel_service.read(
            session=session,
            data={"hostel_id": data.hostel_id}
        )

        bed_place = await bed_place_service.read(
            session=session,
            data={"bed_place_id": data.bed_place_id}
        )

        months_count = self.calculate_difference_between_dates_in_months(data.end_date_accommodation,
                                                                         data.start_date_accommodation)
        month_price = self.get_month_price_by_bed_place(hostel.month_price, bed_place.bed_place_name)

        response = self.calculate_total_hostel_accommodation_cost(month_price, months_count)
        return {
            'total_hostel_accommodation_cost': response
        }

    @classmethod
    def calculate_difference_between_dates_in_months(cls, end_date: date, start_date: date) -> int:
        return (end_date.month - start_date.month + 12 * (end_date.year - start_date.year)) + 1

    @classmethod
    def get_month_price_by_bed_place(cls, hostel_month_price: Decimal, bed_place_name: str) -> Decimal:
        return Decimal(hostel_month_price) * Decimal(bed_place_name)

    @classmethod
    def calculate_total_hostel_accommodation_cost(cls, month_price: Decimal, month_difference: int) -> Decimal:
        return month_price * month_difference

    @classmethod
    async def __create_user_document(cls, session, **kwargs):
        service_id = kwargs.get("service_id")
        name = await cls.__generate_user_document_name(service_id, session)
        date_created = datetime.strptime(datetime.now().strftime(Settings.DATETIME_FORMAT),
                                         Settings.DATETIME_FORMAT)
        kwargs["date_created"] = date_created
        content = await cls.__create_user_document_content_hostel_settlement_service(**kwargs)
        user_document_record = await user_document_service.create(
            session=session,
            data={
                "date_created": date_created,
                "name": name,
                "content": content,
                "user_request_id": kwargs.get("user_request_id")
            })
        return user_document_record

    @classmethod
    async def __create_user_document_content_hostel_settlement_service(cls, **kwargs) -> str:
        context = kwargs.get("context")
        rendered_template = file_manager.render(TEMPLATES_PATH, HOSTEL_BOOKING_TEMPLATE, context)
        file_date_created = str(kwargs.get('date_created')).replace(":", "-").replace(" ", "_")
        document_name = f"hostel_settlement_{file_date_created}_{kwargs.get('user_request_id')}.docx"
        DOCUMENT_PATH = SETTLEMENT_HOSTEL_PATH / str(context['user_id'])
        Path(DOCUMENT_PATH).mkdir(exist_ok=True)
        document_path = file_manager.create(DOCUMENT_PATH, document_name, rendered_template)
        return document_path

    @classmethod
    async def __generate_user_document_name(cls, service_id: int, session: AsyncSession) -> str:
        service = await service_service.read(
            session=session,
            data={"service_id": service_id}
        )
        return f"Заява на {service.service_name.lower()}"

    @classmethod
    async def __generate_user_document_name_for_download(cls, document_name: str, user_id: int,
                                                         session: AsyncSession) -> str:
        student = await student_service.read(session=session, data={"user_id": user_id})
        return f"{document_name.replace(' ', '_')}_{student.first_name}_{student.last_name}.docx"

    @staticmethod
    async def create_students_list_from_file(
            *,
            request: Request,
            university_id: int,
            file: UploadFile = File(...),
            session: AsyncSession):
        specialties, students = await get_specialties_list(university_id), []

        faculty_dict = create_faculty_dict(specialties)

        telephone_set = await create_telephone_set(session=session, filters={"university_id": university_id})

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
                gender=cell(i, col + 8)
            )
            students.append(student)
        return await student_service.create_many(
            session=session,
            objs=students
        )


service_handler = ServiceHandler()
