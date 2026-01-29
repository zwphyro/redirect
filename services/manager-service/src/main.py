from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.api import router
from src.exceptions import NotFoundException

app = FastAPI(
    title="Redirect URLs Management API",
    root_path="/api/v1",
)


@app.exception_handler(NotFoundException)
def not_found_exception_handler(_, exception: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exception)},
    )


app.include_router(router)
