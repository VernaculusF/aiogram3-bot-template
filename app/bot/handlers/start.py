from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.states.registration import RegistrationState
from app.db.repo import UserRepository
from app.services.user_service import UserService

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if message.from_user is None:
        return

    service = UserService(UserRepository(session))
    profile = await service.get_profile(message.from_user.id)

    if profile:
        await message.answer(
            "Welcome back! Use /profile to view your saved profile or /register to update later."
        )
        return

    await state.set_state(RegistrationState.waiting_name)
    await message.answer(
        "Hi! I am your onboarding bot. You are not registered yet.\n"
        "Let us start now. Send your full name:"
    )
