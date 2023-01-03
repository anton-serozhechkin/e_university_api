from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Union

from pydantic import root_validator, validator

from apps.common.schemas import (
    BaseInSchema,
    BaseOutSchema,
    FullNameSchema,
    HostelNameSchema,
    UserDocumentsSchema,
)


speciality = {51: 'Економіка', 121: 'Інженерія програмного забезпечення', 122: "Комп'ютерні науки", 124: 'Системний аналіз',
              125: 'Кібербезпека', 126: 'Інформаційні системи та технології', 186: 'Видавництво та поліграфія',
              53: 'Психологія', 81: 'Право, освітня програма', 232: 'Соціальне забезпечення',
              281: 'Публічне управління та адміністрування', 73: 'Менеджмент', 75: 'Маркетинг',
              22: 'Дизайн', 72: 'Фінанси, банківська справа та страхування', 71: 'Облік і оподаткування',
              11: '"Освітні, педагогічні науки"', 52: 'Політологія', 61: 'Журналістика',
              291:'Міжнародні відносини, суспільні комунікації та регіональні студії', 292: 'Міжнародні економічні відносини',
              76: '"Підприємництво, торгівля та біржова діяльність"', 241: 'Готельно-ресторанна справа', 242: 'Туризм'}


class RequestForHostelAccommodationIn(BaseInSchema):
    rector_first_name: str
    rector_middle_name: str
    rector_last_name: str
    student_first_name: str
    student_middle_name: str
    student_last_name: str
    speciality_code: int
    speciality_name: str
    course: int
    faculty_name: str
    educ_level: str
    comment: str

    @root_validator
    def validate_rector_and_student_names(cls, values):
        names = ['rector_first_name', 'rector_middle_name', 'rector_last_name', 'student_first_name',
                 'student_middle_name', 'student_last_name']
        for name in names:
            if not values.get(name).istitle():
                raise ValueError(f"{name.replace('_', ' ').capitalize()} first letter must be uppercase")
        return values

    @validator('educ_level')
    def validate_education_level(cls, value):
        if value not in ['B', 'M']:
            raise ValueError('Wrong education level value. Should be \'B\' or \'M\', uppercase also')
        return value

    @validator('faculty_name')
    def validate_faculty_name(cls, value):
        if value not in ['Інформаційних технологій', 'Міжнародних відносин і журналістики',
                         'Міжнародної економіки і підприємництва', 'Фінансів і обліку',
                         'Менеджмента і маркетингу', 'Економіки і права']:
            raise ValueError(f'Wrong \'{value}\' number. This faculty doesn\'t exist')
        return value

    @validator('speciality_code')
    def validate_speciality_code(cls, value):
        if value not in speciality.keys():
            raise ValueError(f'Wrong \'{value}\'number. This speciality doesn\'t exist')
        return value

    @validator('speciality_name')
    def validate_speciality_name(cls, value):
        if value not in speciality.values():
            raise ValueError(f'Wrong \'{value}\' name. This speciality doesn\'t exist')
        return value

    @validator('course')
    def validate_course(cls, value):
        if value not in [1, 2, 3, 4, 5, 6]:
            raise ValueError(f"Wrong \'{value}\' number. This course doesn't exist")
        return value

    @root_validator
    def validate_speciality_name_and_speciality_code_correspondence(cls, values):
        if not speciality[values.get('speciality_code')] == values.get('speciality_name'):
                raise ValueError(f"Speciality code \'{values.get('speciality_code')}\' doesn't correspondence with exists "
                                 f"\'{values.get('speciality_name')}\' speciality name")
        return values

class CreateUserRequestIn(BaseInSchema):
    service_id: int
    comment: str = None


class CreateUserRequestOut(BaseOutSchema):
    user_request_id: int
    status_id: int


class UserRequestExistenceOut(BaseOutSchema):
    user_request_id: int = None
    status: Dict[str, Union[int, str]] = None
    user_request_exist: bool = False


class UserRequestBookingHostelOut(BaseOutSchema):
    full_name: FullNameSchema
    user_id: int
    faculty_name: str
    university_id: int
    short_university_name: str
    rector_full_name: FullNameSchema
    date_today: date
    start_year: int
    finish_year: int
    speciality_code: int
    speciality_name: str
    course: int
    educ_level: str
    gender: str


class UserRequestsListOut(BaseOutSchema):
    university_id: int
    user_id: int
    user_request_id: int
    service_name: str
    status: Dict[str, Union[int, str]]
    created_at: datetime


class CancelRequestIn(BaseInSchema):
    status_id: int

    @validator("status_id")
    def validate_status_id(cls, v):
        if v != 4:
            raise ValueError("The application can only be canceled")
        return v


class CancelRequestOut(BaseOutSchema):
    user_request_id: int
    status_id: int


class UserRequestReviewIn(BaseInSchema):
    status_id: int
    room_number: int = None
    start_accommodation_date: date = None
    end_accommodation_date: date = None
    # TODO it's define as decimal, but return int
    total_sum: Decimal = None
    payment_deadline_date: date = None
    remark: str = None
    hostel_id: int = None
    bed_place_id: int = None

    @validator("status_id")
    def validate_status_id(cls, v):
        if v not in [1, 2]:
            raise ValueError("The application can only be approved or rejected")
        return v


class UserRequestReviewOut(BaseOutSchema):
    status_id: int
    user_request_review_id: int


class HostelAccomodationViewOut(BaseOutSchema):
    university_id: int
    user_request_review_id: int
    user_request_id: int
    hostel_name: Dict[str, Union[int, str]]
    hostel_address: Dict[str, str]
    bed_place_name: str
    # TODO it's define as decimal, but return int
    month_price: Decimal
    start_accommodation_date: date
    end_accommodation_date: date
    # TODO it's define as decimal, but return int
    total_sum: Decimal
    iban: str
    university_name: str
    organisation_code: str
    payment_recognition: str
    commandant_full_name: FullNameSchema
    telephone_number: str
    documents: Dict[str, str]


class UserRequestDetailsViewOut(BaseOutSchema):
    user_request_id: int
    university_id: int
    created_at: datetime
    service_name: str
    status_name: str
    status_id: int
    comment: str = None
    hostel_name: HostelNameSchema
    room_number: int = None
    bed_place_name: str = None
    remark: str = None
    documents: List[UserDocumentsSchema]


class CountHostelAccommodationCostIn(BaseInSchema):
    hostel_id: int
    start_accommodation_date: date
    end_accommodation_date: date
    bed_place_id: int

    @root_validator
    def validate_two_dates(cls, values):
        if values.get("start_accommodation_date") >= values.get(
            "end_accommodation_date"
        ):
            raise ValueError(
                "Start date of hostel accommodation can't be more or equal than end"
                " date of hostel accommodation"
            )
        return values


class CountHostelAccommodationCostOut(BaseOutSchema):
    total_hostel_accommodation_cost: Decimal
