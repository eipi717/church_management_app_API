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


def get_rooms_list():
    """
    Fetches and returns a list of all rooms from the database.
    """
    # Create a new database session
    session = init_db()

    try:
        query: Query = session.query(Room)

        rooms: [Room] = query.all()

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
