from fastapi import APIRouter, UploadFile


router = APIRouter(prefix="/dbo", tags=["DBO"])


@router.post("/download_document")
async def download_document(
    file: UploadFile,
):
    ...