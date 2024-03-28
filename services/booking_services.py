import datetime
import os

from sqlalchemy.orm import Query

from DTOs.bookingDTO import BookingDTO
from models.booking_model import Booking
from services.logger_services import init_loggers
from utils import response_utils
from utils.database_utils import init_db
from fastapi.responses import JSONResponse
from fastapi import status as STATUS, HTTPException

# Initialize debug and error loggers
debug_logger, error_logger = init_loggers(os.path.basename(__file__))


def get_booking_list(is_canceled: bool, page: int, number_of_records: int):
    """
    Fetches and returns a list of all booking from the database.
    """
    # Create a new database session
    session = init_db()

    try:
        # Query all bookings
        query: Query = session.query(Booking).filter(Booking.booking_is_canceled == is_canceled)

        bookings: [Booking] = query.offset(10 * (page - 1)).limit(number_of_records).all()

        # Transform booking to a list of dictionaries
        bookings_list = [booking.transform_to_dict() for booking in bookings]

        # Log and return the booking list
        debug_logger.info("Got the booking list successfully!")
        return JSONResponse(status_code=STATUS.HTTP_200_OK,
                            content=response_utils.response_with_data(data=bookings_list))

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


def get_booking_by_user_id(user_id: int):
    """
    Fetches and returns a specific user by its ID.
    """
    session = init_db()

    try:
        # Query the specific booking by user_id
        query: Query = session.query(Booking).filter(Booking.user_id == user_id)

        booking: Booking = query.first()

        # Handle the case where the Booking doesn't exist
        if booking is None:
            debug_logger.debug(f"User with id {user_id} not found!")
            return JSONResponse(
                status_code=STATUS.HTTP_404_NOT_FOUND,
                content=response_utils.empty_response(message=f"User with id {user_id} not found!")
            )
        else:
            # Return the found user
            debug_logger.info(f"User with id {user_id} found!")
            return JSONResponse(
                status_code=STATUS.HTTP_200_OK,
                content=response_utils.response_with_data(data=booking.transform_to_dict())
            )

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


def get_booking_by_room_id(room_id: int):
    """
    Fetches and returns a specific room by its ID.
    """
    session = init_db()

    try:
        # Check the booking is canceled or not, with the room id
        # To get the valid booking
        query: Query = session.query(Booking).filter(Booking.room_id == room_id, Booking.booking_is_canceled)

        booking: Booking = query.first()

        # Handle the case where the Booking doesn't exist
        if booking is None:
            debug_logger.debug(f"Room with id {room_id} not found!")
            return JSONResponse(
                status_code=STATUS.HTTP_404_NOT_FOUND,
                content=response_utils.empty_response(message=f"User with id {room_id} not found!")
            )
        else:
            # Return the found room
            debug_logger.info(f"Room with id {room_id} found!")
            return JSONResponse(
                status_code=STATUS.HTTP_200_OK,
                content=response_utils.response_with_data(data=booking.transform_to_dict())
            )

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


def create_booking(booking_dto: BookingDTO):
    session = init_db()
    try:
        booking: Booking = booking_dto.transform()
        booking.booing_created_at = datetime.datetime.now()
        booking.booking_last_updated_at = datetime.datetime.now()
        session.add(booking)
        session.commit()
        debug_logger.info("Created the announcement successfully!")
        return JSONResponse(
            status_code=STATUS.HTTP_200_OK,
            content=response_utils.response_with_data(data=booking.transform_to_dict()))

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        session.rollback()
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()
