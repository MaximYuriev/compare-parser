import datetime
from io import BytesIO

import requests

from src.commons.constants import URL_FOR_PARSING, STOP_YEAR, MAX_REQUEST_RETRIES
from src.commons.exceptions import UnableDefineSearchBoundariesException
from src.commons.parser.parser import get_xls_files_download_links_w_bulletin_date, get_first_and_last_pages
from src.commons.parser.schema import BulletinSchema
from src.commons.xls.xls_worker import xls_to_schema_list

type xlsFileLink = str
type xlsFile = BytesIO
type BulletinDate = datetime.date
type Page = str
type FirstPage = int
type LastPage = int


def get_bulletin_schema_from_parsed_website() -> list[BulletinSchema]:
    xls_file_w_bulletin_date_list = _get_list_w_xls_file_and_bulletin_date()
    bulletin_list_schema = []

    for file, date in xls_file_w_bulletin_date_list:
        bulletin_list_schema.extend(
            xls_to_schema_list(file, date)
        )

    return bulletin_list_schema


def _get_list_w_xls_file_and_bulletin_date() -> list[tuple[xlsFile, BulletinDate]]:
    xls_file_w_bulletin_date_list = []
    first_page, last_page = _get_search_boundary()
    for page_number in range(first_page, last_page):
        url = f"{URL_FOR_PARSING}{str(page_number)}"
        page = _get_page(url)
        if page is not None:
            xls_file_link_w_bulletin_date = get_xls_files_download_links_w_bulletin_date(page)

            for link, date in xls_file_link_w_bulletin_date:
                if date.year >= STOP_YEAR:
                    xls_file_w_bulletin_date = _fetch_xls_file_w_bulletin_date_from_link(link, date)
                    xls_file_w_bulletin_date_list.append(xls_file_w_bulletin_date)
                else:
                    return xls_file_w_bulletin_date_list

    return xls_file_w_bulletin_date_list


def _get_search_boundary() -> tuple[FirstPage, LastPage]:
    url = URL_FOR_PARSING

    current_retries = 0
    while current_retries < MAX_REQUEST_RETRIES:
        response = requests.get(url)
        if response.status_code == 200:
            return get_first_and_last_pages(response.text)
        else:
            current_retries += 1
    raise UnableDefineSearchBoundariesException


def _get_page(url: str) -> Page | None:
    current_retries = 0
    while current_retries < MAX_REQUEST_RETRIES:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            current_retries += 1
            print(f"Попытка №{current_retries} выполнить запрос по адресу: {url}")
    print(f"Запрос по адресу {url} завершился неудачно!")


def _fetch_xls_file_w_bulletin_date_from_link(
        xls_file_link: xlsFileLink,
        bulletin_date: BulletinDate,
) -> tuple[xlsFile, BulletinDate] | None:
    current_retries = 0
    while current_retries < MAX_REQUEST_RETRIES:
        file = requests.get(xls_file_link)
        if file.status_code == 200:
            xls_file = BytesIO(file.content)
            return xls_file, bulletin_date
        else:
            current_retries += 1
            print(f"Попытка №{current_retries} скачать файл по адресу: {xls_file_link}")
    print(f"Скачивание файла по адресу: {xls_file_link} завершилось неудачно!")
