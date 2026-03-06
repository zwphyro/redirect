def redirect_service_dependency(cls):
    @property
    def service(self):
        if not hasattr(self, "_lazy_service"):
            from src.ip.service import IPService
            from src.redirects.repository import RedirectsRepository
            from src.redirects.service import RedirectService
            from src.user_agent.service import UserAgentService
            from src.clickhouse import client

            self._lazy_service = RedirectService(
                RedirectsRepository(client), IPService(), UserAgentService()
            )
        return self._lazy_service

    cls.service = service
    return cls


@redirect_service_dependency
class RedirectServiceMixin: ...
