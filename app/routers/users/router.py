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


security = HTTPBasic()
@router.get("/basic_auth/", summary="Basic авторизация")
async def basic_auth_credentials(
    session: AsyncSessionDep,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> dict:
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
    return {"message": f"Пользователь с ID {user_id} зарегистрирован!"}


@router.post("/login/", summary="Авторизация пользователя")
async def auth_user(user: ValidateAuthUser) -> Token:
    jwt_payload = {
        "sub": user.username,
        "email": user.email,
    }
    access_token = AuthSystem.encode_jwt(payload=jwt_payload)
    return Token(
        access_token=access_token,
        token_type="Bearer",
    )


@router.get("/me/", summary="Получить информацию о себе")
async def auth_user_check_self_info(user: CurrentActiveUser) -> SUserGet:
    return user
