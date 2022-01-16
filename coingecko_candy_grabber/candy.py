import os, sys, platform
from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote.webelement import WebElement
from creds import PASS, USER
from binary_locations import search_binary

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement

import logging
from logging import Logger

print (__name__)
# logging.basicConfig(filename='myapp.log',format='%(asctime)s %(message)s', level=logging.NOTSET)
# logger = logging.getLogger(__name__).addHandler(logging.StreamHandler())

logger = logging.getLogger('mylogger')
def my_handler(type, value, tb):
    logger.exception(f"Uncaught exception: {type} {value}")


# Install exception handler
sys.excepthook = my_handler

>>>>>>> fix
class Candy(webdriver.Chrome):
    def __init__(self):
        pwd = os.path.abspath(os.curdir)
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.binary_location = search_binary()
        driver_path = Service(pwd+r'\chromedriver_95.exe',)
        super(Candy, self).__init__(options=options, service=driver_path)
        self.implicitly_wait(5000)
        self.maximize_window()
        
    def __exit__(self, *args) -> None:
        print("Exiting...")
        self.quit()
        sys.exit()
    
    def __enter__(self):
        return self
        
    def open_page(self):
        self.get('https://www.coingecko.com/en')
    
    def sing_in(self):
        self.find_element_by_css_selector('a[data-target="#signInModal"]').click()

    def login(self):
        email = self.find_element_by_id('signInEmail')
        email.send_keys(USER)
        password = self.find_element_by_id('signInPassword')
        password.send_keys(PASS)
        self.find_element_by_css_selector('input[data-action="user-login-modal#submit"]').click()

    def open_page_candy(self):
        self.get('https://www.coingecko.com/account/candy?locale=en')

    def get_points(self):        
        self.find_element_by_css_selector('input[data-target="points.button"]').click()
        print("Candies grabbed !")
        self.candy_qty()

    def candys_available(self):
        content:WebElement = self.find_element_by_id('next-daily-reward-countdown-timer')
        res = content.get_attribute('innerHTML')
        print(f"No candies available...wait {res}")
    
    def candy_qty(self):
        cont: WebElement = self.find_element_by_css_selector('div[class="mb-2 font-weight-bold"]')
        res = cont.get_attribute('innerHTML')
        print(res)
