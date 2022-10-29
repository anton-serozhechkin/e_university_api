from apps.hostel.services import AsyncCRUDBase
from apps.educational_institutions.models import faculty_list_view, Faculty, speciality_list_view, Course


faculty_list_service = AsyncCRUDBase(model=faculty_list_view)
faculty_create_service = AsyncCRUDBase(model=Faculty)
speciality_list_service = AsyncCRUDBase(model=speciality_list_view)
course_list_service = AsyncCRUDBase(model=Course)
