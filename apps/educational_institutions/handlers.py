from apps.educational_institutions.models import Faculty
from apps.educational_institutions.schemas import CourseListOut, FacultyIn, FacultyOut, SpecialityListOut
from apps.educational_institutions.services import (course_list_service, faculty_service, faculty_list_service,
                                                    speciality_list_service)

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class EduInstitutionHandler:

    @staticmethod
    async def read_faculties(*,
                             request: Request,
                             university_id: int,
                             session: AsyncSession) -> List[FacultyOut]:
        return await faculty_list_service.list(session=session, filters={"university_id": university_id})

    @staticmethod
    async def create_faculty(*,
                             request: Request,
                             data: FacultyIn,
                             session: AsyncSession) -> FacultyOut:
        faculty: Faculty = await faculty_service.create(session=session, obj=data)
        return FacultyOut.from_orm(obj=faculty)

    @staticmethod
    async def read_speciality_list(*,
                                   request: Request,
                                   university_id: int,
                                   session: AsyncSession) -> List[SpecialityListOut]:
        return await speciality_list_service.list(session=session, filters={"university_id": university_id})

    @staticmethod
    async def read_courses_list(*,
                                request: Request,
                                session: AsyncSession) -> List[CourseListOut]:
        return await course_list_service.list(session=session)


edu_institutions_handler = EduInstitutionHandler()
