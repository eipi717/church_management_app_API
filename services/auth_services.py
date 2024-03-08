from starlette.responses import JSONResponse

from models.http_response_model import HttpResponse
from utils.database_utils import init_db
from models.user_model import User
from helpers import user_helper
from fastapi import status as STATUS


def login(username: str, password: str):
    """
    Used for user login
    :param username: str
    :param password: str
    :return: JSON
    """
    session = init_db()

    # Filter out the user who matched with the input username
    user = session.query(User).filter(User.user_username == username).first()

    if user is None:
        return JSONResponse(status_code=STATUS.HTTP_401_UNAUTHORIZED,
                            content=HttpResponse(message='User not found!', data=[]).convert_to_json())

    # Validate the password
    is_password_correct = user_helper.validate_password(hashed_password=user.user_password_hash,
                                                        password_string=password)

    if not is_password_correct:
        return JSONResponse(status_code=STATUS.HTTP_401_UNAUTHORIZED,
                            content=HttpResponse(message='Incorrect password!', data=[]).convert_to_json())

    print(f'hello: {is_password_correct}')

    return JSONResponse(status_code=STATUS.HTTP_200_OK,
                        content=HttpResponse(message='', data=[user.to_dict_basic_information()]).convert_to_json())


if __name__ == '__main__':
    print(login('Nicholas Ho', '1234'))
