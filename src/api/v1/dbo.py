from fastapi import APIRouter, Depends, UploadFile
from src.api.v1.users import router as user_router
from src.services.jwt import permission_checker
from src.config import oauth2_scheme

router = APIRouter(prefix="/dbo", tags=["DBO"])
router.include_router(user_router)

@router.post("/download_document")
async def download_document(
    file: UploadFile,
    token: str = Depends(oauth2_scheme)
):
    await permission_checker(token, 1)
    ...