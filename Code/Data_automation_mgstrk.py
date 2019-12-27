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

        self.city = city
        self.driver.get('https://www.otodom.pl/wynajem/mieszkanie/{}/'.format(city))
        self.page_source = self.driver.page_source
        self.soup = BeautifulSoup(self.page_source, 'lxml')
        return self.soup

    def number_of_pages(self):
        """ Given city name, returns number of pages with unique offers. """

        self.soup = Home.source_of_homepage(self.city)
        self.pager = self.soup.find('ul', class_="pager")
        temporary_list = []
        for li in self.pager.find_all('li'):
            temporary_list.append(li.text)
        return temporary_list[int(len(temporary_list) - 2)]

    def get_links_from_page(self):
        """ Getting links for unique offers. """
        
        print(Home.number_of_pages())
            

        # print(self.soup.prettify())
        # self.main_div = self.soup.find('div', class_="col-md-content section-listing__row-content")
        # for self.h3 in self.main_div.fina_all('h3'):
        #     self.links = h3.fina_all('a')
        #     for self.a in self.links:
        #         print(self.a.text)
        

if __name__ == "__main__":
    Home = Home_seeker()
    Home.source_of_homepage('krakow')
    Home.number_of_pages()
    Home.get_links_from_page()