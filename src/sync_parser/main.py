from src.config import config
from src.sync_parser.db import get_sync_engine, get_sync_session_maker, save_bulletin_in_db
from src.sync_parser.parser import get_bulletin_schema_from_parsed_website


def start_sync_parser() -> None:
    async_engine = get_sync_engine(config.postgres.db_url_sync)
    session_maker = get_sync_session_maker(async_engine)

    bulletin_schema_list = get_bulletin_schema_from_parsed_website()

    with session_maker() as session:
        save_bulletin_in_db(session=session, bulletin_schema_list=bulletin_schema_list)


if __name__ == "__main__":
    start_sync_parser()
