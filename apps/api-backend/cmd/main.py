from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.api import router
from src.exceptions import NotFoundError, DatabaseError

app = FastAPI(
    title="Redirect URLs Management API",
    root_path="/api/v1",
)


@app.exception_handler(NotFoundError)
def not_found_exception_handler(_, exception: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exception)},
    )


@app.exception_handler(DatabaseError)
def database_exception_handler(_, exception: DatabaseError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exception)},
    )


app.include_router(router)
