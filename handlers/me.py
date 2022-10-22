from handlers.current_user import get_current_user
from schemas.user import UserOut, UserIn

from fastapi import Depends, APIRouter

from schemas.jsend import JSENDOutSchema


router = APIRouter(tags=["Authorization"])


@router.get('/me',
            name="get_me",
            response_model=JSENDOutSchema[UserOut],
            summary='Get current user info',
            responses={200: {"description": "Successful get current user information response"}})
async def get_me(user: UserIn = Depends(get_current_user)):
    return {
        "data": user,
        "message": "Got current user information"
    }
