import aiohttp

from src.async_parser.db import get_async_engine, get_async_session_maker, save_bulletin_in_db
from src.async_parser.parser import get_bulletin_schema_from_parsed_website
from src.config import config


async def start_async_parser() -> None:
    async_engine = get_async_engine(config.postgres.db_url)
    session_maker = get_async_session_maker(async_engine)

    async with aiohttp.ClientSession() as session:
        bulletin_schema_list = await get_bulletin_schema_from_parsed_website(session)

    await save_bulletin_in_db(session_maker=session_maker, bulletin_schema_list=bulletin_schema_list)
