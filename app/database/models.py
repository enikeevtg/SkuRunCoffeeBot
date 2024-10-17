from decouple import config
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)


engine = create_async_engine(url=config('DB_URL'))

async_session = async_sessionmaker(engine)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(20))
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    cup_name: Mapped[str] = mapped_column(String(20))


class DrinkCategory(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))


class DrinkItem(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))


async def db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
