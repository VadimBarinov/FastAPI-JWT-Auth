from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer
)

from app.dependencies import AsyncSessionDep
from app.routers.auth.dao import UserDAO
from app.routers.auth.dependencies import (
    ValidateAuthUser,
    AddNewUser
)
from app.routers.auth.auth_helpers import (
    create_access_token,
    create_refresh_token
)
from app.routers.auth.schemas import (
    TokenInfo,
    SUserGet
)
from app.routers.auth.validation import (
    CurrentAuthUserForRefresh,
    CurrentAuthActiveUser
)

# Так можно получить токен из заголовка
# auto_error=False чтобы не выпадала ошибка в случае, когда токен не указан
http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/auth",
    tags=["Авторизация пользователей", ],
    # В каждом запросе будет ожидаться токен
    # Нужно для проверки типа токена
    dependencies=[Depends(http_bearer), ],
)

# Basic авторизация в URL встраивается имя пользователя и пароль
security = HTTPBasic()


@router.get("/basic_auth/", summary="Basic авторизация")
async def basic_auth_credentials(
        session: AsyncSessionDep,
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> dict:
    """
    # Базовый алгоритм авторизации с помощью username и password
    ---
        Params:
            - username: str
            - password: str
    ---
        Returns:
            {
                "message": "Hi!",
                "username": Entered username,
                "password": Entered password,
            }
    """
    user = await UserDAO.get_user_by_username(session=session, username=credentials.username)
    if (user is None) or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя или пароль!"
        )
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }


@router.post("/register/", summary="Регистрация пользователей")
async def register_user(user_id: AddNewUser) -> dict:
    """
    # Регистрация нового пользователя и добавление его в БД
    ---
        Params:
            - username: str
            - email: EmailStr
            - password: str
    ---
        Returns:
            {
                "message": "Пользователь с ID ... зарегистрирован!"
            }
    """
    return {"message": f"Пользователь с ID {user_id} зарегистрирован!"}


@router.post("/login/", summary="Авторизация пользователя")
async def auth_user(user: ValidateAuthUser) -> TokenInfo:
    """
    # Авторизация пользователя (выдача access токена)
    ---
        Params:
            - username: str
            - password: str
            - client_id: optional field
            - client_secret: optional field
    ---
        Returns:
            Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer",
            )
    """
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# response_model_exclude_none=True
# не указывает поля, если они равны None
@router.post("/refresh/", response_model_exclude_none=True, summary="Refresh access токен")
async def refresh_auth_jwt(user: CurrentAuthUserForRefresh) -> TokenInfo:
    """
    # Refresh access токена
    ---
        Params:
            - refresh_token: header_field
    ---
        Returns:
            Token(
                access_token=access_token,
                token_type="Bearer",
            )
    """
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token
    )


@router.get("/me/", summary="Получить информацию о себе")
async def auth_user_check_self_info(user: CurrentAuthActiveUser) -> SUserGet:
    """
    # Получение информации о себе (по переданному токену в заголовке запроса)
    ---
        Params:
            - access_token: header field
    ---
        Returns:
            {
              "id": User ID,
              "username": Username,
              "email": User E-mail,
              "password": User password,
              "active": Active or unactive
            }
    """
    return user
