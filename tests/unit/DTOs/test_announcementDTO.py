import datetime
from DTOs.announcementDTO import AnnouncementDTO
from models.announcement_model import Announcement
import logging

logger = logging.getLogger(__name__)


def test_announcement_dto_initialization():
    logger.info("Testing AnnouncementDTO initialization...")

    dto = AnnouncementDTO(
        announcement_date=datetime.date(2024, 1, 1),
        announcement_content="This is a test announcement.",
        announcement_title="Test Title",
        announcement_status=True,
        announcement_author="Tester"
    )

    assert dto.announcement_date == datetime.date(2024, 1, 1)
    assert dto.announcement_content == "This is a test announcement."
    assert dto.announcement_title == "Test Title"
    assert dto.announcement_status is True
    assert dto.announcement_author == "Tester"

    logger.info("AnnouncementDTO initialized correctly.")


def test_announcement_dto_transform_to_model():
    logger.info("Testing AnnouncementDTO.transform()...")

    dto = AnnouncementDTO(
        announcement_date=datetime.date(2024, 1, 1),
        announcement_content="Sample content",
        announcement_title="Sample title",
        announcement_status=False,
        announcement_author="Admin"
    )

    model: Announcement = dto.transform()

    assert isinstance(model, Announcement)
    assert model.announcement_date == dto.announcement_date
    assert model.announcement_content == dto.announcement_content
    assert model.announcement_title == dto.announcement_title
    assert model.announcement_status == dto.announcement_status
    assert model.announcement_author == dto.announcement_author
    assert isinstance(model.announcement_updated_at, datetime.datetime)

    logger.info("Announcement model generated from DTO successfully.")