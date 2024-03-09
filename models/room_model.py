from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INT, DATE, TEXT, BOOLEAN

Base = declarative_base()


class Room(Base):
    __tablename__ = 'room'

    room_id = Column(INT, primary_key=True, name="room_id")
    room_name = Column(DATE, name="name")
    room_description = Column(TEXT, name="description")
    room_capacity = Column(INT, name='capacity')
    room_is_booked = Column(BOOLEAN, name="isBooked")
    room_created_at = Column(DATE, name='created_at')
    room_last_updated_at = Column(DATE, name='last_updated_at')

    def __init__(self,
                 room_id: int,
                 room_name: str,
                 room_description: str,
                 room_capacity: int,
                 room_is_booked: bool
                 ):
        self.room_id = room_id
        self.room_name = room_name
        self.room_description = room_description
        self.room_capacity = room_capacity
        self.room_is_booked = room_is_booked

    def transform_to_dict(self):
        return {
            'room_id': self.room_id,
            'room_name': self.room_name,
            'room_description': self.room_description,
            'room_capacity': self.room_capacity,
            'room_is_booked': self.room_is_booked,
            'room_created_at': self.room_created_at,
            'room_last_updated_at': self.room_last_updated_at
        }