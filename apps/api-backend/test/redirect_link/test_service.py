import logging

import pytest

from src.exceptions import DatabaseError, NotFoundError
from src.redirect_link.service import RedirectLinkService


@pytest.fixture
def redirect_service(mock_uow, mock_redirect_repo, mock_short_code_generator):
    mock_uow.redirect_link = mock_redirect_repo
    return RedirectLinkService(mock_uow, mock_short_code_generator)


class TestList:
    async def test_list(self, redirect_service, mock_redirect_repo, link_model):
        mock_redirect_repo.list.return_value = [link_model]

        result = await redirect_service.list(1, limit=10, offset=0)

        assert result == [link_model]
        mock_redirect_repo.list.assert_awaited_once_with(1, limit=10, offset=0)


class TestGetLink:
    async def test_exists(self, redirect_service, mock_redirect_repo, link_model):
        mock_redirect_repo.get_by_short_code.return_value = link_model

        result = await redirect_service.get_link("abc123", 1)

        assert result == link_model

    async def test_missing(self, redirect_service, mock_redirect_repo):
        mock_redirect_repo.get_by_short_code.return_value = None

        with pytest.raises(NotFoundError):
            await redirect_service.get_link("missing", 1)


class TestCreateLink:
    async def test_success_first_try(
        self,
        redirect_service,
        mock_uow,
        mock_redirect_repo,
        mock_short_code_generator,
        link_model,
    ):
        mock_redirect_repo.create.return_value = link_model

        result = await redirect_service.create_link("https://example.com", 1)

        assert result == link_model
        mock_short_code_generator.generate.assert_called_once()
        mock_uow.commit.assert_awaited_once()

    async def test_retry_then_success(
        self,
        redirect_service,
        mock_uow,
        mock_redirect_repo,
        mock_short_code_generator,
        link_model,
    ):
        mock_redirect_repo.create.side_effect = [DatabaseError("conflict"), link_model]

        result = await redirect_service.create_link("https://example.com", 1)

        assert result == link_model
        assert mock_short_code_generator.generate.call_count == 2
        mock_uow.rollback.assert_awaited_once()
        mock_uow.commit.assert_awaited_once()

    async def test_exhaust_all_attempts(
        self,
        redirect_service,
        mock_uow,
        mock_redirect_repo,
        mock_short_code_generator,
        caplog,
    ):
        mock_redirect_repo.create.side_effect = DatabaseError("conflict")
        max_attempts = 10

        with caplog.at_level(logging.ERROR, logger="src.redirect_link.service"):
            with pytest.raises(
                RuntimeError, match="Failed to generate unique short code"
            ):
                await redirect_service.create_link("https://example.com", 1)

        assert mock_short_code_generator.generate.call_count == max_attempts
        assert mock_uow.rollback.await_count == max_attempts
        mock_uow.commit.assert_not_called()
        assert (
            f"Failed to generate unique short code after {max_attempts} attempts"
            in caplog.text
        )


class TestDeleteLink:
    async def test_exists(
        self, redirect_service, mock_uow, mock_redirect_repo, link_model
    ):
        mock_redirect_repo.delete_by_short_code.return_value = link_model

        result = await redirect_service.delete_link("abc123", 1)

        assert result == link_model
        mock_uow.commit.assert_awaited_once()

    async def test_missing(self, redirect_service, mock_redirect_repo):
        mock_redirect_repo.delete_by_short_code.return_value = None

        with pytest.raises(NotFoundError):
            await redirect_service.delete_link("missing", 1)


class TestToggleActive:
    async def test_exists(
        self, redirect_service, mock_uow, mock_redirect_repo, link_model
    ):
        mock_redirect_repo.get_by_short_code.return_value = link_model

        result = await redirect_service.toggle_active("abc123", 1)

        assert result.is_active is False
        mock_uow.commit.assert_awaited_once()

    async def test_missing(self, redirect_service, mock_redirect_repo):
        mock_redirect_repo.get_by_short_code.return_value = None

        with pytest.raises(NotFoundError):
            await redirect_service.toggle_active("missing", 1)
