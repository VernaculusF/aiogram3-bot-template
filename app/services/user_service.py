from app.db.repo import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def get_profile(self, telegram_id: int):
        return await self._repository.get_by_telegram_id(telegram_id)

    async def register_user(self, telegram_id: int, full_name: str, age: int, city: str, about: str):
        existing = await self._repository.get_by_telegram_id(telegram_id)
        if existing:
            return existing
        return await self._repository.create(
            telegram_id=telegram_id,
            full_name=full_name,
            age=age,
            city=city,
            about=about,
        )
