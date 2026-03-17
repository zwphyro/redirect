from user_agents import parse
from acceptlang import parse_accept_lang_header

from src.user_agent.schemas import UserAgentSchema


class UserAgentService:
    def __init__(self):
        pass

    def get_user_agent(self, user_agent: str, language: str) -> UserAgentSchema:
        try:
            ua = parse(user_agent)
        except Exception:
            ua = parse("")

        try:
            language_tags = list(sorted(parse_accept_lang_header(language)))
        except Exception:
            language_tags = []

        return UserAgentSchema(
            browser=ua.browser.family or None,
            browser_version=ua.browser.version_string or None,
            os=ua.os.family or None,
            os_version=ua.os.version_string or None,
            device=ua.device.family or None,
            device_brand=ua.device.brand or None,
            device_model=ua.device.model or None,
            language=language_tags[0].name if language_tags else None,
        )
