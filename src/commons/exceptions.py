from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class ParserException(Exception):
    @property
    def message(self) -> str:
        return "Ошибка парсера!"


@dataclass(frozen=True, eq=False)
class TableNotFoundException(ParserException):
    table_title: str

    @property
    def message(self) -> str:
        return f"Таблица с названием '{self.table_title}' не найдена!"


@dataclass(frozen=True, eq=False)
class UnableDefineSearchBoundariesException(ParserException):
    @property
    def message(self) -> str:
        return f"Невозможно определить границы поиска!"
