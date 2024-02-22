from fastapi import APIRouter
import services.user_services as user_services

router = APIRouter()


@router.get('/getUsers')
async def get_users():
    return user_services.get_users_list()

