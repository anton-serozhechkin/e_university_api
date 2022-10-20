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
