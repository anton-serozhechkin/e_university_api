from apps.authorization.handlers import authorization_router
from apps.components.exception_handlers import backend_exception_handler, http_exception_handler
from apps.components.exceptions import BackendException
from apps.educational_institutions.handlers import educational_institutions_router
from apps.hostel.handlers import hostel_router
from apps.services.handlers import services_router
from apps.users.handlers import users_router
from apps.core.db import database
from settings import Settings
from tags_metadata import metadata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


# Endpoints registration
app.include_router(users_router)
app.include_router(hostel_router)
app.include_router(educational_institutions_router)
app.include_router(services_router)
app.include_router(authorization_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
