import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine

from app.bot.handlers import setup_handlers
from app.bot.middlewares.db import DbSessionMiddleware
from app.config import get_settings
from app.db.base import Base
from app.db import models  # noqa: F401
from app.db.session import build_session_factory


async def create_db_schema(database_dsn: str) -> None:
    engine = create_async_engine(database_dsn, echo=False, pool_pre_ping=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def main() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    await create_db_schema(settings.database_dsn)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    session_factory = build_session_factory(settings.database_dsn)
    dp.update.middleware(DbSessionMiddleware(session_factory))
    dp.include_router(setup_handlers())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
