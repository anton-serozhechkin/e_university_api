from apps.authorization.routers import authorization_router
from apps.common.exception_handlers import (backend_exception_handler, http_exception_handler,
                                            validation_exception_handler)
from apps.common.exceptions import BackendException
from apps.educational_institutions.routers import educational_institutions_router
from apps.hostel.routers import hostel_router
from apps.services.routers import services_router
from apps.users.routers import users_router
from apps.common.db import database
from settings import Settings
from tags_metadata import metadata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI(openapi_tags=metadata)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.CORS_ALLOW_ORIGINS,
    allow_credentials=Settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=Settings.CORS_ALLOW_METHODS,
    allow_headers=Settings.CORS_ALLOW_HEADERS,
)

# Add exception handlers
app.add_exception_handler(BackendException, backend_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)


# Endpoints registration
app.include_router(users_router)
app.include_router(hostel_router)
app.include_router(educational_institutions_router)
app.include_router(services_router)
app.include_router(authorization_router)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()
