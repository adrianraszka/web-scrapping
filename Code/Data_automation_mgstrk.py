from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def OD_search(city):
    # paths
    CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    CHROMEDRIVER_PATH = 'C:/Users/Adrian.Raszka/OneDrive - SOFYNE ACTIVE TECHNOLOGY/Bureau/gitvsc/chromedriver.exe'
    # Window size
    WINDOW_SIZE = "1200,1200"
    # Chrome Options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size={}".format(WINDOW_SIZE))
    chrome_options.binary_location = CHROME_PATH
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                            options=chrome_options)
    driver.get('https://www.otodom.pl/wynajem/mieszkanie/{}/'.format(city))

OD_search('krakow')