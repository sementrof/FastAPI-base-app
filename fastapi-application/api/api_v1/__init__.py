from fastapi import APIRouter

from core.config import settings

from .hotel import router as users_router
from .view_base import router as viev_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)

router.include_router(
    viev_router,
    prefix="",
)
