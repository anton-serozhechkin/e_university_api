from handlers.current_user import get_current_user
from schemas.user import UserOut, UserIn

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema


router = APIRouter()


@router.get('/me', summary='Отримати інформацію про поточного користувача, який увійшов у систему',
            response_model=JSENDOutSchema[UserOut], tags=["Authorization"])
async def get_me(user: UserIn = Depends(get_current_user)):
    return {
        "data": user,
        "message": "Got user information"
    }
