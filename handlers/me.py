from handlers.current_user import get_current_user
from schemas.current_user import UserOut, UserIn

from fastapi import Depends, APIRouter


router = APIRouter()


@router.get('/me', summary='Отримати інформацію про поточного користувача, який увійшов у систему', response_model=UserOut)
async def get_me(user: UserIn = Depends(get_current_user)):
    return user
