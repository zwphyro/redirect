from datetime import datetime
from pydantic import BaseModel


class RedirectDataSchema(BaseModel):
    time: datetime
    short_code: str
    ip: str
    user_agent: str
    language: str
    origin: str

    # @property
    # def browser(self):
    #     ua = parse(self.user_agent)
    #     return ua.browser.family
    #
    # @property
    # def browser_version(self):
    #     ua = parse(self.user_agent)
    #     return ua.browser.version_string
    #
    # @property
    # def os(self):
    #     ua = parse(self.user_agent)
    #     return ua.os.family
    #
    # @property
    # def os_version(self):
    #     ua = parse(self.user_agent)
    #     return ua.os.version_string
    #
    # @property
    # def device(self):
    #     ua = parse(self.user_agent)
    #     return ua.device.family
    #
    # @property
    # def device_brand(self):
    #     ua = parse(self.user_agent)
    #     return ua.device.brand
    #
    # @property
    # def device_model(self):
    #     ua = parse(self.user_agent)
    #     return ua.device.model
    #
    # @property
    # def language_tag(self):
    #     tags = list(sorted(parse_accept_lang_header(self.language)))
    #     return tags[0].name if tags else ""
