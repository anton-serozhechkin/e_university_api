from apps.educational_institutions.models import (
    Course,
    Dean,
    Faculty,
    faculty_list_view,
    speciality_list_view,
)
from apps.hostel.services import AsyncCRUDBase

dean_service = AsyncCRUDBase(model=Dean)
faculty_list_service = AsyncCRUDBase(model=faculty_list_view)
faculty_service = AsyncCRUDBase(model=Faculty)
speciality_list_service = AsyncCRUDBase(model=speciality_list_view)
course_list_service = AsyncCRUDBase(model=Course)
