from models.announcement_model import Announcement


def update_announcement_by_new_announcement(old_announcement: Announcement,
                                            new_announcement: Announcement) -> Announcement:
    """Helper function to update the fields of an announcement."""
    # Directly update fields of the old announcement object
    old_announcement.announcement_title = new_announcement.announcement_title
    old_announcement.announcement_date = new_announcement.announcement_date
    old_announcement.announcement_author = new_announcement.announcement_author
    old_announcement.announcement_content = new_announcement.announcement_content
    old_announcement.announcement_status = new_announcement.announcement_status

    return old_announcement
