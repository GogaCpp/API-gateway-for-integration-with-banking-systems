from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import timedelta

from src.services.jwt import create_access_token, decode_token
from src.services.users import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends()
):
    user = await user_service.auth_user(form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(data={"sub": user.name}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


# Защищённый маршрут
@router.get("/protected/")
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = await decode_token(token)
    print(payload)
    if payload is None:
        raise HTTPException(status_code=401, detail="Неверный токен или срок действия истёк")

    return {"msg": f"Добро пожаловать!{payload}"}


@router.get("/")
async def read_root():
    return {"message": "Добро пожаловать в наше приложение!"}
