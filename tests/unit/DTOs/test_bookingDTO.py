import datetime
import logging
from DTOs.bookingDTO import BookingDTO
from models.booking_model import Booking
from pydantic import ValidationError
import pytest

logger = logging.getLogger(__name__)


def test_booking_dto_initialization():
    logger.info("Testing BookingDTO initialization...")

    dto = BookingDTO(
        user_id=1,
        room_id=101,
        start_time=datetime.datetime(2024, 10, 1, 14, 0),
        end_time=datetime.datetime(2024, 10, 1, 15, 0)
    )

    assert dto.user_id == 1
    assert dto.room_id == 101
    assert dto.start_time == datetime.datetime(2024, 10, 1, 14, 0)
    assert dto.end_time == datetime.datetime(2024, 10, 1, 15, 0)

    logger.info("BookingDTO initialized successfully.")


def test_booking_dto_transform_to_model():
    logger.info("Testing BookingDTO.transform()...")

    dto = BookingDTO(
        user_id=2,
        room_id=202,
        start_time=datetime.datetime(2024, 12, 5, 9, 30),
        end_time=datetime.datetime(2024, 12, 5, 11, 0)
    )

    booking: Booking = dto.transform()

    assert isinstance(booking, Booking)
    assert booking.user_id == 2
    assert booking.room_id == 202
    assert booking.booking_start_time == dto.start_time
    assert booking.booking_end_time == dto.end_time

    logger.info("Booking model created successfully from DTO.")


def test_booking_dto_validation_error():
    logger.info("Testing BookingDTO validation error for invalid input...")

    with pytest.raises(ValidationError):
        BookingDTO(
            user_id="not-an-int",
            room_id=None,
            start_time="invalid-date",
            end_time=123
        )