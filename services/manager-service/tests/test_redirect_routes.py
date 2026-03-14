import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.db import Base
from src.main import app
from src.dependencies import get_db


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


engine_test = create_async_engine(TEST_DATABASE_URL)
AsyncSessionTestLocal = async_sessionmaker(
    engine_test, expire_on_commit=False, class_=AsyncSession
)


async def _override_get_db() -> AsyncSession:
    async with AsyncSessionTestLocal() as session:
        yield session


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True, scope="module")
async def setup_database():
    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_and_get_redirect():
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_response = await client.post(
            "/redirects/",
            json={"original_url": "https://example.com"},
        )

        assert create_response.status_code == 200
        created = create_response.json()
        assert created["original_url"] == "https://example.com"
        assert created["short_code"]
        assert created["is_active"] is True

        get_response = await client.get(f"/redirects/{created['short_code']}")
        assert get_response.status_code == 200
        fetched = get_response.json()
        assert fetched == created


@pytest.mark.asyncio
async def test_get_redirect_not_found_returns_404():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/redirects/nonexistent")

        assert response.status_code == 404
        body = response.json()
        assert "detail" in body
