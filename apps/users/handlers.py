from apps.users.schemas import UsersListViewOut, CreateUserIn, CreateUserOut, DeleteUserIn, RegistrationIn, RegistrationOut
from apps.users.schemas import CreateStudentOut, CreateStudentIn, StudentsListOut, DeleteStudentIn
from models.user_list_view import user_list_view
from models.students_list_view import students_list_view
from apps.users.models import user as user_table
from apps.users.models import student as student_table
from apps.users.models import user_faculty
from apps.users.models import one_time_token
from handlers.current_user import get_current_user
from components.utils import get_hashed_password
from db import database

from random import randint
from typing import List, Union
from datetime import datetime

from translitua import translit
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/{university_id}/users/", response_model=List[UsersListViewOut], tags=["SuperAdmin dashboard"])
async def users_list(university_id: int, user = Depends(get_current_user)):
    query = user_list_view.select().where(user_list_view.c.university_id == university_id)
    response = await database.fetch_all(query)
    return response


@router.post("/{university_id}/users/", response_model=CreateUserOut, tags=["SuperAdmin dashboard"])
async def create_user(university_id: int, user: CreateUserIn, auth = Depends(get_current_user)):
    
    CreateUserIn(
        email=user.email,
        password=user.password,
        password_re_check = user.password_re_check,
        role_id =  user.role_id,
        faculty_id = user.faculty_id
    )

    hashed_password = get_hashed_password(user.password)

    login = f"{(user.email[:4])}-{randint(100,999)}".lower()

    query = user_table.insert().values(login=login, password=hashed_password, 
                                        email=user.email, role_id=user.role_id, 
                                        is_active=False)

    last_record_id = await database.execute(query)

    for faculty_id in user.faculty_id:
        query = user_faculty.insert().values(user_id=last_record_id, 
                                            faculty_id = faculty_id)
        await database.execute(query)

    return {
       "user_id": last_record_id
    }


@router.delete("/{university_id}/users/", tags=["SuperAdmin dashboard"])
async def delete_user(university_id: int, delete_user: DeleteUserIn, auth = Depends(get_current_user)):
    query = user_table.delete().where(user_table.c.user_id == delete_user.user_id)
    
    await database.execute(query)

    return {
        "user_id": delete_user.user_id
    }

@router.post("/registration/", response_model=RegistrationOut, tags=["Authorization"])
async def registation(user: RegistrationIn):

    RegistrationIn(
        token=user.token,
        email=user.email,
        password=user.password,
        password_re_check = user.password_re_check)
    
    query = one_time_token.select().where(one_time_token.c.token == user.token)
    token_data = await database.fetch_all(query)

    if not token_data:
        return JSONResponse(status_code=404, content={"message": "Для реєстрації" \
                                            "користувача, спочатку перейдіть на сторінку " \
                                            "перевірки наявності студента в реєстрі"})
 
    for token in token_data: 
        expires = token.expires
        student_id = token.student_id

    datetime_utc_now = datetime.utcnow()

    if datetime_utc_now > expires:
        return JSONResponse(status_code=403, content={"message": "Час на реєстрацію вичерпано. " \
                                            "Будь ласка, перейдіть на посилання для перевірки " \
                                            "наявності студентав реєстрі."})

    query = student_table.select().where(student_table.c.student_id == student_id)
    student = await database.fetch_all(query)
 
    if not student:
        return JSONResponse(status_code=404, content={"message": "Студента не знайдено"})

    for item in student: 
        full_name = item.full_name
        faculty_id = item.faculty_id
        student_user_id = item.user_id

    if student_user_id:
        return JSONResponse(status_code=409, content={"message": "Обліковий запис для студента " \
                                "вже існує. Будь ласка, перевірте деталі на електронній пошті"})

    transliterated_full_name = translit(full_name)
    login = f"{(transliterated_full_name[:4])}-{randint(100,999)}".lower()

    # Encoding password
    encoded_user_password = get_hashed_password(user.password)

    query = user_table.insert().values(login=login, email=user.email, password=encoded_user_password, role_id=1, is_active=True)
    last_record_id = await database.execute(query)

    query = student_table.update().values(user_id=last_record_id).where(student_table.c.student_id == student_id)
    await database.execute(query)

    query = user_faculty.insert().values(user_id=last_record_id, faculty_id = faculty_id).returning(user_faculty.c.faculty_id)    
    user_faculty_data = await database.execute(query)

    response = {
            "user_id": last_record_id, 
            "faculty_id": user_faculty_data, 
            "login": login
    }

    return response


@router.post("/{university_id}/students/", response_model=CreateStudentOut, tags=["Admin dashboard"])
async def create_student(university_id: int, student: CreateStudentIn, auth = Depends(get_current_user)):
    
    CreateStudentIn(
        full_name=student.full_name,
        telephone_number=student.telephone_number,
        course_id=student.course_id,
        faculty_id=student.faculty_id,
        speciality_id=student.speciality_id,
        gender=student.gender)

    query = student_table.insert().values(full_name=student.full_name, telephone_number=student.telephone_number,
                                        course_id=student.course_id, faculty_id=student.faculty_id,
                                        speciality_id=student.speciality_id, gender=student.gender.upper())

    student_id = await database.execute(query)

    return {
       "student_id": student_id
    }


@router.get("/{university_id}/students/", response_model=List[StudentsListOut], tags=["Admin dashboard"])
async def read_students_list(university_id: int, faculty_id: Union[int, None] = None , user = Depends(get_current_user)):
    if faculty_id: 
        query = students_list_view.select().where(students_list_view.c.faculty_id == faculty_id)
    else:
        query = students_list_view.select().where(students_list_view.c.university_id == university_id)
        
    return await database.fetch_all(query)


@router.delete("/{university_id}/students/", tags=["SuperAdmin dashboard"])
async def delete_student(university_id: int, delete_student: DeleteStudentIn, auth = Depends(get_current_user)):
    query = student_table.delete().where(student_table.c.student_id == delete_student.student_id)
    
    await database.execute(query)

    return {
        "student_id": delete_student.student_id
    }
