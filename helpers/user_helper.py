from hashlib import sha256


def hash_password_SHA256(password: str):
    return sha256(password.encode('utf-8')).hexdigest()


def validate_password(hashed_password: str, password_string: str) -> bool:
    return hashed_password == hash_password_SHA256(password_string)
