from db import database
from handlers import faculty
from handlers.authorization import check_student_existance 
from handlers.authorization import registration
from handlers.authorization import auth
from handlers import me
from handlers import user


from fastapi import FastAPI


app = FastAPI()

# Endpoints registration
app.include_router(faculty.router)
app.include_router(check_student_existance.router)
app.include_router(registration.router)
app.include_router(auth.router)
app.include_router(me.router)
app.include_router(user.router)



@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
