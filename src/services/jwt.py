from typing import Any
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.config import settings
from fastapi import HTTPException, status


async def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


async def permission_checker(token, security_level) -> bool:
    data = await decode_token(token)
    
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_role = data.get("role")
    if user_role < security_level:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)