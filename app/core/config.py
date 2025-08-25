from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

class AuthJWT(BaseSettings):
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    model_config = SettingsConfigDict(
        env_file = BASE_DIR / ".env"
    )


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    db_url: str = (f"postgresql+asyncpg://{db.DB_USER}:{db.DB_PASSWORD}@"
                   f"{db.DB_HOST}:{db.DB_PORT}/{db.DB_NAME}")
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
