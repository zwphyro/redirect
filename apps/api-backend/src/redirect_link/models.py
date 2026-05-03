from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base, id, created_at, updated_at

if TYPE_CHECKING:
    from src.auth.models import User


class RedirectLink(Base):
    id: Mapped[id]
    short_code: Mapped[str] = mapped_column(unique=True, nullable=False)
    target_url: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["User"] = relationship(back_populates="redirect_links")
