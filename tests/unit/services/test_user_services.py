import logging
from unittest.mock import patch, MagicMock
from services import user_services

logger = logging.getLogger(__name__)

# -------------------------
# get_users_list
# -------------------------
@patch("services.user_services.init_db", autospec=True)
def test_get_users_list(mock_init_db):
    logger.info("Testing get_users_list")

    mock_user = MagicMock()
    mock_user.transform_to_dict.return_value = {"user_id": 1, "name": "Test User"}

    mock_query = MagicMock()
    mock_query.all.return_value = [mock_user]

    mock_session = MagicMock()
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = user_services.get_users_list()

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200
    assert b"Test User" in response.body


# -------------------------
# get_user_by_id
# -------------------------
@patch("services.user_services.init_db", autospec=True)
def test_get_user_by_id_found(mock_init_db):
    logger.info("Testing get_user_by_id with valid ID")

    mock_user = MagicMock()
    mock_user.transform_to_dict.return_value = {"user_id": 1, "name": "Found User"}

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user

    mock_session = MagicMock()
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = user_services.get_user_by_id(1)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200
    assert b"Found User" in response.body


@patch("services.user_services.init_db", autospec=True)
def test_get_user_by_id_not_found(mock_init_db):
    logger.info("Testing get_user_by_id with invalid ID")

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None

    mock_session = MagicMock()
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = user_services.get_user_by_id(999)

    logger.info(f"Expected: 404 Not Found; Got: {response.status_code}")
    assert response.status_code == 404


# -------------------------
# create_user
# -------------------------
@patch("services.user_services.init_db", autospec=True)
def test_create_user(mock_init_db):
    logger.info("Testing create_user")

    mock_user = MagicMock()
    mock_user.transform_to_dict.return_value = {"user_id": 1, "name": "Created User"}

    mock_dto = MagicMock()
    mock_dto.transform.return_value = mock_user

    mock_session = MagicMock()
    mock_init_db.return_value = mock_session

    response = user_services.create_user(mock_dto)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200
    assert b"Created User" in response.body


# -------------------------
# change_password
# -------------------------
@patch("services.auth_services.user_helper.validate_password", return_value=True)
@patch("services.auth_services.user_helper.hash_password_SHA256", return_value="hashed")
@patch("services.user_services.init_db", autospec=True)
def test_change_password_success(mock_init_db, mock_validate, mock_hash):
    logger.info("Testing change_password with correct old password")

    mock_user = MagicMock()
    mock_user.transform_to_dict.return_value = {"user_id": 1, "name": "Updated"}

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user

    mock_session = MagicMock()
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    mock_dto = MagicMock()
    mock_dto.user_id = 1
    mock_dto.old_password = "old_pass"
    mock_dto.new_password = "new_pass"

    response = user_services.change_password(mock_dto)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200
    assert b"Updated" in response.body


@patch("services.user_services.user_helper.validate_password", return_value=False)
@patch("services.user_services.init_db", autospec=True)
def test_change_password_incorrect_old(mock_init_db, mock_validate):
    logger.info("Testing change_password with incorrect old password")

    mock_user = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user

    mock_session = MagicMock()
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    mock_dto = MagicMock()
    mock_dto.user_id = 1
    mock_dto.old_password = "wrong_pass"

    response = user_services.change_password(mock_dto)

    logger.info(f"Expected: 401 Unauthorized; Got: {response.status_code}")
    assert response.status_code == 401
    assert b"Incorrect password!" in response.body


@patch("services.user_services.init_db", autospec=True)
def test_change_password_user_not_found(mock_init_db):
    logger.info("Testing change_password with user not found")

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None

    mock_session = MagicMock()
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    mock_dto = MagicMock()
    mock_dto.user_id = 999

    response = user_services.change_password(mock_dto)

    logger.info(f"Expected: 401 Unauthorized; Got: {response.status_code}")
    assert response.status_code == 401
    assert b"User not found!" in response.body