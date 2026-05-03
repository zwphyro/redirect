from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.redirect_link.models import RedirectLink


class RedirectLinkRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list(
        self,
        user_id: int,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ):
        query = (
            select(RedirectLink)
            .where(RedirectLink.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(query)

        return result.scalars().all()

    async def get_by_short_code(self, short_code: str, user_id: int):
        query = select(RedirectLink).where(
            RedirectLink.short_code == short_code, RedirectLink.user_id == user_id
        )
        result = await self._session.execute(query)

        return result.scalars().first()

    async def create(self, short_code: str, target_url: str, user_id: int):
        link = RedirectLink(
            short_code=short_code, target_url=target_url, user_id=user_id
        )
        self._session.add(link)

        return link

    async def delete_by_short_code(self, short_code: str, user_id: int):
        query = (
            delete(RedirectLink)
            .where(
                RedirectLink.short_code == short_code,
                RedirectLink.user_id == user_id,
            )
            .returning(RedirectLink)
        )
        result = await self._session.execute(query)
        return result.scalars().first()
