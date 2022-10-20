from sqlalchemy import select, delete, insert

from models.student import Student
from models.students_list_view import students_list_view
from schemas.student import CreateStudentOut, CreateStudentIn, StudentsListOut, DeleteStudentIn
from handlers.current_user import get_current_user

from db import database
from typing import List, Union

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema

router = APIRouter()


@router.post("/{university_id}/students/", response_model=JSENDOutSchema[CreateStudentOut], tags=["Admin dashboard"])
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

    student_id = await database.execute(query)

    return {
        "data": {
            "student_id": student_id
        },
        "message": f"Create student {student.full_name}"
    }


@router.get("/{university_id}/students/", response_model=JSENDOutSchema[List[StudentsListOut]],
            tags=["Admin dashboard"])
async def read_students_list(university_id: int, faculty_id: Union[int, None] = None, user=Depends(get_current_user)):
    if faculty_id:
        query = select(students_list_view).where(students_list_view.c.faculty_id == faculty_id)
    else:
        query = select(students_list_view).where(students_list_view.c.university_id == university_id)

    return {
        "data": await database.fetch_all(query),
        "message": f"Get students list of the university with id {university_id}"
    }


@router.delete("/{university_id}/students/", response_model=JSENDOutSchema, tags=["SuperAdmin dashboard"])
async def delete_student(university_id: int, delete_student: DeleteStudentIn, auth=Depends(get_current_user)):
    query = delete(Student).where(Student.student_id == delete_student.student_id)

    await database.execute(query)

    return {
        "data": {
            "student_id": delete_student.student_id
        },
        "message": f"Deleted student with id {delete_student.student_id}"
    }
