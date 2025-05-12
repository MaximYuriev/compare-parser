import asyncio
import datetime
from asyncio import Task
from io import BytesIO

from aiohttp import ClientSession

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


async def get_bulletin_schema_from_parsed_website(session: ClientSession) -> list[BulletinSchema]:
    xls_file_w_bulletin_date_list = await _get_list_w_xls_file_and_bulletin_date(session)
    bulletin_list_schema = []

    for file, date in xls_file_w_bulletin_date_list:
        bulletin_list_schema.extend(
            xls_to_schema_list(file, date)
        )

    return bulletin_list_schema


async def _get_list_w_xls_file_and_bulletin_date(session: ClientSession) -> list[tuple[xlsFile, BulletinDate]]:
    fetch_files_tasks = await _get_fetch_files_tasks(session)
    return await asyncio.gather(*fetch_files_tasks)


async def _get_fetch_files_tasks(session: ClientSession) -> list[Task]:
    fetch_files_tasks = []
    first_page, last_page = await _get_search_boundary(session)
    for page_number in range(first_page, last_page):
        url = f"{URL_FOR_PARSING}{str(page_number)}"
        page = await _get_page(session, url)
        if page is not None:
            xls_file_link_w_bulletin_date = get_xls_files_download_links_w_bulletin_date(page)

            for link, date in xls_file_link_w_bulletin_date:
                if date.year >= STOP_YEAR:
                    task = asyncio.create_task(_fetch_xls_file_w_bulletin_date_from_link(session, link, date))
                    fetch_files_tasks.append(task)
                else:
                    return fetch_files_tasks

    return fetch_files_tasks


async def _get_search_boundary(session: ClientSession) -> tuple[FirstPage, LastPage]:
    url = URL_FOR_PARSING

    current_retries = 0
    while current_retries < MAX_REQUEST_RETRIES:
        response = await session.get(url)
        if response.status == 200:
            return get_first_and_last_pages(await response.text())
        else:
            current_retries += 1
    raise UnableDefineSearchBoundariesException


async def _get_page(session: ClientSession, url: str) -> Page | None:
    current_retries = 0
    while current_retries < MAX_REQUEST_RETRIES:
        response = await session.get(url)
        if response.status == 200:
            return await response.text()
        else:
            current_retries += 1
            print(f"Попытка №{current_retries} выполнить запрос по адресу: {url}")
    print(f"Запрос по адресу {url} завершился неудачно!")


async def _fetch_xls_file_w_bulletin_date_from_link(
        session: ClientSession,
        xls_file_link: xlsFileLink,
        bulletin_date: BulletinDate,
) -> tuple[xlsFile, BulletinDate] | None:
    current_retries = 0
    while current_retries < MAX_REQUEST_RETRIES:
        file = await session.get(xls_file_link)
        if file.status == 200:
            xls_file = BytesIO(await file.read())
            return xls_file, bulletin_date
        else:
            current_retries += 1
            print(f"Попытка №{current_retries} скачать файл по адресу: {xls_file_link}")
    print(f"Скачивание файла по адресу: {xls_file_link} завершилось неудачно!")
