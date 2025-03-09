from fastapi import APIRouter, UploadFile
from src.api.v1.users import router as user_router

router = APIRouter(prefix="/dbo", tags=["DBO"])
router.include_router(user_router)

@router.post("/download_document")
async def download_document(
    file: UploadFile,
):
    ...