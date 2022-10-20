from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from components.enums import JSENDStatus
from components.exceptions import BackendException
from settings import Settings
from starlette.exceptions import HTTPException as StarletteHTTPException


def backend_exception_handler(request: Request, exc: BackendException) -> JSONResponse:
    """Return result from Back-end exception."""
    response = JSONResponse(content=exc.dict())
    response.status_code = exc.code
    return response


def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Get the original 'detail' and 'status_code'."""
    response = JSONResponse(
        content={
            "status": JSENDStatus.FAIL,
            "data": exc.detail,
            "message": "Validation error.",
            "code": exc.status_code,
        }
    )
    response.status_code = exc.status_code
    return response


def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
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
    response = JSONResponse(
        content={
            "status": JSENDStatus.FAIL,
            "data": modified_details,
            "message": "Validation error.",
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        }
    )
    response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return response


def integrity_error_handler(error: IntegrityError):
    if "duplicate" in error.args[0]:
        raise BackendException(message=str(error.orig.args[0].split("\n")[-1]) if Settings.DEBUG else "Update error.")
    else:
        raise BackendException(
            message=str(error) if Settings.DEBUG else "Internal server error.",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=JSENDStatus.ERROR,
        )
