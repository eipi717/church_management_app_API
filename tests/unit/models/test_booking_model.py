import datetime
from models.booking_model import Booking

def test_booking_transform_to_dict():
    now = datetime.datetime(2024, 1, 1, 10, 0)
    later = datetime.datetime(2024, 1, 1, 12, 0)

    booking = Booking(
        booking_start_time=now,
        booking_end_time=later,
        booking_user_id=1001,
        booking_room_id=2002
    )

    # Set additional fields
    booking.booking_id = 1
    booking.booking_is_canceled = False
    booking.booing_created_at = datetime.datetime(2024, 1, 1, 9, 0)
    booking.booking_last_updated_at = datetime.datetime(2024, 1, 1, 10, 30)

    result = booking.transform_to_dict()

    assert result["booking_id"] == 1
    assert result["booking_start_time"] == now
    assert result["booking_end_time"] == later
    assert result["booking_user_id"] == 1001
    assert result["booking_room_id"] == 2002
    assert result["booking_is_canceled"] is False
    assert result["booking_created_at"] == datetime.datetime(2024, 1, 1, 9, 0)
    assert result["booking_last_updated_at"] == datetime.datetime(2024, 1, 1, 10, 30)