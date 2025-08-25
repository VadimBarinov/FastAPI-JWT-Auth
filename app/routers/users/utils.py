from typing import Annotated
from fastapi import HTTPException, status, Depends, Form

from app.dependencies import AsyncSessionDep
from app.routers.users.dao import UserDAO
from app.routers.users.schemas import SUserGet, SUserAdd
from app.routers.users.auth import hash_password, validate_password
from app.routers.users.validation import get_current_auth_user


async def validate_auth_user(
        session: AsyncSessionDep,
        username: str = Form(),
        password: str = Form(),
) -> SUserGet:
    """Валидация авторизованного пользователя"""
    unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя или пароль!"
    )
    user: SUserGet = await UserDAO.get_user_by_username(session=session, username=username)
    if not user:
        raise unauthed_exc
    if not validate_password(
            password=password,
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
    """Регистрация нового пользователя"""
    # Поиск пользователя по введенным паролям
    find_users = await UserDAO.get_user_by_username_and_email(
        session=session,
        username=user_data.username,
        email=user_data.email,
    )
    if find_users:
        # Если пользователя найдены, то выброс ошибки
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким именем или почтой уже существует!"
        )
    user_result = user_data.model_dump()
    # Хэширование введенного пароля
    user_result["password"] = hash_password(user_data.password).decode()
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


async def get_current_auth_active_user(user: Annotated[SUserGet, Depends(get_current_auth_user)]) -> SUserGet:
    """Получение активного пользователя"""
    if user.active:
        # Если пользователь активен, то пользователь возвращается в качестве ответа
        return user
    # Иначе выброс ошибки о неактивном пользователе
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неактивный пользователь!")


CurrentAuthActiveUser: type[SUserGet] = Annotated[SUserGet, Depends(get_current_auth_active_user)]