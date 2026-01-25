from fastapi import FastAPI

from src.api import router

app = FastAPI(
    title="Redirect URLs Management API",
    root_path="/api/v1",
)

app.include_router(router)
