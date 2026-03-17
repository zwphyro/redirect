from concurrent.futures import ThreadPoolExecutor

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

    def _enrich_redirect(self, base_redirect: BaseRedirectSchema):
        user_agent = self.user_agent_service.get_user_agent(
            base_redirect.user_agent,
            base_redirect.language,
        )
        ip_info = self.ip_service.get_ip_info(base_redirect.ip)
        return base_redirect, user_agent, ip_info

    def _manage_redirects(self, base_redirects: list[BaseRedirectSchema]):
        if not base_redirects:
            return

        max_workers = min(len(base_redirects), 5)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(self._enrich_redirect, base_redirects):
                yield result

    def store_redirects(self, base_redirects: list[BaseRedirectSchema]):
        redirects = [
            RedirectSchema.from_base_models(*base_models)
            for base_models in self._manage_redirects(base_redirects)
        ]
        self.repository.store_redirects(redirects)
