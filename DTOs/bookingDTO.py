import datetime

from pydantic import BaseModel

from models.booking_model import Booking


class BookingDTO(BaseModel):
    user_id: int
    room_id: int
    start_time: datetime.datetime
    end_time: datetime.datetime

    def transform(self) -> Booking:
        return Booking(booking_start_time=self.start_time, booking_end_time=self.end_time, booking_user_id=self.user_id,
                       booking_room_id=self.room_id)
