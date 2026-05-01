from fastapi import status

from src.exception_registry import ExceptionRegistry


@ExceptionRegistry.register(status.HTTP_404_NOT_FOUND)
class NotFoundError(Exception): ...


@ExceptionRegistry.register(status.HTTP_500_INTERNAL_SERVER_ERROR)
class DatabaseError(Exception): ...
