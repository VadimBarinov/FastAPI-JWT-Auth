from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class SUserGet(BaseModel):
    id: int = Field(..., description="ID пользователя")
    username: str = Field(..., description="Имя пользователя, от 4 до 50 символов")
    email: EmailStr = Field(..., description="Адрес электронной почты")
    password: str = Field(..., min_length=4, max_length=255, description="Пароль, до 255 знаков")
    active: bool = Field(True, description="Активный пользователь")


class SUserAdd(BaseModel):
    username: str = Field(..., description="Имя пользователя, от 4 до 50 символов")
    email: EmailStr = Field(..., description="Адрес электронной почты")
    password: str = Field(..., min_length=4, max_length=32, description="Пароль, от 4 до 32 знаков")
