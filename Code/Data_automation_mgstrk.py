from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import testa2
import csv

CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
CHROMEDRIVER_PATH = 'C:/Users/Adrian.Raszka/OneDrive - SOFYNE ACTIVE TECHNOLOGY/Bureau/gitvsc/chromedriver.exe'
WINDOW_SIZE = "1200,1200"


class Home_seeker:

    def __init__(self):
        """
        Taking chrome options.
        Going on the main page.
        Will go with headless in future.
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

    def get_data_from_link(self):
        ''' Take a link of offer and retrieve data from that offer '''
        
        # self.links_of_offers = Home.get_links_from_page()
        # print(self.links_of_offers)
        headers = ['price per month']
        self.test_set = testa2.test_set
        with open('text.csv', 'w', encoding='utf-8', newline='') as fp:
            self.writer = csv.writer(fp)
            self.writer.writerow(headers)
            for link in self.test_set:
                self.driver.get(link)
                price_per_month = self.driver.find_element_by_xpath('//*[@id="root"]/article/header/div[2]/div[1]/div[2]').text
                self.writer.writerow([price_per_month])

    def save_data_info_file(self):
        ''' Take retrieved data and put into some datafile '''
        pass


list_of_cities = ['krakow']

if __name__ == "__main__":
    Home = Home_seeker()
    for city in list_of_cities:
        # Home.number_of_pages()
        # Home.list_of_links(city)
        # Home.get_links_from_page()
        Home.get_data_from_link()