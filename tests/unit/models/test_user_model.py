import datetime
from models.user_model import User
from helpers.user_helper import hash_password_SHA256


def test_user_transform_to_dict_returns_expected_fields():
    now = datetime.date.today()
    user = User(
        user_name="testuser",
        password_hash="password123",
        user_role="admin",
        user_status=True,
        user_first_name="Test",
        user_last_name="User"
    )

    user.user_id = 1
    user.user_created_time = now
    user.user_updated_at = now
    user.user_last_login = now

    result = user.transform_to_dict()

    assert result["user_id"] == 1
    assert result["username"] == "testuser"
    assert result["password_hash"] == hash_password_SHA256("password123")
    assert result["status"] is True
    assert result["role"] == "admin"
    assert result["first_name"] == "Test"
    assert result["last_name"] == "User"
    assert result["created_at"] == now
    assert result["updated_at"] == now
    assert result["last_login"] == now


def test_user_to_dict_basic_information_returns_subset():
    now = datetime.date.today()
    user = User(
        user_name="simpleuser",
        password_hash="simplepass",
        user_role="member",
        user_status=True,
        user_first_name="Simple",
        user_last_name="User"
    )
    user.user_id = 99
    user.user_last_login = now

    result = user.to_dict_basic_information()

    assert result["user_id"] == 99
    assert result["username"] == "simpleuser"
    assert result["password"] == hash_password_SHA256("simplepass")
    assert result["last_login"] == now