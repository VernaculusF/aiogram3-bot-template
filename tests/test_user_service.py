from types import SimpleNamespace

import pytest

from app.services.user_service import UserService


class FakeUserRepository:
    def __init__(self) -> None:
        self.storage: dict[int, SimpleNamespace] = {}

    async def get_by_telegram_id(self, telegram_id: int):
        return self.storage.get(telegram_id)

    async def create(self, telegram_id: int, full_name: str, age: int, city: str, about: str):
        user = SimpleNamespace(
            telegram_id=telegram_id,
            full_name=full_name,
            age=age,
            city=city,
            about=about,
        )
        self.storage[telegram_id] = user
        return user


@pytest.mark.asyncio
async def test_register_user_creates_profile() -> None:
    repo = FakeUserRepository()
    service = UserService(repo)  # type: ignore[arg-type]

    profile = await service.register_user(
        telegram_id=100,
        full_name="John Doe",
        age=30,
        city="Berlin",
        about="Backend engineer",
    )

    assert profile.city == "Berlin"
    assert profile.full_name == "John Doe"


@pytest.mark.asyncio
async def test_register_user_returns_existing_profile() -> None:
    repo = FakeUserRepository()
    service = UserService(repo)  # type: ignore[arg-type]

    first = await service.register_user(
        telegram_id=100,
        full_name="John Doe",
        age=30,
        city="Berlin",
        about="Backend engineer",
    )
    second = await service.register_user(
        telegram_id=100,
        full_name="Jane Doe",
        age=22,
        city="Paris",
        about="Product manager",
    )

    assert second is first
    assert second.full_name == "John Doe"
