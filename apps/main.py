from db import database
from tags_metadata import metadata
from hostel.handlers import hostel_router
from educational_institutions.handlers import educational_institutions_router
from users.handlers import users_router


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(openapi_tags=metadata)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints registration
app.include_router(users_router)
app.include_router(hostel_router)
app.include_router(educational_institutions_router)
#


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
