from typing import Annotated
from fastapi import Depends
from src.dependencies import UOWDependency
from src.redirect_link.service import RedirectLinkService
from src.redirect_link.short_code import ShortCodeGenerator


def get_short_code_generator():
    return ShortCodeGenerator(length=6)


def get_redirect_link_service(
    uow: UOWDependency,
    short_code_generator: ShortCodeGenerator = Depends(get_short_code_generator),
):
    return RedirectLinkService(uow, short_code_generator)


ServiceDependency = Annotated[RedirectLinkService, Depends(get_redirect_link_service)]
