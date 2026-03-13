from __future__ import annotations

import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import User

logger = logging.getLogger(__name__)


class BotScheduler:
    def __init__(
        self,
        bot: Bot,
        session_factory: async_sessionmaker[AsyncSession],
        admin_ids: list[int],
        interval_minutes: int,
    ) -> None:
        self._bot = bot
        self._session_factory = session_factory
        self._admin_ids = admin_ids
        self._interval_minutes = max(1, interval_minutes)
        self._scheduler = AsyncIOScheduler()

    def start(self) -> None:
        self._scheduler.add_job(
            self._send_users_report,
            trigger="interval",
            minutes=self._interval_minutes,
            id="users_report",
            replace_existing=True,
        )
        self._scheduler.start()
        logger.info("Scheduler started (interval=%s min)", self._interval_minutes)

    async def shutdown(self) -> None:
        if self._scheduler.running:
            self._scheduler.shutdown(wait=False)
            logger.info("Scheduler stopped")

    async def _send_users_report(self) -> None:
        if not self._admin_ids:
            return

        async with self._session_factory() as session:
            users_count = await self._count_users(session)

        text = (
            "<b>Scheduled report</b>\n"
            f"Registered users: <code>{users_count}</code>"
        )

        for admin_id in self._admin_ids:
            try:
                await self._bot.send_message(chat_id=admin_id, text=text)
            except Exception:
                logger.exception("Failed to send scheduler report to admin_id=%s", admin_id)

    @staticmethod
    async def _count_users(session: AsyncSession) -> int:
        stmt = select(func.count(User.id))
        result = await session.execute(stmt)
        return int(result.scalar_one())
