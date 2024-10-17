from sqlalchemy import select, update

from database.models import async_session
from database.models import User


async def set_user(from_user, cup_name: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == from_user.id))

        if not user:
            session.add(User(
                tg_id = from_user.id,
                username = from_user.username,
                first_name = from_user.first_name,
                last_name = from_user.last_name,
                cup_name = cup_name
            ))
            await session.commit()


async def get_user_cup_name(tg_id: int) -> str | None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.cup_name if user else None


async def update_user_cup_name(tg_id: int, cup_name: str) -> None:
    async with async_session() as session:
        await session.execute(update(User)
                              .values(cup_name=cup_name)
                              .where(User.tg_id == tg_id))
        await session.commit()
