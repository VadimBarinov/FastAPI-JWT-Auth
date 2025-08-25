from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from app.dependencies import AsyncSessionDep
from app.routers.users.auth import decode_jwt
from app.routers.users.dao import UserDAO
from app.routers.users.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.routers.users.schemas import SUserGet


oath2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")


def get_current_token_payload(
        token: Annotated[str, Depends(oath2_scheme)]
) -> dict:
    """Получение token payload"""
    try:
        # Декодирование JWT
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не валидный!"
        )
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    """Валидауия типа токена"""
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Неверный тип токена {current_token_type!r}, ожидался {token_type!r}"
        )


async def get_current_auth_user(
        session: AsyncSessionDep,
        payload: Annotated[dict, Depends(get_current_token_payload)],
) -> SUserGet:
    """Получение пользователя по данным из токена"""
    validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    # Получение username из поля subject токена
    username: str | None = payload.get("sub")
    # Получение пользователя из БД
    user = await UserDAO.get_user_by_username(session=session, username=username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен не валидный!"
    )


async def get_current_auth_user_for_refresh(
        session: AsyncSessionDep,
        payload: Annotated[dict, Depends(get_current_token_payload)],
) -> SUserGet:
    """Получение пользователя по данным из refresh токена"""
    validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    username: str | None = payload.get("sub")
    # Получение пользователя из БД
    user = await UserDAO.get_user_by_username(session=session, username=username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен не валидный!"
    )
