"""Merge user_status and products migrations

Revision ID: 3ceedca8385f
Revises: 2e7c22c73159, ee09877b63b6
Create Date: 2025-12-13 16:15:43.611234
"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = "3ceedca8385f"
down_revision = ('2e7c22c73159', 'ee09877b63b6')
branch_labels = None
depends_on = None

def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
