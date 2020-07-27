import names_of_districts
import requests
from bs4 import BeautifulSoup
import re
import csv
import concurrent.futures
import sprz_get_links
import time
from datetime import date


check_headers = ['Cena za całość:', 'Cena za m2:',
                 'Rynek:', 'Powierzchnia:', 'Liczba pokoi:', 'Rok budowy:', 'Stan wykończenia:', 'Ogrzewanie:', 'Okna:', 'Miasto:', 'Dzielnica']


pattern_1 = re.compile(r'(?<=<li>)(.*)(?= <strong>)')
pattern_2 = re.compile(r'(?<=<strong>)(.*)(?=</strong>)')

today = str(date.today())


def parse_links(link):
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
    whole_price = ''.join(d for d in whole_price if d.isdigit())

    # Details
    li_details = {}
    for detail in section_overview.find_all('li'):
        detail_desc = pattern_1.search(str(detail)).group(1)
        detail_info = pattern_2.search(str(detail)).group(1)
        li_details[detail_desc] = detail_info  # appending do dict

    for header in li_details:
        if header == "Powierzchnia:":
            surface.append(li_details[header].replace(',', '.')[:-3])

        if header == "Rynek:":
            market.append(li_details[header])

        if header == "Liczba pokoi:":
            rooms.append(li_details[header])

        if header == "Rok budowy:":
            build_year.append(li_details[header])

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
        location_list.append(li.split()[0])

    location_exists = False
    for _ in location_list:
        if _ in names_of_districts.names:
            location_exists = True
            district = _

    if location_exists == False:
        district = 'None'

    data = [whole_price, price_per_square, market[0], surface[0], rooms[0],
            build_year[0], finishing_condition[0], heating[0], windows[0], city[0], district]

    with open(f'{today}_{city[0]}.csv', 'a+', newline='', encoding="utf-8") as csvfile:
        data_row = csv.writer(csvfile)
        data_row.writerow(data)


start = time.perf_counter()

links = sprz_get_links.get_links_from_page()

for link in links:
    parse_links(link)

finish = time.perf_counter()
print(f'runtime: {finish-start}')
