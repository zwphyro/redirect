from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from src.dependencies import DBDependency
from src.exceptions import NotFoundException
from src.redirect_url.models import RedirectURL

from random import choice

# TODO: implement repository/dao to access database


class RedirectURLService:
    def __init__(self, session: DBDependency):
        self.session = session

    async def list(self, *, limit: int | None = None, offset: int | None = None):
        query = select(RedirectURL).limit(limit).offset(offset)
        result = await self.session.execute(query)

        redirects = result.scalars().all()
        return redirects

    async def get_redirect(self, short_code: str):
        query = select(RedirectURL).where(RedirectURL.short_code == short_code)
        result = await self.session.execute(query)

        try:
            redirect = result.scalars().one()
        except NoResultFound:
            raise NotFoundException("Redirect URL not found")

        return redirect

    async def create_redirect(self, original_url: str):
        # TODO: improve short code generation and collision handling
        while True:
            try:
                short_code = self._generate_short_code()
                redirect = RedirectURL(short_code=short_code, original_url=original_url)

                self.session.add(redirect)
                await self.session.commit()

            except IntegrityError:
                await self.session.rollback()
                continue

            return redirect

    async def delete_redirect(self, short_code: str):
        query = select(RedirectURL).where(RedirectURL.short_code == short_code)
        result = await self.session.execute(query)

        try:
            redirect = result.scalars().one()
        except NoResultFound:
            raise NotFoundException("Redirect URL not found")

        await self.session.delete(redirect)
        await self.session.commit()

        return redirect

    async def toggle_active(self, short_code: str):
        query = select(RedirectURL).where(RedirectURL.short_code == short_code)
        result = await self.session.execute(query)

        try:
            redirect = result.scalars().one()
        except NoResultFound:
            raise NotFoundException("Redirect URL not found")

        redirect.is_active = not redirect.is_active

        await self.session.commit()

        return redirect

    def _generate_short_code(self):
        code_length = 6

        symbols = "".join(
            "".join(chr(code) for code in range(ord(start), ord(end) + 1))
            for start, end in [("a", "z"), ("A", "Z"), ("0", "9")]
        )

        return "".join(choice(symbols) for _ in range(code_length))
