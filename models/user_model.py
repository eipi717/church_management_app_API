from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, INT, DATE, TEXT, VARCHAR, BOOLEAN
from helpers.user_helper import hash_password_SHA256

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(INT, primary_key=True, name="user_id")
    user_username = Column(VARCHAR, name="username")
    user_password_hash = Column(TEXT, name="password_hash")
    user_status = Column(BOOLEAN, name="status")
    user_role = Column(VARCHAR, name="role")
    user_first_name = Column(VARCHAR, name="first_name")
    user_last_name = Column(VARCHAR, name="last_name")
    user_created_time = Column(DATE, name="created_at")
    user_updated_at = Column(DATE, name="updated_at")
    user_last_login = Column(DATE, name="last_login")

    def __init__(self,
                 user_name: str,
                 password_hash: str,
                 user_role: str,
                 user_status: bool,
                 user_first_name: str,
                 user_last_name: str,
                 ):
        self.user_username = user_name
        self.user_password_hash = hash_password_SHA256(password_hash)
        self.user_role = user_role
        self.user_status = user_status
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name

    def transform_to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.user_username,
            'password_hash': self.user_password_hash,
            'status': self.user_status,
            'role': self.user_role,
            'first_name': self.user_first_name,
            'last_name': self.user_last_name,
            'created_at': self.user_created_time,
            'updated_at': self.user_updated_at,
            'last_login': self.user_last_login
        }

    def to_dict_basic_information(self):
        return {
            'user_id': self.user_id,
            'username': self.user_username,
            'password': self.user_password_hash,
            'last_login': self.user_last_login
        }

    def find_booking(self):
        print(self.bookings)