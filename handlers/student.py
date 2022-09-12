from models.student import student as student_table
from models.students_list_view import students_list_view
from schemas.student import CreateStudentOut, CreateStudentIn, StudentsListOut
from handlers.current_user import get_current_user

from db import database
from typing import List, Union

from fastapi import Depends, APIRouter


router = APIRouter()


@router.post("/{university_id}/create-student/", response_model=CreateStudentOut, tags=["Admin dashboard"])
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

@router.get("/{university_id}/students", response_model=List[StudentsListOut], tags=["Admin dashboard"])
async def read_students_list(university_id: int, faculty_id: Union[int, None] = None , user = Depends(get_current_user)):
    if faculty_id: 
        query = students_list_view.select().where(students_list_view.c.faculty_id == faculty_id)
    else:
        query = students_list_view.select().where(students_list_view.c.university_id == university_id)
        
    return await database.fetch_all(query)
