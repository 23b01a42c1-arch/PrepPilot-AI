from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )