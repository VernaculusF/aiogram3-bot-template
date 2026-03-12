from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context  # type: ignore[reportMissingImports, reportAttributeAccessIssue]
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.db.base import Base
from app.db import models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _build_database_url() -> str:
    host = os.getenv("DATABASE_HOST", "localhost")
    port = os.getenv("DATABASE_PORT", "5432")
    user = os.getenv("DATABASE_USER", "bot_user")
    password = os.getenv("DATABASE_PASSWORD", "bot_pass")
    db_name = os.getenv("DATABASE_NAME", "bot_db")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


config.set_main_option("sqlalchemy.url", _build_database_url())
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
