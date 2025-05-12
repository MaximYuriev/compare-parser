from src.commons.parser.schema import BulletinSchema


def get_batches(bulletin_schema_list: list[BulletinSchema], batch_size: int = 500):
    list_dict = [schema.model_dump() for schema in bulletin_schema_list]
    for i in range(0, len(list_dict), batch_size):
        yield list_dict[i:i + batch_size]
