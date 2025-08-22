from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError

from app.dependencies import AsyncSessionDep
from app.routers.users.dao import UserDAO
from app.routers.users.schemas import SUserGet, SUserAdd
from app.routers.users.auth import AuthSystem


async def validate_auth_user(
        session: AsyncSessionDep,
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> SUserGet:
    unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя или пароль!"
    )
    user: SUserGet = await UserDAO.get_user_by_username(session=session, username=user_data.username)
    if not user:
        raise unauthed_exc
    if not AuthSystem.validate_password(
            password=user_data.password,
            hashed_password=user.password.encode(),
    ):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь неактивен!"
        )
    return user

ValidateAuthUser: type[SUserGet] = Annotated[SUserGet, Depends(validate_auth_user)]


async def add_new_user(session: AsyncSessionDep, user_data: Annotated[SUserAdd, Depends()]) -> int:
    find_users = await UserDAO.get_user_by_username_and_email(
        session=session,
        username=user_data.username,
        email=user_data.email,
    )
    if find_users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким именем или почтой уже существует!"
        )
    user_result = user_data.model_dump()
    user_result["password"] = AuthSystem.hash_password(user_data.password).decode()
    result = await UserDAO.add_user(
        session=session,
        username=user_result["username"],
        email=user_result["email"],
        password=user_result["password"],
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь не зарегистрирован!"
        )
    return result

AddNewUser: type[int] = Annotated[int, Depends(add_new_user)]


# Так можно получить токен из заголовка
# http_bearer = HttpBearer()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

async def get_current_token_payload(
        token: Annotated[str, Depends(oath2_scheme)]
) -> dict:
    try:
        payload = AuthSystem.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не валидный!"
        )
    return payload

CurrentUserTokenPayload: type[dict] = Annotated[dict, Depends(get_current_token_payload)]


async def get_current_user(
        session: AsyncSessionDep,
        payload: CurrentUserTokenPayload,
) -> SUserGet:
    username: str | None = payload.get("sub")
    user = await UserDAO.get_user_by_username(session=session, username=username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен не валидный!"
    )

CurrentUser: type[SUserGet] = Annotated[SUserGet, Depends(get_current_user)]


async def get_current_active_user(user: CurrentUser) -> SUserGet:
    if user.active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неактивный пользователь!")

CurrentActiveUser: type[SUserGet] = Annotated[SUserGet, Depends(get_current_active_user)]