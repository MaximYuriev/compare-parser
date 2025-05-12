import asyncio

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.commons.db.models import Bulletin
from src.commons.db.utils import get_batches
from src.commons.parser.schema import BulletinSchema


def get_async_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url, echo=False)


def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def save_bulletin_in_db(
        session_maker: async_sessionmaker[AsyncSession],
        bulletin_schema_list: list[BulletinSchema],
) -> None:
    tasks = [_insert_batches(session_maker, batch) for batch in get_batches(bulletin_schema_list)]
    await asyncio.gather(*tasks)


async def _insert_batches(session_maker: async_sessionmaker[AsyncSession], batch: list[dict]) -> None:
    async with session_maker() as session:
        await session.execute(insert(Bulletin).values(batch))
        await session.commit()
