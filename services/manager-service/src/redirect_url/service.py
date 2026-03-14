from src.redirect_url.short_code import ShortCodeGenerator
from src.unit_of_work import UnitOfWork
from src.exceptions import DatabaseError


class RedirectURLService:
    def __init__(
        self,
        uow: UnitOfWork,
        short_code_generator: ShortCodeGenerator,
    ):
        self._uow = uow
        self._short_code_generator = short_code_generator

    async def list(self, *, limit: int | None = None, offset: int | None = None):
        return await self._uow.redirect_url.list(limit=limit, offset=offset)

    async def get_redirect(self, short_code: str):
        return await self._uow.redirect_url.get_by_short_code(short_code)

    async def create_redirect(self, original_url: str):
        max_attempts = 10

        for _ in range(max_attempts):
            try:
                short_code = self._short_code_generator.generate()
                redirect = await self._uow.redirect_url.create(
                    short_code=short_code,
                    original_url=original_url,
                )
                await self._uow.commit()
                return redirect
            except DatabaseError:
                await self._uow.rollback()
                continue

        raise RuntimeError("Failed to generate unique short code")

    async def delete_redirect(self, short_code: str):
        redirect = await self._uow.redirect_url.delete(short_code)
        await self._uow.commit()
        return redirect

    async def toggle_active(self, short_code: str):
        redirect = await self._uow.redirect_url.toggle_active(short_code)
        await self._uow.commit()
        return redirect
