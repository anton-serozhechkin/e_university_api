from enum import Enum, IntEnum


class Gender(Enum):
    """Enum based class to set up of Gender status"""

    MALE = "Чоловічий"
    FEMALE = "Жіночий"


class CourseOfStudy(IntEnum):
    FIRST_COURSE = 1
    SECOND_COURSE = 2
    THIRD_COURSE = 3
    FOURTH_COURSE = 4
    FIFTH_COURSE = 5
    SIXTH_COURSE = 6
