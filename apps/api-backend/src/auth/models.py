from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base, id, created_at, updated_at


class User(Base):
    id: Mapped[id]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
