from unittest.mock import patch, MagicMock
from services import announcement_services

import logging
logger = logging.getLogger(__name__)

# -------------------------
# get_announcement_list
# -------------------------
@patch("services.announcement_services.init_db", autospec=True)
def test_get_announcement_list(mock_init_db):
    logger.info("Testing get_announcement_list(page=1, number_of_records=10)")

    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_announcement = MagicMock()
    mock_announcement.transform_to_dict.return_value = {"id": 1, "title": "Test"}

    mock_query.offset.return_value.limit.return_value.all.return_value = [mock_announcement]
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = announcement_services.get_announcement_list(page=1, number_of_records=10)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    logger.info(f"Response body: {response.body}")
    assert response.status_code == 200

# -------------------------
# get_announcement_by_id
# -------------------------
@patch("services.announcement_services.init_db", autospec=True)
def test_get_announcement_by_id_found(mock_init_db):
    logger.info("Testing get_announcement_by_id with valid ID=1")

    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_announcement = MagicMock()
    mock_announcement.transform_to_dict.return_value = {"id": 1, "title": "Found"}

    mock_query.filter.return_value.first.return_value = mock_announcement
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = announcement_services.get_announcement_by_id(1)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200

@patch("services.announcement_services.init_db", autospec=True)
def test_get_announcement_by_id_not_found(mock_init_db):
    logger.info("Testing get_announcement_by_id with invalid ID=999")

    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = announcement_services.get_announcement_by_id(999)

    logger.info(f"Expected: 404 Not Found; Got: {response.status_code}")
    assert response.status_code == 404

# -------------------------
# create_announcement
# -------------------------
@patch("services.announcement_services.init_db", autospec=True)
def test_create_announcement(mock_init_db):
    logger.info("Testing create_announcement with mock DTO")

    mock_session = MagicMock()
    mock_announcement = MagicMock()
    mock_announcement.transform_to_dict.return_value = {"id": 1, "title": "Created"}

    mock_dto = MagicMock()
    mock_dto.transform.return_value = mock_announcement
    mock_init_db.return_value = mock_session

    response = announcement_services.create_announcement(mock_dto)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200

# -------------------------
# update_announcement
# -------------------------
@patch("services.announcement_services.update_announcement_by_new_announcement", autospec=True)
@patch("services.announcement_services.init_db", autospec=True)
def test_update_announcement_found(mock_init_db, mock_update_func):
    logger.info("Testing update_announcement with valid ID=1")

    mock_session = MagicMock()
    mock_announcement = MagicMock()
    mock_announcement.transform_to_dict.return_value = {"id": 1, "title": "Updated"}

    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_announcement
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    mock_dto = MagicMock()
    mock_dto.transform.return_value = mock_announcement

    response = announcement_services.update_announcement(mock_dto, 1)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200

@patch("services.announcement_services.init_db", autospec=True)
def test_update_announcement_not_found(mock_init_db):
    logger.info("Testing update_announcement with invalid ID=999")

    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = None
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    mock_dto = MagicMock()
    response = announcement_services.update_announcement(mock_dto, 999)

    logger.info(f"Expected: 404 Not Found; Got: {response.status_code}")
    assert response.status_code == 404

# -------------------------
# delete_announcement
# -------------------------
@patch("services.announcement_services.init_db", autospec=True)
def test_delete_announcement_found(mock_init_db):
    logger.info("Testing delete_announcement with valid ID=1")

    mock_session = MagicMock()
    mock_announcement = MagicMock()
    mock_announcement.transform_to_dict.return_value = {"id": 1, "title": "Deleted"}

    mock_session.query.return_value.filter.return_value.first.return_value = mock_announcement
    mock_init_db.return_value = mock_session

    response = announcement_services.delete_announcement(1)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200

@patch("services.announcement_services.init_db", autospec=True)
def test_delete_announcement_not_found(mock_init_db):
    logger.info("Testing delete_announcement with invalid ID=999")

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_init_db.return_value = mock_session

    response = announcement_services.delete_announcement(999)

    logger.info(f"Expected: 404 Not Found; Got: {response.status_code}")
    assert response.status_code == 404