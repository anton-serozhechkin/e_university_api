from typing import List

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.schemas import FullNameSchema
from apps.educational_institutions.schemas import (
    CourseListOut,
    DeanOut,
    FacultyIn,
    FacultyOut,
    SpecialityListOut,
)
from apps.educational_institutions.services import (
    course_list_service,
    dean_service,
    faculty_list_service,
    faculty_service,
    speciality_list_service,
)


class EduInstitutionHandler:
    @staticmethod
    async def create_dean(
        *, request: Request, data: FullNameSchema, session: AsyncSession
    ) -> DeanOut:
        return await dean_service.create(session=session, obj=data)

    @staticmethod
    async def read_faculties(
        *, request: Request, university_id: int, session: AsyncSession
    ) -> List[FacultyOut]:
        return await faculty_list_service.list(
            session=session, filters={"university_id": university_id}
        )

    async def create_faculty(
        self, *, request: Request, data: FacultyIn, session: AsyncSession
    ) -> FacultyOut:
        if not data.dean_id:
            dean = await self.create_dean(
                request=request,
                data=FullNameSchema(
                    last_name=data.dean_last_name,
                    first_name=data.dean_first_name,
                    middle_name=data.dean_middle_name,
            ),
                session=session,
            )
            data.dean_id = dean.dean_id
        del data.dean_last_name
        del data.dean_first_name
        del data.dean_middle_name
        return await faculty_service.create(session=session, obj=data)

    @staticmethod
    async def read_speciality_list(
        *, request: Request, university_id: int, session: AsyncSession
    ) -> List[SpecialityListOut]:
        return await speciality_list_service.list(
            session=session, filters={"university_id": university_id}
        )

    @staticmethod
    async def read_courses_list(
            *, request: Request, session: AsyncSession,
    ) -> List[CourseListOut]:
        return await course_list_service.list(session=session)


edu_institutions_handler = EduInstitutionHandler()
