from typing import Annotated

from fastapi import (
    Depends,
    HTTPException
)
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from app.dependencies import AsyncSessionDep
from app.routers.auth.auth_utils import decode_jwt
from app.routers.auth.auth_helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE
)
from app.routers.auth.dao import UserDAO
from app.routers.auth.schemas import SUserGet

oath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


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


async def get_user_by_token_subject(session: AsyncSession, payload: dict) -> SUserGet:
    """Получение пользователя по token payload sub"""
    username: str | None = payload.get("sub")
    # Получение пользователя из БД
    user = await UserDAO.get_user_by_username(session=session, username=username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен не валидный!"
    )


class UserGetterFromToken:
    """Класс для получения пользователя по информации из токена"""
    def __init__(
            self,
            token_type: str
    ):
        self.token_type = token_type

    async def __call__(
            self,
            session: AsyncSessionDep,
            payload: Annotated[dict, Depends(get_current_token_payload)]
    ) -> SUserGet:
        validate_token_type(payload=payload, token_type=self.token_type)
        # Получение username из поля subject токена
        return await get_user_by_token_subject(session=session, payload=payload)


CurrentAuthUser: type[SUserGet] = Annotated[SUserGet, Depends(UserGetterFromToken(token_type=ACCESS_TOKEN_TYPE))]
CurrentAuthUserForRefresh: type[SUserGet] = Annotated[SUserGet, Depends(UserGetterFromToken(token_type=REFRESH_TOKEN_TYPE))]


async def get_current_auth_active_user(user: CurrentAuthUser) -> SUserGet:
    """Получение активного пользователя"""
    if user.active:
        # Если пользователь активен, то пользователь возвращается в качестве ответа
        return user
    # Иначе выброс ошибки о неактивном пользователе
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неактивный пользователь!")


CurrentAuthActiveUser: type[SUserGet] = Annotated[SUserGet, Depends(get_current_auth_active_user)]
