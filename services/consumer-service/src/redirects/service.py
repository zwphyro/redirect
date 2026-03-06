from src.ip.service import IPService
from src.redirects.repository import RedirectsRepository
from src.redirects.schemas import BaseRedirectSchema, RedirectSchema
from src.user_agent.service import UserAgentService


class RedirectService:
    def __init__(
        self,
        repository: RedirectsRepository,
        ip_service: IPService,
        user_agent_service: UserAgentService,
    ):
        self.repository = repository
        self.ip_service = ip_service
        self.user_agent_service = user_agent_service

    def _manage_redirects(self, base_redirects: list[BaseRedirectSchema]):
        # TODO: add parallel ip data fetching
        for base_redirect in base_redirects:
            user_agent = self.user_agent_service.get_user_agent(
                base_redirect.user_agent, base_redirect.language
            )
            ip_info = self.ip_service.get_ip_info(base_redirect.ip)
            yield base_redirect, user_agent, ip_info

    def store_redirects(self, base_redirects: list[BaseRedirectSchema]):
        redirects = [
            RedirectSchema.from_base_models(*base_models)
            for base_models in self._manage_redirects(base_redirects)
        ]
        self.repository.store_redirects(redirects)
