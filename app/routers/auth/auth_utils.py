import uuid
from datetime import timedelta, datetime, timezone
import jwt
import bcrypt

from core.config import settings


auth_data = settings.auth_jwt


def encode_jwt(
        payload: dict,
        private_key: str = auth_data.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = auth_data.ALGORITHM,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    """Своя обертка для шифрования JWT"""
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        # Если указан срок действия токена
        expire = now + expire_timedelta
    else:
        # Иначе используется константа ACCESS_TOKEN_EXPIRE_MINUTES из настроек
        expire = now + timedelta(minutes=expire_minutes)
    # Добавление новый полей в payload
    to_encode.update(
        exp=expire,
        iat=now,
        # JSON Token Identifier
        jti=str(uuid.uuid4()),
    )
    encoded: str = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = auth_data.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = auth_data.ALGORITHM,
) -> dict:
    """Своя обертка для расшифровки JWT"""
    decoded: dict = jwt.decode(jwt=token, key=public_key, algorithms=algorithm)
    return decoded


def hash_password(password: str) -> bytes:
    """Хэширование пароля"""
    # Добавление соли
    salt = bcrypt.gensalt()
    # Кодирование пароля в байты
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    """Валидация введенного пароля"""
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
