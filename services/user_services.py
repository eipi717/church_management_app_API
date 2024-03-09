import datetime

from DTOs.userDTO import UserDTO
from DTOs.user_password_changeDTO import UserChangePasswordDTO
from helpers import user_helper
from models.user_model import User
from services.logger_services import init_loggers
from utils import response_utils
from utils.database_utils import init_db
import os
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
                            content=response_utils.response_with_data(data=users_list))

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


def get_user_by_id(user_id: int):
    """
    Fetches and returns a specific user by its ID.
    """
    session = init_db()

    try:
        # Query the specific User by ID
        user = session.query(User).filter(User.user_id == user_id).first()

        # Handle the case where the User doesn't exist
        if user is None:
            debug_logger.debug(f"User with id {user_id} not found!")
            return JSONResponse(
                status_code=STATUS.HTTP_404_NOT_FOUND,
                content=response_utils.empty_response(message=f"User with id {user_id} not found!"))
        else:
            # Return the found user
            debug_logger.info(f"User with id {user_id} found!")
            return JSONResponse(
                status_code=STATUS.HTTP_200_OK,
                content=response_utils.response_with_data(data=[user.transform_to_dict()]))

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
            content=response_utils.response_with_data(data=user.transform_to_dict()))

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
                            content=response_utils.empty_response(message='User not found!'))

    # Validate the password
    is_password_correct = user_helper.validate_password(hashed_password=user.user_password_hash, password_string=user_change_password.old_password)

    if not is_password_correct:
        debug_logger.info("Incorrect password!")
        return JSONResponse(status_code=STATUS.HTTP_401_UNAUTHORIZED,
                            content=response_utils.empty_response(message='Incorrect password!'))

    try:
        user.user_password_hash = user_helper.hash_password_SHA256(password=user_change_password.new_password)
        session.commit()
        return JSONResponse(
            status_code=STATUS.HTTP_200_OK,
            content=response_utils.response_with_data(data=user.transform_to_dict())
        )
    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        session.rollback()
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


