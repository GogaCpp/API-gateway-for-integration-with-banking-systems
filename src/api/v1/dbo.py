from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from src.api.v1.users import router as user_router
from src.database import get_s3_client
from src.services.jwt import permission_checker
from src.config import oauth2_scheme, settings

router = APIRouter(prefix="/dbo", tags=["DBO"])
router.include_router(user_router)


@router.post("/download_document")
async def download_document(
    file: UploadFile = File(),
    s3_client=Depends(get_s3_client),
    token: str = Depends(oauth2_scheme)
):
    await permission_checker(token, 1)
    s3_object_name = f"uploads/{file.filename}"
    try:
        contents = await file.read()
        try:
            await s3_client.head_bucket(Bucket=settings.s3_bucket_name)
        except s3_client.exceptions.ClientError:
            await s3_client.create_bucket(Bucket=settings.s3_bucket_name)
        await s3_client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_object_name,
            Body=contents
        )
        return {
                "filename": file.filename,
                "s3_path": s3_object_name,
                "bucket": settings.s3_bucket_name,
                "message": "File uploaded successfully"
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )
    finally:
        await file.close()


@router.get("/download-url/{file_name}")
async def get_download_url(
    file_name: str,
    expires_in: int = 3600,
    s3_client=Depends(get_s3_client),
    token: str = Depends(oauth2_scheme)
):
    await permission_checker(token, 1)
    s3_object_name = f"uploads/{file_name}"

    try:
        try:
            await s3_client.head_object(Bucket=settings.s3_bucket_name, Key=s3_object_name)
        except s3_client.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise HTTPException(status_code=404, detail="File not found")
            else:
                raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")

        download_url = await s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.s3_bucket_name,
                "Key": s3_object_name
            },
            ExpiresIn=expires_in
        )

        return {
            "download_url": download_url,
            "expires_in": expires_in
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating download URL: {str(e)}"
        )


@router.delete("/delete/{file_name}")
async def delete_file_from_s3(
    file_name: str,
    s3_client=Depends(get_s3_client),
    token: str = Depends(oauth2_scheme)
):
    await permission_checker(token, 1)

    s3_object_name = f"uploads/{file_name}"

    try:

        try:
            await s3_client.head_object(Bucket=settings.s3_bucket_name, Key=s3_object_name)
        except s3_client.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                raise HTTPException(status_code=404, detail="File not found")
            else:
                raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")

        await s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=s3_object_name)

        return {
            "message": f"File {file_name} deleted successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting file: {str(e)}"
        )
