# Import necessary libraries and modules
import datetime

from DTOs.announcementDTO import AnnouncementDTO
from models.announcement_model import Announcement
from helpers.announcement_helper import update_announcement_by_new_announcement
from services.logger_services import init_loggers
from utils import response_utils
from utils.database_utils import init_db
import os
from models.http_response_model import HttpResponse
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status as STATUS
from sqlalchemy.orm import Query

# Initialize debug and error loggers
debug_logger, error_logger = init_loggers(os.path.basename(__file__))


def get_announcement_list():
    """
    Fetches and returns a list of all announcements from the database.
    """
    # Create a new database session
    session = init_db()

    try:
        # Query all announcements
        query: Query = session.query(Announcement)

        announcements: [Announcement] = query.all()

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

    finally:
        session.close()


def get_announcement_by_id(announcement_id: int):
    """
    Fetches and returns a specific announcement by its ID.
    """
    session = init_db()

    try:
        # Query the specific announcement by ID
        query: Query = session.query(Announcement).filter(Announcement.announcement_id == announcement_id)

        announcement: Announcement = query.first()

        # Handle the case where the announcement doesn't exist
        if announcement is None:
            debug_logger.debug(f"Announcement with id {announcement_id} not found!")
            return JSONResponse(
                status_code=STATUS.HTTP_404_NOT_FOUND,
                content=response_utils.empty_response(message=f'Announcement with id {announcement_id} not found!')
            )
        else:
            # Return the found announcement
            debug_logger.info(f"Announcement with id {announcement_id} found!")
            return JSONResponse(
                status_code=STATUS.HTTP_200_OK,
                content=response_utils.response_with_data(data=[announcement.transform_to_dict()]))

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


def create_announcement(announcement_dto: AnnouncementDTO):
    """
    Creates a new announcement in the database.
    """
    session = init_db()

    try:
        # Add the new announcement to the session and commit
        announcement: Announcement = announcement_dto.transform()
        announcement.announcement_created_time = datetime.datetime.now()
        announcement.announcement_updated_at = datetime.datetime.now()
        session.add(announcement)
        session.commit()

        # Log success and return the created announcement
        debug_logger.info("Created the announcement successfully!")
        return JSONResponse(
            status_code=STATUS.HTTP_200_OK,
            content=response_utils.response_with_data(data=announcement.transform_to_dict()))

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        session.rollback()
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


def update_announcement(announcement_dto: AnnouncementDTO, announcement_id: int):
    """Updates an existing announcement."""
    session = init_db()

    try:
        # Fetch the announcement to be updated
        query: Query = session.query(Announcement).filter(Announcement.announcement_id == announcement_id)

        announcement: Announcement = query.first()

        if announcement is None:
            # Handle the case where the announcement doesn't exist
            debug_logger.debug(f"Announcement with id {announcement_id} not found!")
            return JSONResponse(
                status_code=STATUS.HTTP_404_NOT_FOUND,
                content=response_utils.empty_response(message=f"Announcement with id {announcement_id} not found!")
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
                content=response_utils.response_with_data(data=[announcement.transform_to_dict()]))

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        session.rollback()
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()


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
                content=response_utils.empty_response(message=f"Announcement with id {announcement_id} not found!")
            )
        else:
            # Delete the announcement with new data and commit

            session.delete(announcement)
            session.commit()

            # Log success and return the updated announcement
            debug_logger.info(f"Announcement with id {announcement_id} deleted!")
            return JSONResponse(
                status_code=STATUS.HTTP_200_OK,
                content=response_utils.response_with_data(data=[announcement.transform_to_dict()]))

    except Exception as e:
        # Log the error and raise HTTP exception
        error_logger.error(str(e))
        session.rollback()
        raise HTTPException(status_code=STATUS.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        session.close()
