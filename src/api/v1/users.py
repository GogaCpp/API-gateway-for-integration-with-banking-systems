from fastapi import APIRouter


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def get_list(
):
    ...


@router.get("/{user_id}")
async def get_user(
    user_id: int
):
    ...


@router.post("/")
async def create_user(
):
    ...


@router.patch("/")
async def update_user(
):
    ...


@router.delete("/{user_id}")
async def delete_user(
    user_id: int
):
    ...
