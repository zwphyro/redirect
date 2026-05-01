from fastapi import FastAPI

from src.api import router
from src.exception_registry import ExceptionRegistry

app = FastAPI(
    title="Redirect URLs Management API",
    root_path="/api/v1",
)
app.include_router(router)
ExceptionRegistry.apply(app)
