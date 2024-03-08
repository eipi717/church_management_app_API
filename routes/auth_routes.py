from fastapi import APIRouter

from DTOs.userDTO import UserDTO
from services import auth_services

router = APIRouter()


@router.post('/login')
async def login(user_dto: UserDTO):
    return auth_services.login(username=user_dto.username, password=user_dto.password)
