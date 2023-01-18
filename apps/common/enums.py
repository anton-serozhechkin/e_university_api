from enum import Enum


class JSENDStatus(str, Enum):
    """Enum based class to set type of JSEND statuses."""

    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"


class UserRequestStatus(str, Enum):
    """Enum based class to set status of user request."""

    APPROVED = 1
    REJECTED = 2
    IN_PROGRESS = 3
    CANCELLED = 4


class MultipartSubtypeEnum(Enum):
    mixed = "mixed"
    digest = "digest"
    alternative = "alternative"
    related = "related"
    report = "report"
    signed = "signed"
    encrypted = "encrypted"
    form_data = "form-data"
    mixed_replace = "x-mixed-replace"
    byterange = "byterange"
