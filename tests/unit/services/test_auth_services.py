import logging
from unittest.mock import patch, MagicMock
from services import auth_services

logger = logging.getLogger(__name__)

# -------------------------
# login: user not found
# -------------------------
@patch("services.user_services.init_db", autospec=True)
def test_login_user_not_found(mock_init_db):
    logger.info("Testing login with non-existent user")

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_init_db.return_value = mock_session

    response = auth_services.login("ghostuser", "fakepass")

    logger.info(f"Expected: 401 Unauthorized; Got: {response.status_code}")
    assert response.status_code == 401
    assert b"User not found!" in response.body


# -------------------------
# login: incorrect password
# -------------------------
@patch("services.auth_services.user_helper.validate_password", return_value=False)
@patch("services.auth_services.user_helper.hash_password_SHA256", return_value="hashed")
@patch("services.auth_services.init_db", autospec=True)
def test_login_incorrect_password(mock_init_db, mock_hash, mock_validate):
    logger.info("Testing login with incorrect password")

    mock_user = MagicMock()
    mock_user.user_password_hash = "hashed"
    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = auth_services.login("validuser", "wrongpass")

    logger.info(f"Expected: 401 Unauthorized; Got: {response.status_code}")
    assert response.status_code == 401
    assert b"Incorrect password!" in response.body


# -------------------------
# login: success
# -------------------------
@patch("services.auth_services.user_helper.validate_password", return_value=True)
@patch("services.auth_services.user_helper.hash_password_SHA256", return_value="hashed")
@patch("services.auth_services.init_db", autospec=True)
def test_login_success(mock_init_db, mock_hash, mock_validate):
    logger.info("Testing login with correct credentials")

    mock_user = MagicMock()
    mock_user.user_password_hash = "hashed"
    mock_user.to_dict_basic_information.return_value = {
        "user_id": 1,
        "username": "validuser"
    }

    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = auth_services.login("validuser", "correctpass")

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200
    assert b"validuser" in response.body