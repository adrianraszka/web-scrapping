from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


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
        
    def source_of_homepage(self, city):
        """ Returns source code of page """

        page = 1
        self.city = city
        self.driver.get('https://www.otodom.pl/wynajem/mieszkanie/{}/?page={}'.format(city, page))
        self.page_source = self.driver.page_source
        self.soup = BeautifulSoup(self.page_source, 'lxml')
        page+=1
        return self.soup

    def number_of_pages(self):
        """ Given city name, returns number of pages with unique offers. """

        self.soup = Home.source_of_homepage(self.city)
        self.pager = self.soup.find('ul', class_="pager")
        temporary_list_of_pages = []
        for li in self.pager.find_all('li'):
            temporary_list_of_pages.append(li.text)
        return temporary_list_of_pages[int(len(temporary_list_of_pages) - 2)]

    def list_of_links(self, city):
        """ Prepare list of links to gether all unique offers """

        self.pages_of_city = int(Home.number_of_pages())
        list_of_page_links = []
        for i in range(1, self.pages_of_city + 1):
            list_of_page_links.append('https://www.otodom.pl/wynajem/mieszkanie/{}/?page={}'.format(self.city, i))
        # print(list_of_page_links)
        return list_of_page_links[:5]

    def get_links_from_page(self):
        ''' Take a link and retrieve all links of offers '''
        
        #Maybe multithreading would fit

        temporary_list_of_offers = []
        for page_link in Home.list_of_links(self.city):
            self.soup = Home.source_of_homepage(self.city)
            self.main_div = self.soup.find('div', attrs={"class": "col-md-content section-listing__row-content"})
            for article in self.main_div.find_all('article'):
                temporary_list_of_offers.append(article['data-url'])
        print(temporary_list_of_offers)
        return temporary_list_of_offers


    def get_data_from_link(self):
        ''' Take a link of offer and retrieve data from that offer '''
        pass

    def save_data_info_file(self):
        ''' Take retrieved data and put into some datafile '''
        pass


list_of_cities = ['krakow']

if __name__ == "__main__":
    Home = Home_seeker()
    for city in list_of_cities:
        Home.source_of_homepage(city)
        Home.number_of_pages()
        Home.list_of_links(city)
        Home.get_links_from_page()