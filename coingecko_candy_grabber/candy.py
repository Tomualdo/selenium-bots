import os, sys, platform
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from creds import PASS, USER
from binary_locations import search_binary

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement



class Candy(webdriver.Chrome):
    def __init__(self):
        pwd = os.path.abspath(os.curdir)
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.binary_location = search_binary()
        driver_path = Service(pwd+r'\chromedriver_94.exe',)
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

    def candys_available(self):
        try:
            content:WebElement = self.find_element_by_id('next-daily-reward-countdown-timer')
            res = content.get_attribute('innerHTML')
            print(f"No candies available...wait {res}")
        except:
            print("There are candies available")
            self.get_points()
