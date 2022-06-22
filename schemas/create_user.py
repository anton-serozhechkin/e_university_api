import re

from pydantic import BaseModel, validator
from typing import List

class CreateUserIn(BaseModel):
    
    email: str
    password: str
    password_re_check: str
    role_id: int
    faculty_id: List[int]

    @validator('email')
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

    @validator('password_re_check')
    def validate_password(cls, v, values):
        password = values.get('password')

        if not password or not v:
            raise ValueError('Паролі не можуть бути порожніми')

        if password != v:
            raise ValueError('Введені паролі не співпадають')

        return v


class CreateUserOut(BaseModel):
    user_id: int
