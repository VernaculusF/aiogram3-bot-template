from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repo import UserRepository
from app.services.user_service import UserService

router = Router(name="profile")


@router.message(Command("profile"))
async def cmd_profile(message: Message, session: AsyncSession) -> None:
    if message.from_user is None:
        return

    service = UserService(UserRepository(session))
    profile = await service.get_profile(message.from_user.id)

    if profile is None:
        await message.answer("Profile not found. Use /start or /register.")
        return

    await message.answer(
        "Your profile:\n"
        f"Name: {profile.full_name}\n"
        f"Age: {profile.age}\n"
        f"City: {profile.city}\n"
        f"About: {profile.about}"
    )
