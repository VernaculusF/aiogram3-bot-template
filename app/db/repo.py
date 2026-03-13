from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, telegram_id: int, full_name: str, age: int, city: str, about: str) -> User:
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            age=age,
            city=city,
            about=about,
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def update(self, user: User, full_name: str, age: int, city: str, about: str) -> User:
        user.full_name = full_name
        user.age = age
        user.city = city
        user.about = about

        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def count_users(self) -> int:
        stmt = select(func.count(User.id))
        result = await self._session.execute(stmt)
        return int(result.scalar_one())
