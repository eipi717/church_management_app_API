import datetime

from DTOs.userDTO import UserDTO
from DTOs.user_password_changeDTO import UserChangePasswordDTO
from helpers import user_helper
from models.user_model import User
from services.logger_services import init_loggers
from utils.database_utils import init_db
import os
from models.http_response_model import HttpResponse
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status as STATUS

# Initialize debug and error loggers
debug_logger, error_logger = init_loggers(os.path.basename(__file__))


def get_users_list():
    """
    Fetches and returns a list of all users from the database.
    """
    # Create a new database session
    session = init_db()

    try:
        # Query all users
        users = session.query(User).all()

        # Transform user to a list of dictionaries
        users_list = [user.transform_to_dict() for user in users]

        # Log and return the user list
        debug_logger.info("Got the user list successfully!")
        return JSONResponse(status_code=STATUS.HTTP_200_OK,
                            content=HttpResponse(message='', data=users_list).convert_to_json())

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


def create_user(user_dto: UserDTO):
    """
    Creates a new user in the database.
    """
    session = init_db()

    try:
        # Add the new user to the session and commit
        user: User = user_dto.transform()
        user.user_created_time = datetime.datetime.now()
        user.user_updated_at = datetime.datetime.now()
        session.add(user)
        session.commit()

        # Log success and return the created user
        debug_logger.info("Created the user successfully!")
        return JSONResponse(
            status_code=STATUS.HTTP_200_OK,
            content=HttpResponse(message='Succeed!', data=user.transform_to_dict()).convert_to_json()
        )

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        session.rollback()
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


def change_password(user_change_password: UserChangePasswordDTO):

    session = init_db()

    user = session.query(User).filter(User.user_id == user_change_password.user_id).first()

    if user is None:
        debug_logger.info("User not found")
        return JSONResponse(status_code=STATUS.HTTP_401_UNAUTHORIZED,
                            content=HttpResponse(message='User not found!', data=[]).convert_to_json())

    # Validate the password
    is_password_correct = user_helper.validate_password(hashed_password=user.user_password_hash, password_string=user_change_password.old_password)

    if not is_password_correct:
        debug_logger.info("Incorrect password!")
        return JSONResponse(status_code=STATUS.HTTP_401_UNAUTHORIZED,
                            content=HttpResponse(message='Incorrect password!', data=[]).convert_to_json())

    try:
        user.user_password_hash = user_helper.hash_password_SHA256(password=user_change_password.new_password)
        session.commit()
        return JSONResponse(
            status_code=STATUS.HTTP_200_OK,
            content=HttpResponse(message='Succeed!', data=user.transform_to_dict()).convert_to_json()
        )
    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        session.rollback()
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


