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
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size={}".format(WINDOW_SIZE))
        chrome_options.binary_location = CHROME_PATH
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                                options=chrome_options)
        

    def run_thourgh_pages(self, city):
        """
        Getting all page links form certain city.
        Given 24 records on the page, run through all pages to access every record.
        """

        self.city = city
        self.driver.get('https://www.otodom.pl/wynajem/mieszkanie/{}/'.format(city))
        html_city = self.driver.page_source
        return html_city

    def get_links_from_page(self):
        """ Getting links for unique offers. """
        
        self.soup = BeautifulSoup(krakow.run_thourgh_pages(self.city), 'lxml')
        
        for h3 in self.soup.find_all('h3'):
            print(h3.text)

        # print(self.soup.prettify())
        # self.main_div = self.soup.find('div', class_="col-md-content section-listing__row-content")
        # for self.h3 in self.main_div.fina_all('h3'):
        #     self.links = h3.fina_all('a')
        #     for self.a in self.links:
        #         print(self.a.text)
        





if __name__ == "__main__":
    krakow = Home_seeker()
    krakow.run_thourgh_pages('krakow')
    krakow.get_links_from_page()