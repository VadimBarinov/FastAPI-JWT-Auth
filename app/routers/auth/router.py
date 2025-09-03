from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import (
    HTTPBearer
)

from .dependencies import (
    ValidateAuthUser,
    AddNewUser
)
from .auth_helpers import (
    create_access_token,
    create_refresh_token
)
from .schemas import (
    TokenInfo,
    SUserGet
)
from .validation import (
    CurrentAuthUserForRefresh,
    CurrentAuthActiveUser
)


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/auth",
    tags=["Авторизация пользователей", ],
    dependencies=[Depends(http_bearer), ],
)


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
