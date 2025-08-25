from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.dependencies import AsyncSessionDep
from app.routers.users.dao import UserDAO
from app.routers.users.dependencies import ValidateAuthUser, AddNewUser, CurrentActiveUser
from app.routers.users.schemas import SUserGet, Token
from app.routers.users.auth import AuthSystem


router = APIRouter(
    prefix="/users",
    tags=["Авторизация пользователей",],
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
async def auth_user(user: ValidateAuthUser) -> Token:
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
                token_type="Bearer",
            )
    """
    access_token = AuthSystem.create_access_token(user)
    return Token(
        access_token=access_token,
        token_type="Bearer",
    )


@router.get("/me/", summary="Получить информацию о себе")
async def auth_user_check_self_info(user: CurrentActiveUser) -> SUserGet:
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
