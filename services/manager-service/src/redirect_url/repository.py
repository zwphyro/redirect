from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import NotFoundError
from src.redirect_url.models import RedirectURL


class RedirectURLRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[RedirectURL]:
        query = select(RedirectURL).limit(limit).offset(offset)
        result = await self._session.execute(query)

        return result.scalars().all()

    async def get_by_short_code(self, short_code: str) -> RedirectURL:
        query = select(RedirectURL).where(RedirectURL.short_code == short_code)
        result = await self._session.execute(query)

        try:
            return result.scalars().one()
        except NoResultFound as exception:
            raise NotFoundError("Redirect URL not found") from exception

    async def create(self, short_code: str, original_url: str) -> RedirectURL:
        redirect = RedirectURL(short_code=short_code, original_url=original_url)

        self._session.add(redirect)

        return redirect

    async def delete(self, short_code: str) -> RedirectURL:
        redirect = await self.get_by_short_code(short_code)

        await self._session.delete(redirect)

        return redirect

    async def toggle_active(self, short_code: str) -> RedirectURL:
        redirect = await self.get_by_short_code(short_code)

        redirect.is_active = not redirect.is_active

        return redirect
