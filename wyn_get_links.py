import requests
from bs4 import BeautifulSoup
import time
import concurrent.futures


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

    print(f'Zapisano strony z: {link}')


if __name__ == "__main__":
    start = time.perf_counter()
    all_links = list_of_links()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_links_from_page, all_links)

    print()
    finish = time.perf_counter()
    print(f'runtime: {finish-start}')
