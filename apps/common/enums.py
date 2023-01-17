from enum import Enum


class JSENDStatus(str, Enum):
    """Enum based class to set type of JSEND statuses."""

    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"


class MultipartSubtypeEnum(Enum):
    """
    For more info about Multipart subtypes, visit:
    https://en.wikipedia.org/wiki/MIME#Multipart_subtypes
    """

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
