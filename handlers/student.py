from sqlalchemy import select, delete, insert

from models.student import Student
from models.students_list_view import students_list_view
from schemas.student import CreateStudentOut, CreateStudentIn, StudentsListOut, DeleteStudentIn
from handlers.current_user import get_current_user

from db import database
from typing import List, Union

from fastapi import APIRouter, Depends, status as http_status

from schemas.jsend import JSENDOutSchema, JSENDErrorOutSchema

router = APIRouter(
    responses={422: {"model": JSENDErrorOutSchema, "description": "ValidationError"}}
)


@router.post("/{university_id}/students/",
             name="post_student",
             response_model=JSENDOutSchema[CreateStudentOut],
             summary="Create university student",
             responses={200: {"description": "Successful create student of the university response"}},
             tags=["Admin dashboard"])   # TODO after input id of the non-existent university it creates student
async def create_student(university_id: int, student: CreateStudentIn, auth=Depends(get_current_user)):
    CreateStudentIn(
        full_name=student.full_name,
        telephone_number=student.telephone_number,
        course_id=student.course_id,
        faculty_id=student.faculty_id,
        speciality_id=student.speciality_id,
        gender=student.gender)

    query = insert(Student).values(full_name=student.full_name, telephone_number=student.telephone_number,
                                   course_id=student.course_id, faculty_id=student.faculty_id,
                                   speciality_id=student.speciality_id, gender=student.gender.upper())

    return {
        "data": {
            "student_id": await database.execute(query)
        },
        "message": f"Created student {student.full_name}",
        "code": http_status.HTTP_201_CREATED
    }


@router.get("/{university_id}/students/",
            name="get_students_list",
            response_model=JSENDOutSchema[List[StudentsListOut]],
            summary="Get university students list",
            responses={200: {"description": "Successful get all university students list response"}},
            tags=["Admin dashboard"])
async def read_students_list(university_id: int, faculty_id: Union[int, None] = None, user=Depends(get_current_user)):  # TODO after input id of the non-existent university it returns the students
    if faculty_id:
        query = select(students_list_view).where(students_list_view.c.faculty_id == faculty_id)
    else:
        query = select(students_list_view).where(students_list_view.c.university_id == university_id)

    return {
        "data": await database.fetch_all(query),
        "message": f"Got students list of the university with id {university_id}"
    }


@router.delete("/{university_id}/students/",
               name="delete_student",
               response_model=JSENDOutSchema,
               summary="Delete university student",
               responses={200: {"description": "Successful delete university student response"}},
               tags=["SuperAdmin dashboard"])
async def delete_student(university_id: int, delete_student: DeleteStudentIn, auth=Depends(get_current_user)):
    query = delete(Student).where(Student.student_id == delete_student.student_id)

    await database.execute(query)
    # TODO: in response key data has empty dict value, not like it's discribed 
    return {
        "data": {
            "student_id": delete_student.student_id
        },
        "message": f"Deleted student with id {delete_student.student_id}",
        "code": http_status.HTTP_202_ACCEPTED
    }
