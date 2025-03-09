from fastapi import APIRouter
from .abc import router as abc_router
from .dbo import router as dbo_router
from .cm import router as cm_router
from .auth import router as auth_router

router = APIRouter()
router.include_router(abc_router)
router.include_router(dbo_router)
router.include_router(cm_router)
router.include_router(auth_router)