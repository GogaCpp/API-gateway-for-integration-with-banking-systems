import uuid
from fastapi import APIRouter, Depends, status

from src.services.users import UserService
from src.schemas.user import BaseUser, BaseUserList, UserCreatePayload, UserUpdatePayload

router = APIRouter(prefix="/user")


@router.get("/", response_model=BaseUserList)
async def get_list(
    user_service: UserService = Depends()
):
    return await user_service.get_user_list()


@router.get("/{user_id}", response_model=BaseUser)
async def get_user(
    user_id: uuid.UUID,
    user_service: UserService = Depends()
):
    return await user_service.get_user_by_id(user_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BaseUser)
async def create_user(
    user: UserCreatePayload,
    user_service: UserService = Depends()
):
    return await user_service.create_user(user)


@router.patch("/{user_id}", response_model=BaseUser)
async def update_user(
    user_id: uuid.UUID,
    user: UserUpdatePayload,
    user_service: UserService = Depends()
):
    return await user_service.update_user(user_id, user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    user_service: UserService = Depends()
):
    return await user_service.delete_user(user_id)
