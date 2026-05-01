from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base, id, created_at, updated_at

if TYPE_CHECKING:
    from src.redirect_link.models import RedirectLink


class User(Base):
    id: Mapped[id]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    redirect_links: Mapped[list["RedirectLink"]] = relationship(back_populates="user")
