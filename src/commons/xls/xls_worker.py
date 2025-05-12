import datetime
from io import BytesIO

import xlrd
from xlrd.sheet import Sheet

from src.commons.constants import END_REPORT_FILE_ROW, SEARCHED_TEXT
from src.commons.exceptions import TableNotFoundException
from src.commons.parser.schema import BulletinSchema
from src.commons.xls.headers import BulletinHeaderEnum

type xlsFile = BytesIO
type StartTableIndex = int
type HeaderName = str
type CellIndex = int


def xls_to_schema_list(
        xls_file: xlsFile,
        date: datetime.date
) -> list[BulletinSchema]:
    workbook = xlrd.open_workbook(file_contents=xls_file.read())
    sheet = workbook.sheet_by_index(0)

    table_idx = _find_table_idx(sheet=sheet, table_title=SEARCHED_TEXT)
    table_headers = _get_table_headers(sheet=sheet, table_idx=table_idx)

    bulletin_list = []
    for row_idx in range(table_idx + 2, sheet.nrows):
        row_values = sheet.row_values(row_idx)
        exchange_product_id = row_values[table_headers[BulletinHeaderEnum.EXCHANGE_PRODUCT_ID]]

        if exchange_product_id not in END_REPORT_FILE_ROW:
            bulletin = BulletinSchema(
                exchange_product_id=exchange_product_id,
                exchange_product_name=row_values[table_headers[BulletinHeaderEnum.EXCHANGE_PRODUCT_NAME]],
                delivery_basis_name=row_values[table_headers[BulletinHeaderEnum.DELIVERY_BASIS_NAME]],
                volume=row_values[table_headers[BulletinHeaderEnum.VOLUME]],
                total=row_values[table_headers[BulletinHeaderEnum.TOTAL]],
                count=row_values[table_headers[BulletinHeaderEnum.COUNT]],
                date=date,
            )
            if bulletin.count > 0:
                bulletin_list.append(bulletin)

    return bulletin_list


def _find_table_idx(sheet: Sheet, table_title: str) -> StartTableIndex:
    for row_idx in range(sheet.nrows):
        row_values = sheet.row_values(row_idx)
        if any(table_title in str(cell) for cell in row_values):
            return row_idx + 1
    raise TableNotFoundException(table_title)


def _get_table_headers(sheet: Sheet, table_idx: StartTableIndex) -> dict[BulletinHeaderEnum, CellIndex]:
    row = sheet.row_values(table_idx)
    header_map = {}

    for idx, header in enumerate(row):
        normalized_header = header.lower().replace("\n", " ")
        if normalized_header in BulletinHeaderEnum:
            header_map[BulletinHeaderEnum(normalized_header)] = idx

    return header_map
