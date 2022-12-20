from pydantic import ValidationError

from apps.common.enums import JSENDStatus
from apps.common.exceptions import BackendException

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from settings import Settings
from sqlalchemy.exc import IntegrityError
from typing import Union


def backend_exception_handler(request: Request, exc: BackendException) -> JSONResponse:
    """Return result from Back-end exception."""
    return JSONResponse(content=exc.dict(), status_code=exc.code)


def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Get the original 'detail', 'status_code' and 'headers'."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": JSENDStatus.FAIL,
            "data": exc.detail,
            "message": "Validation error.",
            "code": exc.status_code,
        },
        headers=exc.headers
    )


def validation_exception_handler(request: Request, exc: Union[RequestValidationError, ValidationError]) -> JSONResponse:
    """Get the original 'detail' list of errors."""
    details = exc.errors()
    modified_details = []
    for error in details:
        modified_details.append(
            {
                "location": error["loc"],
                "message": error["msg"].capitalize() + ".",
                "type": error["type"],
                "context": error.get("ctx", None),
            }
        )
    return JSONResponse(
        content={
            "status": JSENDStatus.FAIL,
            "data": modified_details,
            "message": "Validation error.",
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def integrity_error_handler(error: IntegrityError) -> None:
    if "duplicate" in error.args[0]:
        raise BackendException(message=str(error.orig.args[0].split("\n")[-1]) if Settings.DEBUG else "Update error.")
    else:
        raise BackendException(
            message=str(error) if Settings.DEBUG else "Internal server error.",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=JSENDStatus.ERROR,
        )
