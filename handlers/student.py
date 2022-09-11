from models.student import student as student_table
from schemas.student import CreateStudentOut, CreateStudentIn
from handlers.current_user import get_current_user

from db import database

from fastapi import Depends, APIRouter 


router = APIRouter()

@router.post("/{university_id}/create-student/", response_model=CreateStudentOut, tags=["Admin dashboard"])
async def create_user(university_id: int, student: CreateStudentIn, auth = Depends(get_current_user)):
    
    CreateStudentIn(
        full_name=student.full_name,
        telephone_number=student.telephone_number,
        course_id=student.course_id,
        faculty_id=student.faculty_id,
        speciality_id=student.speciality_id,
        gender=student.gender)

    query = student_table.insert().values(full_name=student.full_name, telephone_number=student.telephone_number,
                                        course_id=student.course_id, faculty_id=student.faculty_id,
                                        speciality_id=student.speciality_id, gender=student.gender)

    last_record_id = await database.execute(query)
    return last_record_id