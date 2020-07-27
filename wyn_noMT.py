import names_of_districts
import requests
from bs4 import BeautifulSoup
import re
import csv
import concurrent.futures
import z_Get_Links
import time


check_headers = ['Czynsz - dodatkowo:',
                 'Kaucja:', 'Powierzchnia:', 'Liczba pokoi:']

pattern_1 = re.compile(r'(?<=<li>)(.*)(?= <strong>)')
pattern_2 = re.compile(r'(?<=<strong>)(.*)(?=</strong>)')


def parse_links(link):
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
    price_per_month = ''.join(
        d for d in price_per_month if d.isdigit())

    # Details
    li_details = {}
    for detail in section_overview.find_all('li'):
        detail_desc = pattern_1.search(str(detail)).group(1)
        detail_info = pattern_2.search(str(detail)).group(1)
        li_details[detail_desc] = detail_info  # appending do dict

    for header in li_details:
        if header == "Powierzchnia:":
            surface.append(li_details[header].replace(',', '.')[:-3])

        if header == "Czynsz - dodatkowo:":
            additional_rent.append(li_details[header][:-3])

        if header == "Kaucja:":

            deposit.append(li_details[header].strip()[:-3])

        if header == "Liczba pokoi:":
            rooms.append(li_details[header])

    for column in columns:
        if len(column) == 0:
            column.append('None')

    # City (pass a parameter if more cities)
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

    data = [price_per_month, additional_rent[0],
            deposit[0], surface[0], rooms[0], city[0], district]

    with open('asd.csv', 'a+', newline='', encoding="utf-8") as csvfile:
        data_row = csv.writer(csvfile)
        data_row.writerow(data)


start = time.perf_counter()

links = z_Get_Links.get_links_from_page()
for link in links:
    parse_links(link)

finish = time.perf_counter()
print(f'runtime: {finish-start}')
