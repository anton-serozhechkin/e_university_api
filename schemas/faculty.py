import re

from pydantic import BaseModel, validator


class FacultyIn(BaseModel):

    university_id: int
    name: str
    shortname: str
    main_email: str = None

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
                           '[A-Za-z0-9' + specials + ']+(?<!['+ specials + '])@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')
        message = False

        if not v:
            message = "Електронний адрес не може бути порожнім"

        elif not re.fullmatch(regex, v):
            message = f"Невірний формат адреси електронної пошти: {v}."

        if message:
            raise ValueError(message)

        return v
    

class FacultyOut(BaseModel):
    faculty_id: int
    name: str
    shortname: str
    main_email: str = None
    university_id: int
    decan_first_name: str = None
    decan_last_name: str = None
    decan_middle_name: str = None
