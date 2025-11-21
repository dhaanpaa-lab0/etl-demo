"""Add filetype to ctl_file_sources

Revision ID: 64d1c82f82f5
Revises: de21b5591edd
Create Date: 2025-11-20 17:27:58.093599

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "64d1c82f82f5"
down_revision: Union[str, Sequence[str], None] = "de21b5591edd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "ctl_file_sources",
        sa.Column("file_type", sa.String(50), comment="File type", default=""),
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
