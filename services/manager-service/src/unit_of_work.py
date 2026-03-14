from typing import Type, Callable
from types import TracebackType
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import DatabaseError
from src.redirect_url.repository import RedirectURLRepository


class UnitOfWork:
    def __init__(self, session_pool: Callable[..., AsyncSession]):
        self._session_pool = session_pool

    async def __aenter__(self):
        self._session = self._session_pool()
        self.redirect_url = RedirectURLRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        if exc_type is not None:
            await self.rollback()
        await self.close()

    async def commit(self):
        try:
            await self._session.commit()
        except IntegrityError as error:
            await self.rollback()
            self._handle_integrity_error(error)

    async def flush(self):
        await self._session.flush()

    async def rollback(self):
        await self._session.rollback()

    async def close(self):
        await self._session.close()

    def _handle_integrity_error(self, error: IntegrityError):
        raise DatabaseError(f"Integrity violation: {error}")
