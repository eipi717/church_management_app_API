import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INT, DATE, TEXT, VARCHAR, BOOLEAN

Base = declarative_base()


class Announcement(Base):
    __tablename__ = 'announcement'

    announcement_id = Column(INT, primary_key=True, name="id")
    announcement_date = Column(DATE, name="date")
    announcement_content = Column(TEXT, name="content")
    announcement_title = Column(VARCHAR, name="title")
    announcement_status = Column(BOOLEAN, name="status")
    announcement_author = Column(VARCHAR, name="author")
    announcement_created_time = Column(DATE, name="created_at")
    announcement_updated_at = Column(DATE, name="updated_at")

    def __init__(self,
                 announcement_date: datetime.date,
                 announcement_content: str,
                 announcement_title: str,
                 announcement_status: bool,
                 announcement_author: str,
                 announcement_updated_at: datetime.datetime
                 ):
        self.announcement_date = announcement_date
        self.announcement_content = announcement_content
        self.announcement_title = announcement_title
        self.announcement_status = announcement_status
        self.announcement_author = announcement_author
        self.announcement_updated_at = announcement_updated_at

    def transform_to_dict(self):
        return {
            'id': self.announcement_id,
            'date': self.announcement_date,
            'content': self.announcement_content,
            'title': self.announcement_title,
            'status': self.announcement_status,
            'author': self.announcement_author,
            'created_time': self.announcement_created_time,
            'updated_at': self.announcement_updated_at
        }

