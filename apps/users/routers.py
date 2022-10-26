from apps.users.handlers import get_current_user
from apps.users.schemas import UserOut, UsersListViewOut, CreateUserOut, CreateUserIn, DeleteUserIn, \
    RegistrationOut, RegistrationIn, CreateStudentOut, CreateStudentIn, StudentsListOut, UserIn, DeleteStudentIn, \
    StudentCheckExistanceOut, StudentCheckExistanceIn
from apps.users import handlers
from apps.common.schemas import JSENDOutSchema

from typing import List, Union
from fastapi import Depends, APIRouter


users_router = APIRouter()


@users_router.post("/check-student-existance", response_model=JSENDOutSchema[StudentCheckExistanceOut],
                   tags=["Authorization"])  # TODO spelling mistake, there is need to check path in other modules
async def check_student(student: StudentCheckExistanceIn):
    result = await handlers.check_student(student)
    return {
        "data": {
            'token': result.token,
            'student': result.student,
            'expires': result.expires
        },
        "message": f"Get information of student with id {result.student}"
    }


@users_router.get("/{university_id}/users/", response_model=JSENDOutSchema[List[UsersListViewOut]],
                  tags=["SuperAdmin dashboard"])
async def read_users_list(university_id: int, user=Depends(get_current_user)):
    return {
        "data": await handlers.read_users_list(university_id),
        "message": f"Got user list of the university with id {university_id}"
    }


@users_router.post("/{university_id}/users/", response_model=JSENDOutSchema[CreateUserOut], tags=["SuperAdmin dashboard"])
async def create_user(university_id: int, user: CreateUserIn, auth=Depends(get_current_user)):
    last_record_id = await handlers.create_user(user)
    return {
        "data": {
            "user_id": last_record_id
        },
        "message": f"Created user with id {last_record_id}"
    }


@users_router.delete("/{university_id}/users/", response_model=JSENDOutSchema, tags=["SuperAdmin dashboard"])
async def delete_user(university_id: int, delete_user: DeleteUserIn, auth=Depends(get_current_user)):
    await handlers.del_user(delete_user)
    return {
        "data": {
            "user_id": delete_user.user_id
        },
        "message": f"Deleted user with id {delete_user.user_id}"
    }


@users_router.post("/registration", response_model=JSENDOutSchema[RegistrationOut], tags=["Authorization"])
async def registration(user: RegistrationIn):
    response = await handlers.registration(user)
    return {
        "data": response,
        "message": f"User with id {response['user_id']} was registered successfully"
    }


@users_router.post("/{university_id}/students/", response_model=JSENDOutSchema[CreateStudentOut], tags=["Admin dashboard"])
#TODO after input id of the non-existent university it creates student
async def create_student(university_id: int, student: CreateStudentIn, auth=Depends(get_current_user)):
    return {
        "data": await handlers.create_student(student),
        "message": f"Created student {student.full_name}"
    }


@users_router.get("/{university_id}/students/", response_model=JSENDOutSchema[List[StudentsListOut]],
                  tags=["Admin dashboard"])
async def read_students_list(university_id: int, faculty_id: Union[int, None] = None, user=Depends(get_current_user)):  #TODO after input id of the non-existent university it returns the students
    return {
        "data": await handlers.read_students_list(university_id, faculty_id),
        "message": f"Got students list of the university with id {university_id}"
    }


@users_router.delete("/{university_id}/students/", response_model=JSENDOutSchema, tags=["SuperAdmin dashboard"])
async def delete_student(university_id: int, delete_student: DeleteStudentIn, auth=Depends(get_current_user)):
    await handlers.delete_student(delete_student)
    return {
        "data": {
            "student_id": delete_student.student_id
        },
        "message": f"Deleted student with id {delete_student.student_id}"
    }


@users_router.get('/me', summary='Отримати інформацію про поточного користувача, який увійшов у систему',
                  response_model=JSENDOutSchema[UserOut], tags=["Authorization"])
async def get_me(user: UserIn = Depends(get_current_user)):
    return {
        "data": user,
        "message": "Got user information"
    }
