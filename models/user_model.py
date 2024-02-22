import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INT, DATE, TEXT, VARCHAR, BOOLEAN

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = Column(INT, primary_key=True, name="id")
    user_username = Column(DATE, name="username")
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
                 user_updated_at: datetime.datetime
                 ):
        self.user_username = user_name
        self.user_password_hash = password_hash
        self.user_role = user_role
        self.user_status = user_status,
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_updated_at = user_updated_at

    def transform_to_dict(self):
        return {
            'id': self.user_id,
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

