from apps.authorization.handlers import authorization_router
from apps.common.exception_handlers import backend_exception_handler, http_exception_handler
from apps.common.exceptions import BackendException
from apps.educational_institutions.handlers import educational_institutions_router
from apps.hostel.handlers import hostel_router
from apps.services.handlers import services_router
from apps.users.handlers import users_router
from apps.common.db import database
from settings import Settings
from tags_metadata import metadata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(openapi_tags=metadata)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:4200', 'http://localhost:8000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
