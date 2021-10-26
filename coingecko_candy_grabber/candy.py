import os, sys, platform
import logging
from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote.webelement import WebElement
from creds import PASS, USER
from binary_locations import search_binary

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement


>>>>>>> fix
class Candy(webdriver.Chrome):
    def __init__(self):
        pwd = os.path.abspath(os.curdir)
        parent_dir = os.path.split(os.getcwd())[0]
        options = Options()
        # options.add_experimental_option("detach", True)
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        binary_location = search_binary()
        options.binary_location = binary_location
        driver_path = pwd+'/chromedriver'
        #print(os.environ['PATH'])
        os.environ['PATH'] += ":"+driver_path+":"
        print(os.environ['PATH'])
        try:
            print("...INIT FINISH")
            super(Candy, self).__init__(options=options)
            print("...INIT FINISH")
        except Exception as e:
            print(e)
        self.implicitly_wait(5)
        self.maximize_window()
        print("INIT FINISH")
        
    def __exit__(self, *args) -> None:
        print("Exiting...")
        self.close()
        self.quit()
        sys.exit()
    
    def __enter__(self):
        return self
        
    def open_page(self):
        self.get('https://www.coingecko.com/en')
    
    def sing_in(self):
        self.find_element_by_css_selector('a[data-target="#signInModal"]').click()
        print("singed in !")

    def login(self):
        email = self.find_element_by_css_selector("input[name='user[email]']")
        email.send_keys(USER)
        password = self.find_element_by_css_selector("input[name='user[password]']")
        password.send_keys(PASS)
        self.find_element_by_css_selector("input[type='submit']").click()

    def open_page_candy(self):
        self.get('https://www.coingecko.com/account/candy?locale=en')

    def get_points(self):        
        self.find_element_by_css_selector('input[data-target="points.button"]').click()
        print("Candies grabbed !")
        self.candy_qty()

    def candies_available(self):
        content:WebElement = self.find_element_by_id('next-daily-reward-countdown-timer')
        res = content.get_attribute('innerHTML')
        print(f"No candies available...wait {res}")

    def candy_qty(self):
        content: WebElement = self.find_element_by_css_selector('div[class="mb-2 font-weight-bold"]')
        res = content.get_attribute('innerHTML')
        print(res)
