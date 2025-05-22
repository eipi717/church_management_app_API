import datetime
from models.announcement_model import Announcement

def test_announcement_transform_to_dict():
    announcement = Announcement(
        announcement_date=datetime.date(2024, 1, 1),
        announcement_content="Test content",
        announcement_title="Test title",
        announcement_status=True,
        announcement_author="Jane Doe",
        announcement_updated_at=datetime.datetime(2024, 1, 2, 10, 0, 0)
    )
    announcement.announcement_id = 1
    announcement.announcement_created_time = datetime.datetime(2024, 1, 1, 9, 0, 0)

    result = announcement.transform_to_dict()

    assert result["announcement_id"] == 1
    assert result["date"] == datetime.date(2024, 1, 1)
    assert result["content"] == "Test content"
    assert result["title"] == "Test title"
    assert result["status"] is True
    assert result["author"] == "Jane Doe"
    assert result["created_time"] == datetime.datetime(2024, 1, 1, 9, 0, 0)
    assert result["updated_at"] == datetime.datetime(2024, 1, 2, 10, 0, 0)