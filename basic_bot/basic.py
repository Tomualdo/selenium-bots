import os, sys, platform, subprocess
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

from logger import my_logger

logger = my_logger(__name__)

class Basic(webdriver.Chrome):
    def __init__(self):

        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        my_proxy = "http://192.168.100.10:8118"
        prox.http_proxy = my_proxy
        # prox.socks_proxy = my_proxy
        prox.ssl_proxy = my_proxy

        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)

        pwd = os.path.abspath(os.curdir)
        parent_dir = os.path.split(os.getcwd())[0]
        options = Options()
        ua = UserAgent()
        user_agent = ua.random
        print(f"Using fake user agent: {user_agent}")
        # options.add_experimental_option("detach", True)
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument(f'user-agent={user_agent}')
        # binary_location = search_binary()
        binary_location = f"/usr/bin/brave-browser"
        options.binary_location = binary_location
        driver_path = parent_dir
        # print(os.environ['PATH'])
        if f":{driver_path}" not in os.environ['PATH']:
            os.environ['PATH'] += ":" + driver_path
        else:
            print("PATH ALREADY UPDATED")
        try:
            super(Basic, self).__init__(options=options,
                                        desired_capabilities=capabilities)
            self.implicitly_wait(5)
            self.maximize_window()
            print("...INIT FINISH")
            logger.info("init finished")
        except Exception as e:
            print(f"{e}")
            if platform.system() == 'Linux':
                subprocess.Popen(['pkill', 'brave'])

    def __exit__(self, *args) -> None:
        print("Exiting...")
        for arg in args:
            print(arg)
        self.close()
        self.quit()
        # sys.exit()

    def __enter__(self):
        return self

    def check_ip(self):
        self.get('http://checkip.dyndns.org/')
        return print(self.page_source)

    def duck(self):
        self.get('https://www.duckdns.org/')
        # return print(self.page_source)
