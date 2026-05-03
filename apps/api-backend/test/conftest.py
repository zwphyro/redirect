import logging
from unittest.mock import AsyncMock, MagicMock

import pytest


log = logging.getLogger(__name__)


@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()
    uow.flush = AsyncMock()
    return uow


@pytest.fixture
def mock_auth_repo():
    repo = MagicMock()
    repo.get_user_by_id = AsyncMock()
    repo.get_user_by_email = AsyncMock()
    repo.create_user = AsyncMock()
    return repo


@pytest.fixture
def mock_redirect_repo():
    repo = MagicMock()
    repo.list = AsyncMock()
    repo.get_by_short_code = AsyncMock()
    repo.create = AsyncMock()
    repo.delete_by_short_code = AsyncMock()
    return repo


@pytest.fixture
def mock_password_hash():
    ph = MagicMock()
    ph.hash = MagicMock(return_value="hashed_password")
    ph.verify = MagicMock(return_value=True)
    return ph


@pytest.fixture
def mock_token():
    token = MagicMock()
    token.create_access_token = MagicMock(return_value="access_token")
    token.create_refresh_token = MagicMock(return_value="refresh_token")
    token.decode_access_token = MagicMock(return_value=None)
    token.decode_refresh_token = MagicMock(return_value=None)
    return token


@pytest.fixture
def mock_short_code_generator():
    gen = MagicMock()
    gen.generate = MagicMock(return_value="abc123")
    return gen


@pytest.fixture
def user_model():
    class FakeUser:
        id = 1
        email = "test@example.com"
        password_hash = "hashed_password"

    return FakeUser()


@pytest.fixture
def link_model():
    class FakeLink:
        id = 1
        short_code = "abc123"
        target_url = "https://example.com"
        is_active = True
        user_id = 1

    return FakeLink()
