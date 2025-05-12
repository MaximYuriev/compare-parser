import datetime

from bs4 import BeautifulSoup

from src.commons.constants import CONTAINER_CLASS_NAME, INNER_ELEMENTS_CLASS_NAME, TITLE_INNER_ELEMENT_CLASS_NAME, \
    BASE_URL

type xlsFileLink = str
type BulletinDate = datetime.date
type Page = str
type FirstPage = int
type LastPage = int


def get_first_and_last_pages(page: Page) -> tuple[FirstPage, LastPage]:
    soup = BeautifulSoup(page, 'html.parser')
    container = soup.find('div', class_='bx-pagination-container')
    elements = container.find_all('span')
    return int(elements[1].text), int(elements[-2].text)


def get_xls_files_download_links_w_bulletin_date(page: Page) -> list[tuple[xlsFileLink, BulletinDate]]:
    soup = BeautifulSoup(page, 'html.parser')

    container = soup.find('div', class_=CONTAINER_CLASS_NAME)
    elements = container.find_all('div', class_=INNER_ELEMENTS_CLASS_NAME)

    result = []
    for element in elements:
        link_element = element.find('a')
        link = BASE_URL + link_element["href"]

        date_element = element.find(class_=TITLE_INNER_ELEMENT_CLASS_NAME)
        date_string = date_element.find('span').text
        date = datetime.datetime.strptime(date_string, "%d.%m.%Y").date()

        result.append((link, date))

    return result
