from models.http_response_model import HttpResponse
from services.logger_services import init_loggers
import os
from utils.database_utils import init_db
from models.room_model import Room
from fastapi.responses import JSONResponse
from fastapi import status as STATUS, HTTPException
from sqlalchemy.orm import Query


# Initialize debug and error loggers
debug_logger, error_logger = init_loggers(os.path.basename(__file__))


def get_rooms_list(page: int, number_of_records: int):
    """
    Fetches and returns a list of all rooms from the database.
    """
    # Create a new database session
    session = init_db()

    try:
        query: Query = session.query(Room)

        rooms: [Room] = query.offset((page - 1) * 10).limit(number_of_records).all()

        # Transform room to a list of dictionaries
        rooms_list = [room.transform_to_dict() for room in rooms]

        # Log and return the user list
        debug_logger.info("Got the room list successfully!")
        return JSONResponse(status_code=STATUS.HTTP_200_OK,
                            content=HttpResponse(message='', data=rooms_list).convert_to_json())

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


def inactive_room(room_id: int) -> None:
    session = init_db()

    try:
        # Query the specific booking by user_id
        query: Query = session.query(Room).filter(Room.room_id == room_id)

        room: Room = query.first()

        # Handle the case where the Booking doesn't exist
        if room is None:
            debug_logger.debug(f"Room with id {room_id} not found!")

        else:
            debug_logger.info(f"Room with id {room_id} found!")
            room.room_is_booked = False
            session.commit()

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise Exception(str(e))

    finally:
        session.close()
