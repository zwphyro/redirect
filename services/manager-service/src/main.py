from fastapi import FastAPI, HTTPException, status
from sqlalchemy.exc import NoResultFound

from src.api import router

app = FastAPI(
    title="Redirect URLs Management API",
    root_path="/api/v1",
)


@app.exception_handler(NoResultFound)
def not_found_exception_handler(*_):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found"
    )


app.include_router(router)
