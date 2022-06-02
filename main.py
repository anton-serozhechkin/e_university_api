from fastapi import FastAPI
from db import database
from handlers import faculty

app = FastAPI()

app.include_router(faculty.router)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
