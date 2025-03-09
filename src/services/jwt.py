from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.config import settings
# Секретный ключ для подписи токенов
SECRET_KEY = "Yx5Js7OCS6dD4b4Hfy3Ldi6Y3idY9S00199uIIvP0MU"
ALGORITHM = "HS256"  # Алгоритм подписи
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена


# Функция для создания JWT-токена
async def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})  # Добавляем время истечения
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Функция для проверки токена
async def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None  # Если токен недействителен или истёк