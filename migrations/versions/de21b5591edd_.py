"""empty message

Revision ID: de21b5591edd
Revises:
Create Date: 2025-11-20 17:12:36.207296

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "de21b5591edd"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.create_table(
        "ctl_file_sources",
        sa.Column("file_key", sa.String(50), primary_key=True, comment="File key"),
        sa.Column("file_description", sa.String(100), comment="File description"),
        sa.Column("enabled", sa.Boolean, default=True, comment="File import enabled"),
    )
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
