import os
from selenium import webdriver
from creds import PASS, USER

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class Candy(webdriver.Chrome):
    def __init__(self):
        pwd = os.path.abspath(os.curdir)
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.binary_location = \
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
        driver_path = Service(pwd+r'\chromedriver_95.exe',)
        super(Candy, self).__init__(options=options, service=driver_path)
        self.implicitly_wait(100)
        self.maximize_window()
        
    
    def __exit__(self, *args) -> None:
        print("Exiting...")
        self.quit()
    
    def __enter__(self):
        return self
        
    def open_page(self):
        self.get('https://www.coingecko.com/en')
    
    def candy_icon(self):
        self.find_element_by_css_selector('a[data-target="#signInModal"]').click()
        # self.find_element_by_css_selector('a[data-toggle="modal"]').click()

    def login(self):
        email = self.find_element_by_id('signInEmail')
        email.send_keys(USER)
        password = self.find_element_by_id('signInPassword')
        password.send_keys(PASS)
        self.find_element_by_css_selector('input[data-action="user-login-modal#submit"]').click()

    def get_points(self):        
        self.find_element_by_css_selector('input[data-target="points.button"]').click()

