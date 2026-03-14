from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base, id, created_at, updated_at


class RedirectURL(Base):
    id: Mapped[id]
    short_code: Mapped[str] = mapped_column(unique=True, nullable=False)
    original_url: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
