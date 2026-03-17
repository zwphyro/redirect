from src.clickhouse import get_clickhouse_client
from src.ip.service import IPService
from src.redirect_events.repository import RedirectEventsRepository
from src.redirect_events.service import RedirectEventService
from src.user_agent.service import UserAgentService


def build_redirect_event_service() -> RedirectEventService:
    client = get_clickhouse_client()
    repository = RedirectEventsRepository(client)
    ip_service = IPService()
    user_agent_service = UserAgentService()

    return RedirectEventService(repository, ip_service, user_agent_service)
