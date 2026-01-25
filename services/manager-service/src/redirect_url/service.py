from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.redirect_url.exceptions import RedirectURLNotFoundException
from src.redirect_url.models import RedirectURL

from random import choice


async def list_redirects(session: AsyncSession):
    result = await session.execute(select(RedirectURL))
    redirects = result.scalars().all()
    return redirects


async def get_redirect(short_code: str, session: AsyncSession):
    query = select(RedirectURL).where(RedirectURL.short_code == short_code)
    result = await session.execute(query)

    redirect = result.scalars().first()

    if redirect is None:
        raise RedirectURLNotFoundException

    return redirect


def generate_short_code():
    code_length = 6
    symbols = (
        "".join(chr(code) for code in range(ord("a"), ord("z") + 1))
        + "".join(chr(code) for code in range(ord("A"), ord("Z") + 1))
        + "".join(chr(code) for code in range(ord("0"), ord("9") + 1))
    )

    return "".join(choice(symbols) for _ in range(code_length))


async def create_redirect(original_url: str, session: AsyncSession):
    # TODO: solve collisions
    short_code = generate_short_code()
    redirect = RedirectURL(short_code=short_code, original_url=original_url)

    session.add(redirect)
    await session.commit()

    return redirect


async def delete_redirect(short_code: str, session: AsyncSession):
    query = select(RedirectURL).where(RedirectURL.short_code == short_code)
    result = await session.execute(query)

    redirect = result.scalars().first()

    if redirect is None:
        raise RedirectURLNotFoundException

    await session.delete(redirect)
    await session.commit()

    return redirect
