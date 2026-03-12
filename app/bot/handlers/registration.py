from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from typing import cast

from app.bot.states.registration import RegistrationState
from app.db.repo import UserRepository
from app.services.user_service import UserService

router = Router(name="registration")


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext) -> None:
    await state.set_state(RegistrationState.waiting_name)
    await message.answer("Registration started. Send your full name:")


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("There is no active dialog.")
        return

    await state.clear()
    await message.answer("Dialog canceled.")


@router.message(RegistrationState.waiting_name, F.text)
async def process_name(message: Message, state: FSMContext) -> None:
    if message.text is None:
        await message.answer("Send text value for your name.")
        return

    name = cast(str, message.text).strip()
    if len(name) < 2:
        await message.answer("Name is too short. Please enter at least 2 characters.")
        return

    await state.update_data(full_name=name)
    await state.set_state(RegistrationState.waiting_age)
    await message.answer("Now send your age (number from 10 to 100):")


@router.message(RegistrationState.waiting_age, F.text)
async def process_age(message: Message, state: FSMContext) -> None:
    if message.text is None:
        await message.answer("Send text value for your age.")
        return

    raw_age = cast(str, message.text).strip()
    if not raw_age.isdigit():
        await message.answer("Age should be a number. Try again:")
        return

    age = int(raw_age)
    if age < 10 or age > 100:
        await message.answer("Age should be between 10 and 100. Try again:")
        return

    await state.update_data(age=age)
    await state.set_state(RegistrationState.waiting_city)
    await message.answer("Great. Now send your city (2-80 chars):")


@router.message(RegistrationState.waiting_city, F.text)
async def process_city(message: Message, state: FSMContext) -> None:
    if message.text is None:
        await message.answer("Send text value for your city.")
        return

    city = cast(str, message.text).strip()
    if len(city) < 2 or len(city) > 80:
        await message.answer("City should be between 2 and 80 chars. Try again:")
        return

    await state.update_data(city=city)
    await state.set_state(RegistrationState.waiting_about)
    await message.answer("Tell me a few words about yourself (5-300 chars):")


@router.message(RegistrationState.waiting_about, F.text)
async def process_about(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if message.from_user is None:
        await state.clear()
        return

    if message.text is None:
        await message.answer("Send text value for about section.")
        return

    about = cast(str, message.text).strip()
    if len(about) < 5 or len(about) > 300:
        await message.answer("About text should be between 5 and 300 chars. Try again:")
        return

    data = await state.get_data()
    full_name = data["full_name"]
    age = data["age"]
    city = data["city"]

    service = UserService(UserRepository(session))
    profile = await service.register_user(
        telegram_id=message.from_user.id,
        full_name=full_name,
        age=age,
        city=city,
        about=about,
    )

    await state.clear()
    await message.answer(
        "Registration completed!\n"
        f"Name: {profile.full_name}\n"
        f"Age: {profile.age}\n"
        f"City: {profile.city}\n"
        f"About: {profile.about}\n\n"
        "Use /profile anytime."
    )
