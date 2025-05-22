import logging
from unittest.mock import patch, MagicMock
from services import room_services

logger = logging.getLogger(__name__)

# -------------------------
# get_rooms_list
# -------------------------
@patch("services.room_services.init_db", autospec=True)
def test_get_rooms_list(mock_init_db):
    logger.info("Testing get_rooms_list with page=1 and number_of_records=5")

    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_room = MagicMock()
    mock_room.transform_to_dict.return_value = {"room_id": 1, "name": "Room A"}

    mock_query.offset.return_value.limit.return_value.all.return_value = [mock_room]
    mock_session.query.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = room_services.get_rooms_list(page=1, number_of_records=5)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200
    assert b"Room A" in response.body


# -------------------------
# inactive_room - room found
# -------------------------
@patch("services.room_services.init_db", autospec=True)
def test_inactive_room_found(mock_init_db):
    logger.info("Testing inactive_room with valid room_id=1")

    mock_room = MagicMock()
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_room
    mock_init_db.return_value = mock_session

    room_services.inactive_room(room_id=1)

    logger.info("Expected: session.commit() called")
    assert mock_room.room_is_booked is False
    mock_session.commit.assert_called_once()


# -------------------------
# inactive_room - room not found
# -------------------------
@patch("services.room_services.init_db", autospec=True)
def test_inactive_room_not_found(mock_init_db):
    logger.info("Testing inactive_room with invalid room_id=999 (room not found)")

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_init_db.return_value = mock_session

    # Should not raise exception even if room not found
    room_services.inactive_room(room_id=999)

    logger.info("Expected: no commit called")
    mock_session.commit.assert_not_called()