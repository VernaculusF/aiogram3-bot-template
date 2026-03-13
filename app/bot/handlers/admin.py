from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.repo import UserRepository
from app.services.user_service import UserService

router = Router(name="admin")


def _is_admin(user_id: int | None) -> bool:
    if user_id is None:
        return False
    settings = get_settings()
    return user_id in settings.bot_admins


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else None
    if not _is_admin(user_id):
        await message.answer("Access denied.")
        return

    await message.answer(
        "Admin commands:\n"
        "/stats - show users statistics\n"
        "/report_now - send report to all admins"
    )


@router.message(Command("stats"))
async def cmd_stats(message: Message, session: AsyncSession) -> None:
    user_id = message.from_user.id if message.from_user else None
    if not _is_admin(user_id):
        await message.answer("Access denied.")
        return

    settings = get_settings()
    service = UserService(UserRepository(session))
    users_count = await service.get_users_count()

    await message.answer(
        "<b>Bot stats</b>\n"
        f"Registered users: <code>{users_count}</code>\n"
        f"Scheduler interval: <code>{settings.scheduler_report_interval_minutes}</code> min"
    )


@router.message(Command("report_now"))
async def cmd_report_now(message: Message, session: AsyncSession) -> None:
    user_id = message.from_user.id if message.from_user else None
    if not _is_admin(user_id):
        await message.answer("Access denied.")
        return

    settings = get_settings()
    service = UserService(UserRepository(session))
    users_count = await service.get_users_count()

    text = (
        "<b>Manual admin report</b>\n"
        f"Registered users: <code>{users_count}</code>"
    )

    if message.bot is None:
        await message.answer("Bot instance is unavailable.")
        return

    delivered = 0
    for admin_id in settings.bot_admins:
        try:
            await message.bot.send_message(chat_id=admin_id, text=text)
            delivered += 1
        except Exception:
            continue

    await message.answer(f"Report sent to <code>{delivered}</code> admins.")
