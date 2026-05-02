from src.redirect_link.short_code import ShortCodeGenerator
from src.unit_of_work import UnitOfWork
from src.exceptions import DatabaseError, NotFoundError


class RedirectLinkService:
    def __init__(
        self,
        uow: UnitOfWork,
        short_code_generator: ShortCodeGenerator,
    ):
        self._uow = uow
        self._short_code_generator = short_code_generator

    async def list(
        self, user_id: int, *, limit: int | None = None, offset: int | None = None
    ):
        return await self._uow.redirect_link.list(user_id, limit=limit, offset=offset)

    async def get_link(self, short_code: str, user_id: int):
        link = await self._uow.redirect_link.get_by_short_code(short_code, user_id)

        if link is None:
            raise NotFoundError("Redirect link not found")

        return link

    async def create_link(self, target_url: str, user_id: int):
        max_attempts = 10

        for _ in range(max_attempts):
            try:
                short_code = self._short_code_generator.generate()
                link = await self._uow.redirect_link.create(
                    short_code,
                    target_url,
                    user_id,
                )
                await self._uow.commit()

                return link
            except DatabaseError:
                await self._uow.rollback()
                continue

        raise RuntimeError("Failed to generate unique short code")

    async def delete_link(self, short_code: str, user_id: int):
        link = await self._uow.redirect_link.delete_by_short_code(short_code, user_id)

        if link is None:
            raise NotFoundError("Redirect link not found")

        await self._uow.commit()

        return link

    async def toggle_active(self, short_code: str, user_id: int):
        link = await self._uow.redirect_link.get_by_short_code(short_code, user_id)

        if link is None:
            raise NotFoundError("Redirect link not found")

        link.is_active = not link.is_active

        await self._uow.commit()
        return link
