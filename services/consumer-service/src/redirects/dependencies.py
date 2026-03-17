from src.clickhouse import get_clickhouse_client
from src.ip.service import IPService
from src.redirects.repository import RedirectsRepository
from src.redirects.service import RedirectService
from src.user_agent.service import UserAgentService


def build_redirect_service() -> RedirectService:
    client = get_clickhouse_client()
    repository = RedirectsRepository(client)
    ip_service = IPService()
    user_agent_service = UserAgentService()

    return RedirectService(repository, ip_service, user_agent_service)
