import names_of_districts
import requests
from bs4 import BeautifulSoup
import re
import csv
import concurrent.futures
import wyn_get_links
import time
from datetime import date

links_from_all_pages = []


def number_of_pages():

    source = requests.get(
        "https://www.otodom.pl/wynajem/mieszkanie/krakow/").text
    soup = BeautifulSoup(source, 'lxml')
    pager = soup.find('ul', attrs={"class": "pager"})
    temporary_list_of_pages = []
    for li in pager.find_all('li'):
        temporary_list_of_pages.append(li.text)

    return temporary_list_of_pages[int(len(temporary_list_of_pages) - 2)]


def list_of_links():

    pages_of_city = int(number_of_pages())
    list_of_page_links = []
    for i in range(1, pages_of_city + 1):
        list_of_page_links.append(
            'https://www.otodom.pl/wynajem/mieszkanie/krakow/?page={}'.format(i))

    return list_of_page_links


def get_links_from_page(link):

    link_details = requests.get(link).text
    soup = BeautifulSoup(link_details, 'lxml')
    main_div = soup.find(
        'div', attrs={"class": "col-md-content section-listing__row-content"})

    for article in main_div.find_all('article'):
        links_from_all_pages.append(article['data-url'])

    print(f'Zapisano oferty z: {link}')


if __name__ == "__main__":
    start = time.perf_counter()
    all_links = list_of_links()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_links_from_page, all_links)

    print()
    finish = time.perf_counter()
    print(f'runtime: {finish-start}')

################################################

check_headers = ['Cena za całość:', 'Cena za m2:',
                 'Rynek:', 'Powierzchnia:', 'Liczba pokoi:', 'Rok budowy:', 'Stan wykończenia:', 'Ogrzewanie:', 'Okna:', 'Miasto:', 'Dzielnica']


pattern_1 = re.compile(r'(?<=<li>)(.*)(?= <strong>)')
pattern_2 = re.compile(r'(?<=<strong>)(.*)(?=</strong>)')

today = str(date.today())


def parse_links(link):
    try:
        print(link)
        source = requests.get(link).text
        soup = BeautifulSoup(source, 'lxml')

        section_overview = soup.find(
            'section', class_="section-overview")

        additional_rent, deposit, surface, rooms = [], [], [], []
        columns = [additional_rent, deposit, surface, rooms]

        # price per month
        header_details = soup.find('header')
        price_per_month = header_details.div.next_sibling.next_sibling.text
        price_per_month = float(''.join(
            d for d in price_per_month if d.isdigit()))

        # Details
        li_details = {}
        for detail in section_overview.find_all('li'):
            detail_desc = pattern_1.search(str(detail)).group(1)
            detail_info = pattern_2.search(str(detail)).group(1)
            li_details[detail_desc] = detail_info  # appending do dict

        for header in li_details:
            if header == "Powierzchnia:":
                surface.append(
                    float(li_details[header].replace(',', '.').replace(' ', '')[:-2]))

            if header == "Czynsz - dodatkowo:":
                additional_rent.append(
                    float(li_details[header].replace(',', '.').replace(' ', '')[:-2]))

            if header == "Kaucja:":
                deposit.append(float(li_details[header].replace(' ', '')[:-2]))

            if header == "Liczba pokoi:":
                rooms.append(int(li_details[header]))

        for column in columns:
            if len(column) == 0:
                column.append('None')

        # City (pass a parameter if more cities)
        city = ['Kraków']

        # Adreess
        location_list = []
        location = header_details.div.a.text.split(',')

        for li in location:
            # print(li.strip())
            location_list.append(li.strip())

        location_exists = False
        for _ in location_list:
            if _ in names_of_districts.names:
                location_exists = True
                district = _

        if location_exists == False:
            pass

        else:
            data = [price_per_month, additional_rent[0],
                    deposit[0], surface[0], rooms[0], city[0], district, link]

            with open(f'{today}_wynajem_{city[0]}.csv', 'a+', newline='', encoding="utf-8") as csvfile:
                data_row = csv.writer(csvfile)
                data_row.writerow(data)

    except Exception as error:
        print(error, link)


if __name__ == "__main__":
    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(parse_links, links_from_all_pages)

    finish = time.perf_counter()
    print(f'runtime: {finish-start}')
