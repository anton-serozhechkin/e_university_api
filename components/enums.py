import enum


class JSENDStatus(str, enum.Enum):
    """Enum based class to set type of JSEND statuses."""

    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"
