import datetime

from models.announcement_model import Announcement
from models.user_model import User
from services.logger_services import init_loggers
from utils.database_utils import init_db
from utils.logging_utils import Logger
from enums.logging_enums import LogLevel
import os
from models.http_response_model import HttpResponse
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status as STATUS

# Initialize debug and error loggers
debug_logger, error_logger = init_loggers(os.path.basename(__file__))


def get_users_list():
    """
    Fetches and returns a list of all announcements from the database.
    """
    # Create a new database session
    session = init_db()

    try:
        # Query all announcements
        users = session.query(User).all()

        # Transform announcements to a list of dictionaries
        users_list = [user.transform_to_dict() for user in users]

        # Log and return the announcement list
        debug_logger.info("Got the announcement list successfully!")
        return JSONResponse(status_code=STATUS.HTTP_200_OK,
                            content=HttpResponse(message='', data=users_list).convert_to_json())

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()
