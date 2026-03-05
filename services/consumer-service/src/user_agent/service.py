from user_agents import parse
from acceptlang import parse_accept_lang_header

from src.user_agent.schemas import UserAgentSchema


class UserAgentService:
    def __init__(self):
        pass

    def get_user_agent(self, user_agent: str, language: str):
        ua = parse(user_agent)
        language_tags = list(sorted(parse_accept_lang_header(language)))
        return UserAgentSchema(
            browser=ua.browser.family,
            browser_version=ua.browser.version_string,
            os=ua.os.family,
            os_version=ua.os.version_string,
            device=ua.device.family,
            device_brand=ua.device.brand,
            device_model=ua.device.model,
            language=language_tags[0].name if language_tags else "",
        )
