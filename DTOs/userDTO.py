from pydantic import BaseModel, Field
from models.user_model import User
from typing import Optional


class UserDTO(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    status: Optional[bool] = None
    role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    def transform(self) -> User:
        return User(user_name=self.username, password_hash=self.password, user_role=self.role,
                    user_status=self.status, user_first_name=self.first_name, user_last_name=self.last_name)