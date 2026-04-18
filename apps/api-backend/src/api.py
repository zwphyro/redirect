from fastapi import APIRouter
from src.redirect_link.routes import router as redirect_link_router

router = APIRouter()

router.include_router(redirect_link_router, prefix="/redirect_links")
