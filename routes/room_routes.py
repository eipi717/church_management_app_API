from fastapi import APIRouter
import services.room_services as room_services

router = APIRouter()


@router.get('/getAllRooms')
async def get_rooms():
    return room_services.get_rooms_list()
