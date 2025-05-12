from enum import Enum


class BulletinHeaderEnum(Enum):
    EXCHANGE_PRODUCT_ID = "код инструмента"
    EXCHANGE_PRODUCT_NAME = "наименование инструмента"
    DELIVERY_BASIS_NAME = "базис поставки"
    VOLUME = "объем договоров в единицах измерения"
    TOTAL = "обьем договоров, руб."
    COUNT = "количество договоров, шт."
