"""link users to links

Revision ID: 49b4739e7266
Revises: 5447d9a744a5
Create Date: 2026-05-02 02:17:49.280767

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "49b4739e7266"
down_revision: Union[str, Sequence[str], None] = "5447d9a744a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DELETE FROM redirect_links")
    op.add_column("redirect_links", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "fk_redirect_links_user_id",
        "redirect_links",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_redirect_links_user_id", "redirect_links", type_="foreignkey"
    )
    op.drop_column("redirect_links", "user_id")
