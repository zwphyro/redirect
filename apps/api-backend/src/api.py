from fastapi import APIRouter
from src.redirect_link.routes import router as redirect_link_router
from src.auth.routes import router as auth_router

router = APIRouter()

router.include_router(redirect_link_router, prefix="/redirect_links")
router.include_router(auth_router, prefix="/auth")
