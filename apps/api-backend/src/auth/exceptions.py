from fastapi import status

from src.exception_registry import ExceptionRegistry


@ExceptionRegistry.register(status.HTTP_401_UNAUTHORIZED)
class IncorrectLoginOrPasswordError(Exception): ...


@ExceptionRegistry.register(status.HTTP_401_UNAUTHORIZED)
class InvalidPayloadError(Exception): ...


@ExceptionRegistry.register(status.HTTP_401_UNAUTHORIZED)
class TokenExpiredError(Exception): ...


@ExceptionRegistry.register(status.HTTP_401_UNAUTHORIZED)
class UserNotFoundError(Exception): ...
