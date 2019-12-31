from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import testa2
import csv
import re
import pandas as pd

CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
CHROMEDRIVER_PATH = 'C:/Users/Adrian.Raszka/OneDrive - SOFYNE ACTIVE TECHNOLOGY/Bureau/gitvsc/chromedriver.exe'
WINDOW_SIZE = "1200,1200"


class Home_seeker:

    def __init__(self):
        """
        Taking chrome options.
        Going on the main page.
        """

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size={}".format(WINDOW_SIZE))
        chrome_options.binary_location = CHROME_PATH
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                                options=chrome_options)
        

    def number_of_pages(self):
        """ Given city name, returns number of pages with unique offers. """

        self.city = city
        self.driver.get('https://www.otodom.pl/wynajem/mieszkanie/{}/'.format(self.city))
        self.page_source = self.driver.page_source
        self.soup = BeautifulSoup(self.page_source, 'lxml')
        self.pager = self.soup.find('ul', attrs={"class": "pager"})
        temporary_list_of_pages = []
        for li in self.pager.find_all('li'):
            temporary_list_of_pages.append(li.text)
        return temporary_list_of_pages[int(len(temporary_list_of_pages) - 2)] 
        #This just reurns value of button leading to last page of found records (returns 1 element from list)

    def list_of_links(self, city):
        """ Prepare list of links to gether all unique offers """

        self.pages_of_city = int(Home.number_of_pages())
        list_of_page_links = []
        for i in range(1, self.pages_of_city + 1):
            list_of_page_links.append('https://www.otodom.pl/wynajem/mieszkanie/{}/?page={}'.format(city, i))
        # print(list_of_page_links[:5])
        return list_of_page_links[:5]

    def get_links_from_page(self):
        ''' Take a link and retrieve all links of offers '''
        
        #Maybe multithreading would fit
        self.pages_list = Home.list_of_links(city)
        singlepage_list_of_offers = []

        for link in self.pages_list:
            self.driver.get(link)
            self.link_details = self.driver.page_source
            self.soup = BeautifulSoup(self.link_details, 'lxml')
            self.main_div = self.soup.find('div', attrs={"class": "col-md-content section-listing__row-content"})
            for article in self.main_div.find_all('article'):
                singlepage_list_of_offers.append(article['data-url'])
                # print(article['data-url'])
        # print(singlepage_list_of_offers)
        return set(singlepage_list_of_offers)
        # returning set to avoid duplicated offers 

    def detailed_data_from_offer(self):
        ''' Take a link of offer and retrieve data from that offer '''
        
        # self.links_of_offers = Home.get_links_from_page()
        # headers = ['price_per_month', 'additional_rent', 'deposit', 'surface', 'rooms', 'city', 'district']
        
        check_headers = ['Czynsz - dodatkowo:', 'Kaucja:', 'Powierzchnia:', 'Liczba pokoi:']
        price_per_month, additional_rent, deposit, surface, rooms = [], [], [], [], []
        headers_table = [price_per_month, additional_rent, deposit, surface, rooms]

        pattern_1 = re.compile(r'(?<=<li>)(.*)(?= <strong>)')
        pattern_2 = re.compile(r'(?<=<strong>)(.*)(?=</strong>)')

        self.test_set = testa2.test_set
        for link in self.test_set:
            #getting price per month of offer
            self.driver.get(link)
            price_per_month = self.driver.find_element_by_xpath('//*[@id="root"]/article/header/div[2]/div[1]/div[2]').text
            headers_table[0].append([''.join([d for d in price_per_month if d.isdigit()])])
            #getting other details of offer
            self.soup = BeautifulSoup(self.offer_details, 'lxml')
            self.details_div = self.soup.find('section', attrs={"class": "section-overview"})
            for li in self.details_div.find_all('li'):
                split_li = str(li.extract()) 
                match_1 = pattern_1.search(split_li).group(1)
                if match_1 in check_headers:
                    header_index = check_headers.index(match_1)
                    match_2 = pattern_2.search(split_li).group(1)
                    headers_table[header_index].append(match_2) #
        


        pd.DataFrame({'price_per_month':price_per_month[0], 'additional_rent':headers_table[1],'deposit':headers_table[2], 
                    'surface':headers_table[3], 'rooms':headers_table[4]}).to_csv('your.csv') #TODO: name of csv same as name of city with curret date


list_of_cities = ['krakow']

if __name__ == "__main__":
    Home = Home_seeker()
    for city in list_of_cities:
        # Home.number_of_pages()
        # Home.list_of_links(city)
        # Home.get_links_from_page()
        # Home.get_data_from_link()
        Home.detailed_data_from_offer()
