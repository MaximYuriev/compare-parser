from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

from src.commons.db.models import Bulletin
from src.commons.db.utils import get_batches
from src.commons.parser.schema import BulletinSchema


def get_sync_engine(db_url: str) -> Engine:
    return create_engine(db_url, echo=False)


def get_sync_session_maker(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(engine, expire_on_commit=False)


def save_bulletin_in_db(
        session: Session,
        bulletin_schema_list: list[BulletinSchema],
) -> None:
    for batch in get_batches(bulletin_schema_list):
        session.bulk_insert_mappings(Bulletin, batch)
    session.commit()
