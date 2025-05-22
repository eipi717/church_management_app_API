import logging
from DTOs.userDTO import UserDTO
from models.user_model import User
from pydantic import ValidationError
import pytest

logger = logging.getLogger(__name__)


def test_user_dto_initialization_minimal():
    logger.info("Testing UserDTO minimal initialization...")

    dto = UserDTO(username="admin", password="securepass123")

    assert dto.username == "admin"
    assert dto.password == "securepass123"
    assert dto.status is None
    assert dto.role is None
    assert dto.first_name is None
    assert dto.last_name is None

    logger.info("Minimal initialization passed.")


def test_user_dto_initialization_full():
    logger.info("Testing UserDTO full initialization...")

    dto = UserDTO(
        username="johndoe",
        password="secret",
        status=True,
        role="admin",
        first_name="John",
        last_name="Doe"
    )

    assert dto.username == "johndoe"
    assert dto.password == "secret"
    assert dto.status is True
    assert dto.role == "admin"
    assert dto.first_name == "John"
    assert dto.last_name == "Doe"

    logger.info("Full initialization passed.")


def test_user_dto_transform_to_model():
    logger.info("Testing UserDTO.transform() to User model...")

    dto = UserDTO(
        username="janedoe",
        password="password123",
        role="user",
        status=False,
        first_name="Jane",
        last_name="Doe"
    )

    user: User = dto.transform()

    assert isinstance(user, User)
    assert user.user_username == "janedoe"
    assert user.user_status is False
    assert user.user_role == "user"
    assert user.user_first_name == "Jane"
    assert user.user_last_name == "Doe"
    assert user.user_password_hash is not None

    logger.info("Transformation to User model passed.")


def test_user_dto_validation_error():
    logger.info("Testing UserDTO with invalid data...")

    with pytest.raises(ValidationError) as exc_info:
        UserDTO(username="")

    assert "password" in str(exc_info.value)