from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

from src.api import router

app = FastAPI(
    title="Redirect URLs Management API",
    root_path="/api/v1",
)


@app.exception_handler(NoResultFound)
def not_found_exception_handler(*_):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Not found"},
    )


app.include_router(router)
