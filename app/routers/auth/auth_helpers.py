from datetime import timedelta

from core.config import settings
from .auth_utils import encode_jwt
from .schemas import SUserGet


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
        token_type: str,
        token_data: dict,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    """Создание payload токена"""
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    token: str = encode_jwt(
        payload=jwt_payload,
        expire_timedelta=expire_timedelta,
        expire_minutes=expire_minutes,
    )
    return token


def create_access_token(user: SUserGet) -> str:
    """Создание токена для переданного пользователя"""
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(user: SUserGet) -> str:
    """Создание refresh токена"""
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.REFRESH_TOKEN_EXPIRE_DAYS),
    )
