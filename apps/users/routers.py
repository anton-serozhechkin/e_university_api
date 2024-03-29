from typing import List, Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.dependencies import get_async_session, get_current_user
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.users.handlers import user_handler
from apps.users.schemas import (
    CreateStudentIn,
    CreateStudentOut,
    CreateUserIn,
    CreateUserOut,
    DeleteStudentIn,
    DeleteUserIn,
    RegistrationIn,
    StudentCheckExistenceIn,
    StudentCheckExistenceOut,
    StudentsListOut,
    UserIn,
    UserOut,
    UsersListViewOut,
)

users_router = APIRouter()


@users_router.post(
    "/check-student-existence/",
    name="create_student_existence",
    response_model=JSENDOutSchema[StudentCheckExistenceOut],
    summary="Check student existence",
    responses={
        200: {"description": "Successful check student existence response"},
        404: {
            "model": JSENDFailOutSchema,
            "description": "Invalid input data response",
        },
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
    },
    tags=["Users application"],
)
async def check_student(
    request: Request,
    student: StudentCheckExistenceIn,
    session: AsyncSession = Depends(get_async_session),
):
    """**Check student existence in the database**.

    **Input**:
    - **last_name**: last name of the student
    - **first_name**: first name of the student
    - **telephone_number**: telephone number, must be 12 digits

    **Return**:
    - **student_id**: int, id of student
    - **token**: str, used for user registration
    - **expires_at**: datetime, token expires datetime
    """
    result = await user_handler.check_student(
        request=request, student=student, session=session
    )
    return {
        "data": result,
        "message": f"Get information of student with id {result.student_id}",
    }


@users_router.get(
    "/{university_id}/users/",
    name="read_users_list",
    response_model=JSENDOutSchema[List[UsersListViewOut]],
    summary="Get university users list",
    responses={
        200: {
            "description": "Successful get all users list of the university response"
        },
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
    },
    tags=["Users application"],
)
async def read_users_list(
    request: Request,
    university_id: int,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return {
        "data": await user_handler.read_users_list(
            request=request, university_id=university_id, session=session
        ),
        "message": f"Got user list of the university with id {university_id}",
    }


@users_router.post(
    "/{university_id}/users/",
    name="create_user",
    response_model=JSENDOutSchema[CreateUserOut],
    summary="Create user",
    responses={
        200: {"description": "Successful create user response"},
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
    },
    tags=["Users application"],
)
async def create_user(
    request: Request,
    university_id: int,
    user: CreateUserIn,
    auth=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """**Method for creating user record**.

    **Path**:
    - **university_id**: university id for creating user

    **Input**:
    - **email**: user email, only letters (a-z), numbers (0-9) and periods (.) are
        allowed, required
    - **password**: password, cannot be empty, required
    - **password_re_check**: password recheck, required
    - **role_id**: user role id, required
    - **faculty_id**: user faculty id, required

    **Return**:
    - **user_id**: int, id of created user
    - **login**: str, username of created user
    - **last_visit**: datetime, date and time of last successfull user login
    - **email**: str, user email
    - **is_active**: bool, flag which indicates is user active
    - **role_id**: int, id of user role
    """
    user = await user_handler.create_user(request=request, user=user, session=session)
    return {"data": user, "message": f"Created user with id {user.user_id}"}


@users_router.delete(
    "/{university_id}/users/",
    name="delete_user",
    response_model=JSENDOutSchema[DeleteUserIn],
    summary="Delete user",
    responses={
        200: {"description": "Successful delete user response"},
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
    },
    tags=["Users application"],
)
async def delete_user(
    request: Request,
    university_id: int,
    data: DeleteUserIn,
    auth=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await user_handler.del_user(request=request, delete_user=data, session=session)
    return {
        "data": {"user_id": data.user_id},
        "message": f"Deleted user with id {data.user_id}",
    }


@users_router.post(
    "/registration",
    name="registration",
    response_model=JSENDOutSchema[CreateUserOut],
    summary="User registration",
    responses={
        200: {"description": "Successful user registration response"},
        403: {
            "model": JSENDFailOutSchema,
            "description": "Registration time expired fail response",
        },
        404: {
            "model": JSENDFailOutSchema,
            "description": "Invalid input data response",
        },
        409: {
            "model": JSENDFailOutSchema,
            "description": "Input data already exist response",
        },
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
    },
    tags=["Users application"],
)
async def registration(
    request: Request,
    user: RegistrationIn,
    session: AsyncSession = Depends(get_async_session),
):
    """**Method for user registration, using token based on student's record**.

    **Input**:
    - **token**: token from "Check user existence"
    - **email**: enter user email; only letters (a-z), numbers (0-9) and
        periods (.) are allowed
    - **password**: enter password; password cannot be empty

    **Return**:
    - **user_id**: int, id of created user
    - **login**: str, username of created user
    - **last_visit**: datetime, date and time of last successfull user login
    - **email**: str, user email
    - **is_active**: bool, flag which indicates is user active
    - **role_id**: int, id of user role
    """
    response = await user_handler.registration(
        request=request, user=user, session=session
    )
    return {
        "data": response,
        "message": f"User with id {response.user_id} was registered successfully",
    }


@users_router.post(
    "/{university_id}/students/",
    name="create_student",
    response_model=JSENDOutSchema[CreateStudentOut],
    summary="Create university student",
    responses={
        200: {"description": "Successful create student of the university response"},
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
    },
    tags=["Users application"],
)
# TODO after input id of the non-existent university it creates student
async def create_student(
    request: Request,
    university_id: int,
    student: CreateStudentIn,
    auth=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """**Method for university student record creating**.

    **Path**:
    - **university_id**: university id

    **Input**:
    - **last_name**: student last name, required
    - **first_name**: student fist name, required
    - **middle_name**: student middle name, not required
    - **telephone_number**: student telephone number, must consists of 12 digits,
        required
    - **course_id**: student course id, must be between 1 and 6, required
    - **faculty_id**: faculty id, required
    - **speciality_id**: speciality id, required
    - **gender**: student gender, 'Ч' or 'Ж', required

    **Return**:
    - created student id
    """
    student = await user_handler.create_student(
        request=request, student=student, session=session
    )
    return {
        "data": student,
        "message": f"Created student with id {student.student_id}",
    }


@users_router.get(
    "/{university_id}/students/",
    name="read_students_list",
    response_model=JSENDOutSchema[List[StudentsListOut]],
    summary="Get university students list",
    responses={
        200: {"description": "Successful get all university students list response"},
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
    },
    tags=["Users application"],
)
async def read_students_list(
    request: Request,
    university_id: int,
    faculty_id: Optional[int] = None,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):  # TODO returns students if url params aren't exists in DB
    return {
        "data": await user_handler.read_students_list(
            request=request,
            university_id=university_id,
            faculty_id=faculty_id,
            session=session,
        ),
        "message": f"Got students list of the university with id {university_id}",
    }


@users_router.delete(
    "/{university_id}/students/",
    name="delete_student",
    response_model=JSENDOutSchema[DeleteStudentIn],
    summary="Delete university student",
    responses={
        200: {"description": "Successful delete university student response"},
        422: {"model": JSENDFailOutSchema, "description": "ValidationError"},
    },
    tags=["Users application"],
)
async def delete_student(
    request: Request,
    university_id: int,
    del_student: DeleteStudentIn,
    auth=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await user_handler.delete_student(
        request=request, del_student=del_student, session=session
    )
    return {
        "data": {"student_id": del_student.student_id},
        "message": f"Deleted student with id {del_student.student_id}",
    }


@users_router.get(
    "/me",
    name="read_me",
    response_model=JSENDOutSchema[UserOut],
    summary="Get current user info",
    responses={
        200: {"description": "Successful get current user information response"}
    },
    tags=["Users application"],
)
async def get_me(user: UserIn = Depends(get_current_user)):
    return {"data": user, "message": "Got user information"}
