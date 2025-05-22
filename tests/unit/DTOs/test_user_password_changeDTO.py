import logging
import pytest
from pydantic import ValidationError
from DTOs.user_password_changeDTO import UserChangePasswordDTO

logger = logging.getLogger(__name__)


def test_user_change_password_dto_initialization():
    logger.info("Testing valid UserChangePasswordDTO initialization...")

    dto = UserChangePasswordDTO(
        user_id=1,
        old_password="oldpass123",
        new_password="newpass456"
    )

    assert dto.user_id == 1
    assert dto.old_password == "oldpass123"
    assert dto.new_password == "newpass456"

    logger.info("Initialization successful with correct data.")


def test_user_change_password_dto_invalid_types():
    logger.info("Testing UserChangePasswordDTO with invalid types...")

    with pytest.raises(ValidationError):
        # Passing a string for `user_id` which should be an int
        UserChangePasswordDTO(
            user_id="not-an-int",
            old_password="abc",
            new_password="def"
        )

    logger.info("ValidationError correctly raised for invalid types.")


def test_user_change_password_dto_empty_passwords():
    logger.info("Testing UserChangePasswordDTO with empty password strings...")

    dto = UserChangePasswordDTO(
        user_id=99,
        old_password="",
        new_password=""
    )

    assert dto.old_password == ""
    assert dto.new_password == ""

    logger.info("Empty passwords are accepted by design.")