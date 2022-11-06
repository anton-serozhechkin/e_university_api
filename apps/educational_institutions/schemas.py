from apps.common.schemas import BaseOutSchema, BaseInSchema

import re

from pydantic import validator
from typing import Dict, Union


class FacultyIn(BaseInSchema):
    university_id: int
    name: str
    shortname: str
    main_email: str = None
    dean_id: int = None

    @validator('main_email')
    def validate_email(cls, v):
        """
        The method is using for email validation. Only letters (a-z), numbers (0-9) and periods (.) are allowed
        :return: True or not None string
        """
        specials = '!#$%&\'*+-/=?^_`{|?.'
        specials = re.escape(specials)
        regex = re.compile('^(?![' + specials + '])'
                                                '(?!.*[' + specials + ']{2})'
                                                                      '(?!.*[' + specials + ']$)'
                                                                                            '[A-Za-z0-9' + specials + ']+(?<![' + specials + '])@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')
        message = False

        if not v:
            message = "The email address cannot be empty."

        elif not re.fullmatch(regex, v):
            message = f"Invalid email address format: {v}."

        if message:
            raise ValueError(message)

        return v


class FacultyOut(BaseOutSchema):
    faculty_id: int
    name: str
    shortname: str
    main_email: str = None
    university_id: int
    dean_full_name: Dict[str, str] = None


class SpecialityListOut(BaseOutSchema):
    faculty_id: int
    speciality_id: int
    university_id: int
    speciality_info: Dict[str, Union[int, str]]


class CourseListOut(BaseOutSchema):
    course_id: int
    value: int 

   


