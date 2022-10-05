from db import database
from tags_metadata import metadata
#from handlers.authorization import check_student_existance 
#from handlers.authorization import auth
from hostel.handlers import hostel_router
from educational_instuctions.handlers import educational_instructions_router
#from handlers import me


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
app.include_router(hostel_router)
app.include_router(educational_instructions_router)
#


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
