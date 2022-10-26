from apps.educational_institutions.models import faculty_list_view, Faculty, speciality_list_view, Course
from apps.educational_institutions.schemas import FacultyIn
from apps.common.db import database

from sqlalchemy import select, insert


async def post_faculties(university_id: int):
    query = select(faculty_list_view).where(faculty_list_view.c.university_id == university_id)
    return await database.fetch_all(query)


async def post_faculty(faculty: FacultyIn):
    query = insert(Faculty).values(name=faculty.name, shortname=faculty.shortname,
                                   main_email=faculty.main_email,
                                   university_id=faculty.university_id)

    last_record_id = await database.execute(query)
    return {
        **faculty.dict(),
        "faculty_id": last_record_id
    }


async def get_speciality_list(university_id: int):
    query = select(speciality_list_view).where(speciality_list_view.c.university_id == university_id)
    return await database.fetch_all(query)


async def get_courses_list():
    query = select(Course)
    return await database.fetch_all(query)
