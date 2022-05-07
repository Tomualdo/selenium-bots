import os, sys, platform
import logging
import pickle as pkl
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from creds import PASS, USER
from binary_locations import search_binary
from fake_useragent import UserAgent

from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement


class Candy(webdriver.Chrome):
    def __init__(self):
        self.pwd = os.path.abspath(os.curdir)
        parent_dir = os.path.split(os.getcwd())[0]
        options = Options()
        ua = UserAgent()
        userAgent = ua.random
        print(f"Using fake user agent: {userAgent}")
        # options.add_experimental_option("detach", True)
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f'user-agent={userAgent}')
        binary_location = search_binary()
        options.binary_location = binary_location
        #options.binary_location = r"/usr/bin/firefox"
        driver_path = parent_dir
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
        #self.maximize_window()
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
        #email = self.find_element_by_css_selector("input[name='user[email]']")
        print("email search")
        page_source = self.page_source
        if "resolve_captcha_headline" in page_source:
            print("found captcha !!! exiting...")
            self.save_cookies(self.get_cookies())
            #exit()

        #print(self.page_source)
        email = self.find_element_by_css_selector("input[name='user[email]']")
        email.send_keys(USER)
        print("emails filled")
        password = self.find_element_by_css_selector("input[name='user[password]']")
        password.send_keys(PASS)
        print("fields was filled...")
        self.find_element_by_css_selector("input[type='submit']").click()
        #self.find_element_by_css_selector("button[type='submit']").click()
        print("creds submitted...")

    def open_page_candy(self):
        self.get('https://www.coingecko.com/account/candy?locale=en')
        print("page opened...")

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
    
    def save_cookies(self, object):
        print(f"saving cookies into {self.pwd}/my_cookies")
        with open(f"{self.pwd}/my_cookies", 'wb') as my_file:
            pkl.dump(object, my_file)

    def load_cookies(self):
        print("***************")
        if os.path.isfile(f"{self.pwd}/mod_cookies"):
            print("Found new cookies...try loading...")
            with open(f"{self.pwd}/mod_cookies", "rb") as f:
                new_cookies = pkl.load(f)
            for cookie in new_cookies:
                print(f"loadin cookie {cookie}")
                self.add_cookie(cookie)
