from fastapi import APIRouter, Header
import services.booking_services as booking_services
from DTOs.bookingDTO import BookingDTO

router = APIRouter()


@router.get('/getAllBookings')
async def get_bookings(isCanceled: bool | None = False, page: int | None = 1, numberOfRecords: int | None = 10):
    return booking_services.get_booking_list(is_canceled=isCanceled, page=page, number_of_records=numberOfRecords)


@router.get('/getBookingByUserId/{user_id}')
async def get_booking_by_user_id(user_id: int):
    return booking_services.get_booking_by_user_id(user_id=user_id)


@router.post('/createBooking')
async def create_booking(booking_dto: BookingDTO):
    return booking_services.create_booking(booking_dto=booking_dto)


@router.get('/getBookingByRoomId/{room_id}')
async def get_booking_by_room_id(room_id: int):
    return booking_services.get_booking_by_room_id(room_id=room_id)


@router.get('/cancelBooking/{booking_id}')
async def cancel_booking(booking_id: int):
    return booking_services.cancel_booking(booking_id=booking_id)
