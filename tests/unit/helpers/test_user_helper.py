from helpers.user_helper import hash_password_SHA256, validate_password

def test_hash_password_SHA256_returns_expected_hash():
    password = "mySecurePassword"
    expected = hash_password_SHA256(password)
    assert expected == hash_password_SHA256(password)  # Consistency check
    assert isinstance(expected, str)
    assert len(expected) == 64  # SHA-256 produces 64-character hex digest

def test_validate_password_returns_true_on_correct_password():
    password = "correctPassword"
    hashed = hash_password_SHA256(password)
    assert validate_password(hashed, password) is True

def test_validate_password_returns_false_on_incorrect_password():
    password = "correctPassword"
    wrong_password = "wrongPassword"
    hashed = hash_password_SHA256(password)
    assert validate_password(hashed, wrong_password) is False