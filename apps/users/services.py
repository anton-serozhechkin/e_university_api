from apps.common.services import AsyncCRUDBase
from apps.users.models import (
    OneTimeToken,
    Student,
    User,
    user_list_view,
    students_list_view,
)


student_service = AsyncCRUDBase(model=Student)
one_time_token_service = AsyncCRUDBase(model=OneTimeToken)
user_list_service = AsyncCRUDBase(model=user_list_view)
user_service = AsyncCRUDBase(model=User)
student_list_service = AsyncCRUDBase(model=students_list_view)
