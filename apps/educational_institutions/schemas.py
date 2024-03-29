import re
from typing import Dict, Union

from pydantic import validator

from apps.common.schemas import BaseInSchema, BaseOutSchema, FullNameSchema


class DeanOut(FullNameSchema):
    dean_id: int


class FacultyIn(BaseInSchema):
    university_id: int
    name: str
    shortname: str
    main_email: str = None
    dean_id: int = None
    dean_last_name: str = None
    dean_first_name: str = None
    dean_middle_name: str = None

    @validator("main_email")
    def validate_email(cls, v: str) -> str:
        """The method is using for email validation.

        Only letters (a-z), numbers (0-9) and periods (.) are allowed

        Return: True or not None string
        """
        specials = "!#$%&'*+-/=?^_`{|?."
        specials = re.escape(specials)
        regex = re.compile(
            "^(?!["
            + specials
            + "])(?!.*["
            + specials
            + "]{2})(?!.*["
            + specials
            + "]$)[A-Za-z0-9"
            + specials
            + "]+(?<!["
            + specials
            + "])@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$"
        )
        message = False

        if not v:
            message = "The email address cannot be empty"

        elif not re.fullmatch(regex, v):
            message = f"Invalid email address format: {v}"

        if message:
            raise ValueError(message)

        return v


class FacultyOut(BaseOutSchema):
    university_id: int
    faculty_id: int
    name: str
    shortname: str
    main_email: str = None
    dean_id: int
    dean_full_name: FullNameSchema = (
        None  # TODO after creating new faculty it value of field is equal null
    )


class SpecialityOut(BaseOutSchema):
    faculty_id: int
    speciality_id: int
    university_id: int
    speciality_info: Dict[str, Union[int, str]]


class CourseOut(BaseOutSchema):
    course_id: int
    value: int
