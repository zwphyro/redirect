from fastapi import APIRouter
from src.redirect_url.routes import router as redirect_url_router

router = APIRouter()

router.include_router(redirect_url_router, prefix="/redirects")
