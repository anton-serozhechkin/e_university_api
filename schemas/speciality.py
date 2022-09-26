from pydantic import BaseModel

from typing import Dict, Union


class SpecialityListOut(BaseModel):
    faculty_id: int
    speciality_id: int
    university_id: int
    speciality_info: Dict[str, Union[int, str]]
