from db import database
from handlers import faculty
from handlers.authorization import check_student_existance 

from fastapi import FastAPI


app = FastAPI()

app.include_router(faculty.router)
app.include_router(check_student_existance.router)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
