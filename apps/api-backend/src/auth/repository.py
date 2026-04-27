from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(self, user_id: int):
        user = await self._session.get(User, user_id)

        return user

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self._session.execute(query)

        return result.scalars().first()

    async def create_user(self, email: str, password_hash: str):
        user = User(email=email, password_hash=password_hash)
        self._session.add(user)

        return user
