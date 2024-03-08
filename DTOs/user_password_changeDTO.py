from pydantic import BaseModel


class UserChangePasswordDTO(BaseModel):
    user_id: int
    old_password: str
    new_password: str
