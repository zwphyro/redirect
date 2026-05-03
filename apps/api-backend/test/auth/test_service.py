import logging
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from src.auth.exceptions import (
    IncorrectLoginOrPasswordError,
    InvalidPayloadError,
    TokenExpiredError,
    UserNotFoundError,
)
from src.auth.schemas import AccessTokenPayload, RefreshTokenPayload
from src.auth.service import AuthService


@pytest.fixture
def auth_service(mock_uow, mock_auth_repo, mock_password_hash, mock_token):
    mock_uow.auth = mock_auth_repo
    mock_uow.redirect_link = MagicMock()
    return AuthService(mock_uow, mock_password_hash, mock_token)


class TestRegister:
    async def test_success(self, auth_service, mock_uow, mock_auth_repo, user_model):
        mock_auth_repo.get_user_by_email.return_value = None
        mock_auth_repo.create_user.return_value = user_model

        result = await auth_service.register("test@example.com", "password123")

        assert result is None
        mock_auth_repo.create_user.assert_called_once_with(
            "test@example.com", "hashed_password"
        )
        mock_uow.commit.assert_awaited_once()

    async def test_user_already_exists(
        self, auth_service, mock_uow, mock_auth_repo, user_model, caplog
    ):
        mock_auth_repo.get_user_by_email.return_value = user_model

        with caplog.at_level(logging.WARNING, logger="src.auth.service"):
            result = await auth_service.register("test@example.com", "password123")

        assert result is None
        mock_auth_repo.create_user.assert_not_called()
        mock_uow.commit.assert_not_called()
        assert "test@example.com" in caplog.text
        assert "already exists" in caplog.text

    async def test_create_user_raises(
        self, auth_service, mock_uow, mock_auth_repo, caplog
    ):
        mock_auth_repo.get_user_by_email.return_value = None
        mock_auth_repo.create_user.side_effect = Exception("db error")

        with caplog.at_level(logging.WARNING, logger="src.auth.service"):
            result = await auth_service.register("test@example.com", "password123")

        assert result is None
        mock_uow.commit.assert_not_called()
        assert "test@example.com" in caplog.text
        assert "Failed to create user" in caplog.text


class TestLogin:
    async def test_valid_credentials(
        self, auth_service, mock_auth_repo, mock_token, user_model
    ):
        mock_auth_repo.get_user_by_email.return_value = user_model

        access_token, refresh_token = await auth_service.login(
            "test@example.com", "password123"
        )

        assert access_token == "access_token"
        assert refresh_token == "refresh_token"
        mock_token.create_access_token.assert_called_once_with(
            AccessTokenPayload(sub="1")
        )
        mock_token.create_refresh_token.assert_called_once_with(
            RefreshTokenPayload(sub="1")
        )

    async def test_user_not_found(self, auth_service, mock_auth_repo):
        mock_auth_repo.get_user_by_email.return_value = None

        with pytest.raises(IncorrectLoginOrPasswordError):
            await auth_service.login("missing@example.com", "password123")

    async def test_wrong_password(
        self, auth_service, mock_auth_repo, mock_password_hash, user_model
    ):
        mock_auth_repo.get_user_by_email.return_value = user_model
        mock_password_hash.verify.return_value = False

        with pytest.raises(IncorrectLoginOrPasswordError):
            await auth_service.login("test@example.com", "wrongpassword")


class TestGetCurrentUser:
    async def test_valid_token(
        self, auth_service, mock_auth_repo, mock_token, user_model
    ):
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        payload = AccessTokenPayload(sub="1", exp=future)
        mock_token.decode_access_token.return_value = payload
        mock_auth_repo.get_user_by_id.return_value = user_model

        user = await auth_service.get_current_user("valid_token")

        assert user == user_model
        mock_auth_repo.get_user_by_id.assert_awaited_once_with(1)

    async def test_invalid_payload(self, auth_service, mock_token):
        mock_token.decode_access_token.return_value = None

        with pytest.raises(InvalidPayloadError):
            await auth_service.get_current_user("bad_token")

    async def test_expired_token(self, auth_service, mock_token):
        past = datetime.now(timezone.utc) - timedelta(hours=1)
        payload = AccessTokenPayload(sub="1", exp=past)
        mock_token.decode_access_token.return_value = payload

        with pytest.raises(TokenExpiredError):
            await auth_service.get_current_user("expired_token")

    async def test_user_not_found(self, auth_service, mock_auth_repo, mock_token):
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        payload = AccessTokenPayload(sub="1", exp=future)
        mock_token.decode_access_token.return_value = payload
        mock_auth_repo.get_user_by_id.return_value = None

        with pytest.raises(UserNotFoundError):
            await auth_service.get_current_user("valid_token")


class TestRefresh:
    async def test_valid_refresh_token(
        self, auth_service, mock_auth_repo, mock_token, user_model
    ):
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        payload = RefreshTokenPayload(sub="1", exp=future)
        mock_token.decode_refresh_token.return_value = payload
        mock_auth_repo.get_user_by_id.return_value = user_model

        access_token, new_refresh_token = await auth_service.refresh("valid_refresh")

        assert access_token == "access_token"
        assert new_refresh_token == "refresh_token"

    async def test_invalid_payload(self, auth_service, mock_token):
        mock_token.decode_refresh_token.return_value = None

        with pytest.raises(InvalidPayloadError):
            await auth_service.refresh("bad_token")

    async def test_expired_token(self, auth_service, mock_token):
        past = datetime.now(timezone.utc) - timedelta(hours=1)
        payload = RefreshTokenPayload(sub="1", exp=past)
        mock_token.decode_refresh_token.return_value = payload

        with pytest.raises(TokenExpiredError):
            await auth_service.refresh("expired_token")

    async def test_user_not_found(self, auth_service, mock_auth_repo, mock_token):
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        payload = RefreshTokenPayload(sub="1", exp=future)
        mock_token.decode_refresh_token.return_value = payload
        mock_auth_repo.get_user_by_id.return_value = None

        with pytest.raises(UserNotFoundError):
            await auth_service.refresh("valid_refresh")
