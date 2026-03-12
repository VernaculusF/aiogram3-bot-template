"""create users table

Revision ID: 20260312_1710
Revises:
Create Date: 2026-03-12 17:10:00

"""
from alembic import op  # type: ignore[reportMissingImports]
import sqlalchemy as sa


revision = "20260312_1710"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("users"):
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("telegram_id", sa.BigInteger(), nullable=False),
            sa.Column("full_name", sa.String(length=128), nullable=False),
            sa.Column("age", sa.Integer(), nullable=False),
            sa.Column("city", sa.String(length=120), nullable=False),
            sa.Column("about", sa.String(length=600), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_users_telegram_id", "users", ["telegram_id"], unique=True)
        return

    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    if "city" not in existing_columns:
        op.add_column(
            "users",
            sa.Column("city", sa.String(length=120), nullable=True, server_default=sa.text("'Unknown'")),
        )
        op.alter_column("users", "city", server_default=None, nullable=False)

    existing_indexes = {index["name"] for index in inspector.get_indexes("users")}
    if "ix_users_telegram_id" not in existing_indexes:
        op.create_index("ix_users_telegram_id", "users", ["telegram_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_users_telegram_id", table_name="users")
    op.drop_table("users")
