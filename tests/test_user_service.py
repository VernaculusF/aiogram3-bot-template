from types import SimpleNamespace
import unittest

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


class TestUserService(unittest.IsolatedAsyncioTestCase):
    async def test_register_user_creates_profile(self) -> None:
        repo = FakeUserRepository()
        service = UserService(repo)  # type: ignore[arg-type]

        profile = await service.register_user(
            telegram_id=100,
            full_name="John Doe",
            age=30,
            city="Berlin",
            about="Backend engineer",
        )

        self.assertEqual(profile.city, "Berlin")
        self.assertEqual(profile.full_name, "John Doe")

    async def test_register_user_returns_existing_profile(self) -> None:
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

        self.assertIs(second, first)
        self.assertEqual(second.full_name, "John Doe")
