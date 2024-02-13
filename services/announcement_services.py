# Import necessary libraries and modules
from DTOs.announcementDTO import AnnouncementDTO
from models.announcement_model import Announcement
from helpers.announcement_helper import update_announcement_by_new_announcement
from utils.database_utils import init_db
from utils.logging_utils import Logger
from enums.logging_enums import LogLevel
import os
from models.http_response_model import HttpResponse
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status as STATUS

# Initialize debug and error loggers
debug_logger = Logger(name=os.path.basename(__file__), level=str(LogLevel.DEBUG)).create_logger()
error_logger = Logger(name=os.path.basename(__file__), level=str(LogLevel.ERROR)).create_logger()


def get_announcement_list():
    """
    Fetches and returns a list of all announcements from the database.
    """
    # Create a new database session
    session = init_db()

    try:
        # Query all announcements
        announcements = session.query(Announcement).all()

        # Transform announcements to a list of dictionaries
        announcement_list = [announcement.transform_to_dict() for announcement in announcements]

        # Log and return the announcement list
        debug_logger.info("Got the announcement list successfully!")
        return JSONResponse(status_code=STATUS.HTTP_200_OK,
                            content=HttpResponse(message='', data=announcement_list).convert_to_json())

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_announcement_by_id(announcement_id: int):
    """
    Fetches and returns a specific announcement by its ID.
    """
    session = init_db()

    try:
        # Query the specific announcement by ID
        announcement = session.query(Announcement).filter(Announcement.announcement_id == announcement_id).first()

        # Handle the case where the announcement doesn't exist
        if announcement is None:
            debug_logger.debug(f"Announcement with id {announcement_id} not found!")
            return JSONResponse(
                status_code=STATUS.HTTP_404_NOT_FOUND,
                content=HttpResponse(message=f"Announcement with id {announcement_id} not found!",
                                     data=[]).convert_to_json()
            )
        else:
            # Return the found announcement
            debug_logger.info(f"Announcement with id {announcement_id} found!")
            return JSONResponse(
                status_code=STATUS.HTTP_200_OK,
                content=HttpResponse(message='', data=[announcement.transform_to_dict()]).convert_to_json()
            )

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def create_announcement(announcement_dto: AnnouncementDTO):
    """
    Creates a new announcement in the database.
    """
    session = init_db()

    try:
        # Add the new announcement to the session and commit
        session.add(announcement_dto.transform())
        session.commit()

        # Log success and return the created announcement
        debug_logger.info("Created the announcement successfully!")
        return JSONResponse(
            status_code=STATUS.HTTP_200_OK,
            content=HttpResponse(message='Succeed!', data=[announcement_dto.transform()]).convert_to_json()
        )

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def update_announcement(announcement_dto: AnnouncementDTO, announcement_id: int):
    """Updates an existing announcement."""
    session = init_db()

    try:
        # Fetch the announcement to be updated
        announcement = session.query(Announcement).filter(Announcement.announcement_id == announcement_id).first()

        if announcement is None:
            # Handle the case where the announcement doesn't exist
            debug_logger.debug(f"Announcement with id {announcement_id} not found!")
            return JSONResponse(
                status_code=STATUS.HTTP_404_NOT_FOUND,
                content=HttpResponse(message=f"Announcement with id {announcement_id} not found!",
                                     data=[]).convert_to_json()
            )
        else:
            # Update the announcement with new data and commit
            update_announcement_by_new_announcement(old_announcement=announcement,
                                                    new_announcement=announcement_dto.transform())
            session.commit()

            # Log success and return the updated announcement
            debug_logger.info(f"Announcement with id {announcement_id} updated!")
            return JSONResponse(
                status_code=STATUS.HTTP_200_OK,
                content=HttpResponse(message='', data=[announcement.transform_to_dict()]).convert_to_json()
            )

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_announcement(announcement_id: int):
    """
    deletes an existing announcement.
    """
    session = init_db()

    try:
        # Fetch the announcement to be updated
        announcement = session.query(Announcement).filter(Announcement.announcement_id == announcement_id).first()

        if announcement is None:
            # Handle the case where the announcement doesn't exist
            debug_logger.debug(f"Announcement with id {announcement_id} not found!")
            return JSONResponse(
                status_code=STATUS.HTTP_404_NOT_FOUND,
                content=HttpResponse(message=f"Announcement with id {announcement_id} not found!",
                                     data=[]).convert_to_json()
            )
        else:
            # Delete the announcement with new data and commit

            session.delete(announcement)
            session.commit()

            # Log success and return the updated announcement
            debug_logger.info(f"Announcement with id {announcement_id} deleted!")
            return JSONResponse(
                status_code=STATUS.HTTP_200_OK,
                content=HttpResponse(message='', data=[announcement.transform_to_dict()]).convert_to_json()
            )

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
