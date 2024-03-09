import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INT, DATE, ForeignKey
from sqlalchemy.orm import relationship
from models.user_model import User
from models.room_model import Room

Base = declarative_base()


class Booking(Base):
    __tablename__ = 'booking'

    booking_id = Column(INT, primary_key=True, name="booking_id")
    booking_start_time = Column(DATE, name='start_time')
    booking_end_time = Column(DATE, name='end_time')
    booing_created_at = Column(DATE, name='created_at')
    booking_last_updated_at = Column(DATE, name='last_updated')
    user_id = Column(INT, ForeignKey(User.user_id), nullable=False)
    room_id = Column(INT, ForeignKey(Room.room_id), nullable=False)
    user = relationship(User, backref='booking')
    room = relationship(Room, backref='booking')

    def __init__(self,
                 booking_start_time: datetime.datetime,
                 booking_end_time: datetime.datetime,
                 booking_user_id: int,
                 booking_room_id: int
                 ):
        self.booking_start_time = booking_start_time
        self.booking_end_time = booking_end_time
        self.user_id = booking_user_id
        self.room_id = booking_room_id

    def transform_to_dict(self):
        return {
            'booking_id': self.booking_id,
            'booking_start_time': self.booking_start_time,
            'booking_end_time': self.booking_end_time,
            'booking_user_id': self.user_id,
            'booking_room_id': self.room_id,
            'booking_created_at': self.booing_created_at,
            'booking_last_updated_at': self.booking_last_updated_at
        }