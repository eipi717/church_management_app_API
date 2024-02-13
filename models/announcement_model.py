import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INT, DATE, TEXT, VARCHAR, BOOLEAN

Base = declarative_base()


class Announcement(Base):
    __tablename__ = 'announcement'

    announcement_id = Column(INT, primary_key=True, name="ANNOUNCEMENT_id")
    announcement_date = Column(DATE, name="ANNOUNCEMENT_date")
    announcement_content = Column(TEXT, name="ANNOUNCEMENT_content")
    announcement_title = Column(VARCHAR, name="ANNOUNCEMENT_title")
    announcement_status = Column(BOOLEAN, name="ANNOUNCEMENT_status")
    announcement_author = Column(VARCHAR, name="ANNOUNCEMENT_author")

    def __init__(self,
                 announcement_date: datetime.date,
                 announcement_content: str,
                 announcement_title: str,
                 announcement_status: bool,
                 announcement_author: str
                 ):
        self.announcement_date = announcement_date
        self.announcement_content = announcement_content
        self.announcement_title = announcement_title
        self.announcement_status = announcement_status
        self.announcement_author = announcement_author

    def transform_to_dict(self):
        return {
            'announcement_id': self.announcement_id,
            'announcement_date': self.announcement_date,
            'announcement_content': self.announcement_content,
            'announcement_title': self.announcement_title,
            'announcement_status': self.announcement_status,
            'announcement_author': self.announcement_author
        }

