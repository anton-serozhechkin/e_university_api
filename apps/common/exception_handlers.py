from apps.common.enums import JSENDStatus
from apps.common.exceptions import BackendException

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from settings import Settings
from sqlalchemy.exc import IntegrityError


def backend_exception_handler(request: Request, exc: BackendException) -> JSONResponse:
    """Return result from Back-end exception."""
    response = JSONResponse(content=exc.dict())
    response.status_code = exc.code
    return response


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
