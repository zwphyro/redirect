from fastapi import FastAPI, status
from starlette.responses import JSONResponse

from src.auth.exceptions import (
    IncorrectLoginOrPasswordError,
    InvalidPayloadError,
    TokenExpiredError,
    UserNotFoundError,
)


def register(app: FastAPI):
    exceptions = [
        IncorrectLoginOrPasswordError,
        InvalidPayloadError,
        TokenExpiredError,
        UserNotFoundError,
    ]
    status_codes = [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_401_UNAUTHORIZED,
    ]

    for exception, status_code in zip(exceptions, status_codes):

        @app.exception_handler(exception)
        def exception_handler(_, exception):
            return JSONResponse(
                status_code=status_code,
                content={"detail": str(exception)},
            )
