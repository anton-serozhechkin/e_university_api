from urllib import response
from webbrowser import get
from models.student import student as student_table
from db import database 
from sqlalchemy import * 
from typing import List     

from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class StudentIn(BaseModel):
    full_name: str
    telephony_number: int


class Student(BaseModel):
    student_id: int
    full_name: str
    telephone_number: int
    faculty_id: int
    user_id: int



@router.post("/students/", response_model=List[StudentIn])
async def read_students():
    bar_tags = StudentIn
    query = """SELECT * FROM table student WHERE tags LIKE '%' :bar_tags '%'"""
    tags_res_list = database.execute(text(query), {"bar_tags": bar_tags}).fetchall()


