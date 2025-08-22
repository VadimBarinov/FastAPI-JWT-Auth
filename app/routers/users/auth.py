from datetime import timedelta, datetime, timezone

import jwt
import bcrypt

from app.core.config import settings


class AuthSystem:

    auth_data = settings.auth_jwt

    @staticmethod
    def encode_jwt(
            payload: dict,
            private_key: str = auth_data.PRIVATE_KEY_PATH.read_text(),
            algorithm: str = auth_data.ALGORITHM,
            expire_timedelta: timedelta | None = None,
            expire_minutes: int = settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
    ):
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(exp=expire, iat=now)
        encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
        return encoded

    @staticmethod
    def decode_jwt(
            token: str | bytes,
            public_key: str = auth_data.PUBLIC_KEY_PATH.read_text(),
            algorithm: str = auth_data.ALGORITHM,
    ):
        decoded = jwt.decode(jwt=token, key=public_key, algorithms=algorithm)
        return decoded

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(password=pwd_bytes, salt=salt)

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )