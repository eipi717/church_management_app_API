import datetime
from helpers.announcement_helper import update_announcement_by_new_announcement
from models.announcement_model import Announcement

def test_update_announcement_by_new_announcement():
    old = Announcement(
        announcement_title="Old Title",
        announcement_date=datetime.datetime(2023, 1, 1),
        announcement_author="Old Author",
        announcement_content="Old Content",
        announcement_status=False,
        announcement_updated_at=datetime.datetime(2023, 1, 1),
    )

    new = Announcement(
        announcement_title="New Title",
        announcement_date=datetime.datetime(2023, 12, 1),
        announcement_author="New Author",
        announcement_content="New Content",
        announcement_status=True,
        # Set old.update_at > new.update_at to test whether update_announcement_by_new_announcement update the update_at field
        announcement_updated_at=datetime.datetime(2021, 1, 1),
    )

    updated = update_announcement_by_new_announcement(old, new)

    assert updated.announcement_title == "New Title"
    assert updated.announcement_date == datetime.datetime(2023, 12, 1)
    assert updated.announcement_author == "New Author"
    assert updated.announcement_content == "New Content"
    assert updated.announcement_status == True
    assert updated.announcement_updated_at > datetime.datetime(2023, 1, 1)