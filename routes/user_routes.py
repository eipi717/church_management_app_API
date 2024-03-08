from fastapi import APIRouter
import services.user_services as user_services
from DTOs.userDTO import UserDTO
from DTOs.user_password_changeDTO import UserChangePasswordDTO

router = APIRouter()


@router.get('/getUsers')
async def get_users():
    return user_services.get_users_list()


@router.post('/createUsers')
async def create_users(user: UserDTO):
    return user_services.create_user(user_dto=user)


@router.post('/changePassword', )
async def change_password(user_change_password: UserChangePasswordDTO):
    return user_services.change_password(user_change_password=user_change_password)