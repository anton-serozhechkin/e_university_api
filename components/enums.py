from enum import Enum


class JSENDStatus(str, Enum):
    """Enum based class to set type of JSEND statuses."""

    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"
