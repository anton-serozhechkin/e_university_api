from enum import Enum, IntEnum


class Gender(Enum):
    """Enum based class to set up of Gender status"""

    MALE = "Чоловічий"
    FEMALE = "Жіночий"


class CourseOfStudy(IntEnum):
    """Enum based class to set up Course of study"""

    BACHELOR_FIRST_COURSE = 1
    BACHELOR_SECOND_COURSE = 2
    BACHELOR_THIRD_COURSE = 3
    BACHELOR_FOURTH_COURSE = 4
    MASTER_FIFTH_COURSE = 5
    MASTER_SIXTH_COURSE = 6
