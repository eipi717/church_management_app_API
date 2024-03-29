from fastapi import APIRouter
import services.room_services as room_services

router = APIRouter()


@router.get('/getAllRooms')
async def get_rooms(page: int | None = 1, numberOfRecords: int | None = 10):
    return room_services.get_rooms_list(page=page, number_of_records=numberOfRecords)
