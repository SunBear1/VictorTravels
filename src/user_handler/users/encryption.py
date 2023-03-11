import hashlib

import jwt

from users.exceptions import UserWrongTokenSchemaException

JWT_SECRET = "TAJNY_SEKRET"


def hash_password(password) -> str:
    """
    Hash password with SHA256
    :param password: user password to be hashed
    :return: hashed user password
    """
    password_bytes = password.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(password_bytes)
    hashed_password = sha256.hexdigest()
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(password_bytes)
    hashed_input_password = sha256.hexdigest()
    if hashed_input_password == hashed_password:
        return True
    else:
        return False


def verify_jwt_token(token: str) -> dict[str, str]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except jwt.exceptions.InvalidSignatureError:
        raise UserWrongTokenSchemaException(message="Wrong token signature")
    except jwt.exceptions.DecodeError:
        raise UserWrongTokenSchemaException(message="Cant decode token")
