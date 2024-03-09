from fastapi import APIRouter
import services.booking_services as booking_services
from DTOs.bookingDTO import BookingDTO

router = APIRouter()


@router.get('/getAllBookings')
async def get_bookings():
    return booking_services.get_booking_list()


@router.get('/getBookingByUserId/{user_id}')
async def get_booking_by_user_id(user_id: int):
    return booking_services.get_booking_by_user_id(user_id=user_id)


@router.post('/createBooking')
async def create_booking(booking_dto: BookingDTO):
    return booking_services.create_booking(booking_dto=booking_dto)