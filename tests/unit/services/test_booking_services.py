import logging
from unittest.mock import patch, MagicMock
from services import booking_services

logger = logging.getLogger(__name__)

# -------------------------
# get_booking_list
# -------------------------
@patch("services.booking_services.init_db", autospec=True)
def test_get_booking_list(mock_init_db):
    logger.info("Testing get_booking_list with is_canceled=False, page=1, number_of_records=10")

    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_booking = MagicMock()
    mock_booking.transform_to_dict.return_value = {"id": 1, "status": "active"}

    mock_query.offset.return_value.limit.return_value.all.return_value = [mock_booking]
    mock_session.query.return_value.filter.return_value = mock_query
    mock_init_db.return_value = mock_session

    response = booking_services.get_booking_list(is_canceled=False, page=1, number_of_records=10)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200


# -------------------------
# get_booking_by_user_id
# -------------------------
@patch("services.booking_services.init_db", autospec=True)
def test_get_booking_by_user_id_found(mock_init_db):
    logger.info("Testing get_booking_by_user_id with valid user_id=1")

    mock_booking = MagicMock()
    mock_booking.transform_to_dict.return_value = {"user_id": 1, "status": "booked"}

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_booking
    mock_init_db.return_value = mock_session

    response = booking_services.get_booking_by_user_id(1)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200


@patch("services.booking_services.init_db", autospec=True)
def test_get_booking_by_user_id_not_found(mock_init_db):
    logger.info("Testing get_booking_by_user_id with invalid user_id=999")

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_init_db.return_value = mock_session

    response = booking_services.get_booking_by_user_id(999)

    logger.info(f"Expected: 404 Not Found; Got: {response.status_code}")
    assert response.status_code == 404


# -------------------------
# get_booking_by_room_id
# -------------------------
@patch("services.booking_services.init_db", autospec=True)
def test_get_booking_by_room_id_found(mock_init_db):
    logger.info("Testing get_booking_by_room_id with valid room_id=1")

    mock_booking = MagicMock()
    mock_booking.transform_to_dict.return_value = {"room_id": 1, "status": "booked"}

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_booking
    mock_init_db.return_value = mock_session

    response = booking_services.get_booking_by_room_id(1)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200


@patch("services.booking_services.init_db", autospec=True)
def test_get_booking_by_room_id_not_found(mock_init_db):
    logger.info("Testing get_booking_by_room_id with invalid room_id=999")

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_init_db.return_value = mock_session

    response = booking_services.get_booking_by_room_id(999)

    logger.info(f"Expected: 404 Not Found; Got: {response.status_code}")
    assert response.status_code == 404


# -------------------------
# create_booking
# -------------------------
@patch("services.booking_services.init_db", autospec=True)
def test_create_booking(mock_init_db):
    logger.info("Testing create_booking with valid BookingDTO")

    mock_session = MagicMock()
    mock_booking = MagicMock()
    mock_booking.transform_to_dict.return_value = {"id": 1, "status": "created"}

    mock_dto = MagicMock()
    mock_dto.transform.return_value = mock_booking

    mock_init_db.return_value = mock_session

    response = booking_services.create_booking(mock_dto)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200


# -------------------------
# cancel_booking
# -------------------------
@patch("services.booking_services.init_db", autospec=True)
def test_cancel_booking(mock_init_db):
    logger.info("Testing cancel_booking with valid booking_id=1")

    mock_booking = MagicMock()
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = mock_booking
    mock_init_db.return_value = mock_session

    response = booking_services.cancel_booking(1)

    logger.info(f"Expected: 200 OK; Got: {response.status_code}")
    assert response.status_code == 200