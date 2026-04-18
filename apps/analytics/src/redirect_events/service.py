from concurrent.futures import ThreadPoolExecutor

from src.ip.service import IPService
from src.redirect_events.repository import RedirectEventsRepository
from src.redirect_events.schemas import BaseRedirectEventSchema, RedirectEventSchema
from src.user_agent.service import UserAgentService


class RedirectEventService:
    def __init__(
        self,
        repository: RedirectEventsRepository,
        ip_service: IPService,
        user_agent_service: UserAgentService,
    ):
        self.repository = repository
        self.ip_service = ip_service
        self.user_agent_service = user_agent_service

    def _enrich_redirect_event(self, base_redirect_event: BaseRedirectEventSchema):
        user_agent = self.user_agent_service.get_user_agent(
            base_redirect_event.user_agent,
            base_redirect_event.language,
        )
        ip_info = self.ip_service.get_ip_info(base_redirect_event.ip)
        return base_redirect_event, user_agent, ip_info

    def _manage_redirect_events(
        self, base_redirect_events: list[BaseRedirectEventSchema]
    ):
        if not base_redirect_events:
            return

        max_workers = min(len(base_redirect_events), 5)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(
                self._enrich_redirect_event, base_redirect_events
            ):
                yield result

    def store_redirect_events(
        self, base_redirect_events: list[BaseRedirectEventSchema]
    ):
        redirect_events = [
            RedirectEventSchema.from_base_models(*base_models)
            for base_models in self._manage_redirect_events(base_redirect_events)
        ]
        self.repository.store_redirect_events(redirect_events)
