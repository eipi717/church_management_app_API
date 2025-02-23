from fastapi import APIRouter
import services.room_services as room_services

router = APIRouter()


@router.get('/getAllRooms')
async def get_rooms(page: int | None = 1, numberOfRecords: int | None = 10):
    return room_services.get_rooms_list(page=page, number_of_records=numberOfRecords)


@router.get('/InactiveRoom/{room_id}')
async def incative_room(room_id: int):
    return room_services.inactive_room(room_id=room_id)
