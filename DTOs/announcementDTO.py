from pydantic import BaseModel
import datetime

from models.announcement_model import Announcement


class AnnouncementDTO(BaseModel):
    announcement_date: datetime.date
    announcement_content: str
    announcement_title: str
    announcement_status: bool
    announcement_author: str

    def transform(self) -> Announcement:
        return Announcement(announcement_date=self.announcement_date,
                            announcement_content=self.announcement_content,
                            announcement_author=self.announcement_author, announcement_status=self.announcement_status,
                            announcement_title=self.announcement_title)
