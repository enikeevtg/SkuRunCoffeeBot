from sqlalchemy import select, update
from typing import List

from database.models import async_session
from database.models import User, DrinkCategory, DrinkItem


async def set_user(from_user, nickname: str) -> None:
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.tg_id == from_user.id)
        )

        if not user:
            session.add(
                User(
                    tg_id=from_user.id,
                    username=from_user.username,
                    first_name=from_user.first_name,
                    last_name=from_user.last_name,
                    nickname=nickname,
                )
            )
            await session.commit()


async def get_nickname(tg_id: int) -> str | None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.nickname if user else None


async def update_nickname(tg_id: int, nickname: str) -> None:
    async with async_session() as session:
        await session.execute(
            update(User).values(nickname=nickname).where(User.tg_id == tg_id)
        )
        await session.commit()


async def get_categories() -> List[DrinkCategory]:
    async with async_session() as session:
        return await session.scalars(select(DrinkCategory))


async def get_category_items(category_id: int) -> List[DrinkItem]:
    async with async_session() as session:
        return await session.scalars(
            select(DrinkItem).where(DrinkItem.category_id == category_id)
        )


async def get_all_items() -> List[DrinkItem]:
    async with async_session() as session:
        return await session.scalars(select(DrinkItem))


async def get_item_by_id(item_id: int):
    async with async_session() as session:
        return await session.scalar(
            select(DrinkItem).where(DrinkItem.id == item_id)
        )
