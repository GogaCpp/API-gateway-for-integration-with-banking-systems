from .router import router as v1_router

from fastapi import APIRouter

router = APIRouter(prefix="/v1")
router.include_router(v1_router)
