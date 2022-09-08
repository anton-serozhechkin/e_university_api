from pydantic import BaseModel


class CourseListOut(BaseModel):
    course_id: int
    course_number: int 