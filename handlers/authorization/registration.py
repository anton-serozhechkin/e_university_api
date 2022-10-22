from sqlalchemy import update, select, insert

from models.user import User
from models.student import Student
from models.one_time_token import OneTimeToken
from models.user_faculty import UserFaculty
from db import database
from components.utils import get_hashed_password
from schemas.user import RegistrationIn, RegistrationOut

from random import randint
from datetime import datetime

from translitua import translit
from fastapi import APIRouter, status as http_status

from schemas.jsend import JSENDOutSchema, JSENDErrorOutSchema, JSENDFailOutSchema
from components.exceptions import BackendException

router = APIRouter(
    responses={422: {"model": JSENDErrorOutSchema, "description": "ValidationError"},
               403: {"model": JSENDFailOutSchema, "description": "Registration time expired fail response"},
               404: {"model": JSENDFailOutSchema, "description": "Invalid input data response"},
               409: {"model": JSENDFailOutSchema, "description": "Input data already exist response"}}
)


@router.post("/registration",
             name="registration",
             response_model=JSENDOutSchema[RegistrationOut],
             summary="User registration",
             responses={200: {"description": "Successful user registration response"}},
             tags=["Authorization"])
async def registation(user: RegistrationIn):  # TODO spelling mistake 'registRation'

    RegistrationIn(
        token=user.token,
        email=user.email,
        password=user.password,
        password_re_check=user.password_re_check)

    query = select(OneTimeToken).where(OneTimeToken.token == user.token)
    token_data = await database.fetch_all(query)

    if not token_data:
        raise BackendException(
            message="To register a user, first go to the page for checking the presence of a student in the register.",
            code=http_status.HTTP_404_NOT_FOUND
        )

    for token in token_data:
        expires = token.expires
        student_id = token.student_id

    datetime_utc_now = datetime.utcnow()

    if datetime_utc_now > expires:  # TODO Local variable 'expires' might be referenced before assignment
        raise BackendException(
            message=("Registration time has expired."
                     "Please go to the link to check the availability of students on the register."),
            code=http_status.HTTP_403_FORBIDDEN
        )

    query = select(Student).where(Student.student_id == student_id)
    student = await database.fetch_all(query)

    if not student:
        raise BackendException(
            message="Student is not found.",
            code=http_status.HTTP_404_NOT_FOUND
        )

    for item in student:
        full_name = item.full_name
        faculty_id = item.faculty_id
        student_user_id = item.user_id

    if student_user_id:  # TODO Local variable 'student_user_id' might be referenced before assignment
        raise BackendException(
            message="A student account already exists. Please check your email for details.",
            code=http_status.HTTP_409_CONFLICT
        )

    transliterated_full_name = translit(full_name)  # TODO Local variable 'full_name' might be referenced before assignment
    login = f"{(transliterated_full_name[:4])}-{randint(100, 999)}".lower()

    # Encoding password
    encoded_user_password = get_hashed_password(user.password)

    query = insert(User).values(login=login, email=user.email, password=encoded_user_password, role_id=1,
                                is_active=True)
    last_record_id = await database.execute(query)

    query = update(Student).values(user_id=last_record_id).where(Student.student_id == student_id)
    await database.execute(query)

    query = insert(UserFaculty).values(user_id=last_record_id, faculty_id=faculty_id).returning(
        UserFaculty.faculty_id)     # TODO Local variable 'faculty_id' might be referenced before assignment
    user_faculty_data = await database.execute(query)

    return {
        "data": {
            "user_id": last_record_id,
            "faculty_id": user_faculty_data,
            "login": login
        },
        "message": f"User with id {last_record_id} was registered successfully",
        "code": http_status.HTTP_201_CREATED
    }
