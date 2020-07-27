import names_of_districts
import requests
from bs4 import BeautifulSoup
import re
import csv
import concurrent.futures
import sprz_get_links
import time
from datetime import date


links_from_all_pages = []


def number_of_pages():

    source = requests.get(
        "https://www.otodom.pl/sprzedaz/mieszkanie/krakow/").text
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
            'https://www.otodom.pl/sprzedaz/mieszkanie/krakow/?page={}'.format(i))

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

        market, surface, rooms, build_year, finishing_condition, heating, windows = [
        ], [], [], [], [], [], []

        columns = [market, surface, rooms, build_year,
                   finishing_condition, heating, windows]

        # price per month
        header_details = soup.find('header')
        whole_price = header_details.div.next_sibling.next_sibling.div.text
        whole_price = float(''.join(d for d in whole_price if d.isdigit()))
        print(whole_price, type(whole_price))

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

            if header == "Rynek:":
                market.append(li_details[header])

            if header == "Liczba pokoi:":
                rooms.append(int(li_details[header]))

            if header == "Rok budowy:":
                build_year.append(int(li_details[header]))

            if header == "Stan wykończenia:":
                finishing_condition.append(li_details[header])

            if header == "Ogrzewanie:":
                heating.append(li_details[header])

            if header == "Okna:":
                windows.append(li_details[header])

        for column in columns:
            if len(column) == 0:
                column.append('None')

        # price per square
        price_per_square = (float(whole_price)//float(surface[0]))

        # # City (pass a parameter if more cities)
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
            data = [whole_price, price_per_square, market[0], surface[0], rooms[0],
                    build_year[0], finishing_condition[0], heating[0], windows[0], city[0], district, link]

            with open(f'{today}_sprzedaz_{city[0]}.csv', 'a+', newline='', encoding="utf-8") as csvfile:
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
