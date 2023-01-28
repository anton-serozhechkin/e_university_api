from enum import Enum


class JSENDStatus(str, Enum):
    """Enum based class to set type of JSEND statuses."""

    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"


class UserRequestStatus(int, Enum):
    """Enum based class to set status of user request."""

    APPROVED = 1
    REJECTED = 2
    IN_PROGRESS = 3
    CANCELLED = 4
