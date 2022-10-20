from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from components.enums import JSENDStatus
from components.exceptions import BackendException
from settings import Settings


def backend_exception_handler(request: Request, exc: BackendException) -> JSONResponse:
    """Return result from Back-end exception."""
    response = JSONResponse(content=exc.dict())
    response.status_code = exc.code
    return response
