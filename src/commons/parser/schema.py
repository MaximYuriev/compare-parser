import datetime

from pydantic import BaseModel, field_validator, computed_field


class BulletinSchema(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    delivery_basis_name: str
    volume: int
    total: int
    count: int
    date: datetime.date

    @field_validator("volume", mode='before')
    @classmethod
    def validate_volume(cls, value: str) -> int:
        return int(value) if value != "-" and value != "" else 0

    @field_validator("total", mode='before')
    @classmethod
    def validate_total(cls, value: str) -> int:
        return int(value) if value != "-" and value != "" else 0

    @field_validator("count", mode='before')
    @classmethod
    def validate_count(cls, value: str) -> int:
        return int(value) if value != "-" and value != "" else 0

    @computed_field
    @property
    def oil_id(self) -> str:
        return self.exchange_product_id[:4]

    @computed_field
    @property
    def delivery_basis_id(self) -> str:
        return self.exchange_product_id[4:7]

    @computed_field
    @property
    def delivery_type_id(self) -> str:
        return self.exchange_product_id[-1]
