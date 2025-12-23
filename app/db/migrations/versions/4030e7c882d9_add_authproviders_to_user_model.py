"""
add authProviders to user model

Revision ID: 4030e7c882d9
Revises: 83155398b87c
Create Date: 2025-12-23 16:39:10.978145
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4030e7c882d9"
down_revision = "83155398b87c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1️⃣ Add auth_providers as NULLABLE first
    op.add_column(
        "users",
        sa.Column("auth_providers", sa.String(), nullable=True),
    )

    # 2️⃣ Backfill existing users
    op.execute(
        "UPDATE users SET auth_providers = 'local' WHERE auth_providers IS NULL"
    )

    # 3️⃣ Enforce NOT NULL
    op.alter_column(
        "users",
        "auth_providers",
        nullable=False,
    )

    # 4️⃣ Make phone & password nullable (for OAuth users)
    op.alter_column(
        "users",
        "phone",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )

    op.alter_column(
        "users",
        "password",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )


def downgrade() -> None:
    # Revert phone & password constraints
    op.alter_column(
        "users",
        "password",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )

    op.alter_column(
        "users",
        "phone",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )

    # Drop auth_providers
    op.drop_column("users", "auth_providers")
