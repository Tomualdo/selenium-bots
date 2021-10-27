import os, sys, time, secrets, binascii, hashlib
from wordlist import words as wordlist
from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webelement import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


import logging
logger = logging.getLogger('metamask.log')
# logging.basicConfig(filename='metamask.log',
#                     format='%(asctime)s %(message)s',
#                     level=logging.ERROR)
def my_handler(type, value, tb):
    logger.exception(f"Uncaught exception: {type} {value}")


# Install exception handler
sys.excepthook = my_handler

class Metamask(webdriver.Chrome):
    def __init__(self):
        pwd = os.path.abspath(os.curdir)
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_extension(pwd+r'/metamask_extension_10_3_0_0.crx')
        driver_path = Service(pwd+r'\chromedriver_95.exe',)
        super(Metamask, self).__init__(options=options, service=driver_path)
        self.implicitly_wait(5)
        self.maximize_window()

    def __exit__(self, *args) -> None:
        print("Exiting...")
        self.quit()
        sys.exit()

    def __enter__(self):
        return self
    
    @staticmethod
    def gen_wordlist(words: int=15, previous_seed: int=None ):
        """Generate seed according BIP39"""
        accepted_words = {12:128, 15:160, 18:192, 21:224, 24:256}
        if words is not None and words not in accepted_words.keys():
            raise ValueError(f"words count did not match required count {accepted_words.keys()}")
        bits = accepted_words.get(words)
        if not previous_seed:
            start_seed = secrets.randbits(bits)
        else:
            start_seed = previous_seed
        s = bin(start_seed)[2:].zfill(bits)
        h=int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
        entrophy = binascii.hexlify(h).decode()
        entrophy_sha = binascii.hexlify(hashlib.sha256(h).digest()).decode()
        s_ = s
        chsum_len = accepted_words.get(words) // 32
        chsum = bin(int(entrophy_sha,16))[2::].zfill(256)
        chsum = chsum[:chsum_len]
        s_ += chsum
        seed = []
        for x,i in enumerate(range(0,len(s_),11)):
            # print(f"{int(s_[i:i+11],2)} = {k.words[int(s_[i:i+11],2)]}")
            seed.append(wordlist[int(s_[i:i+11],2)])
        print(f"{s=}\n{chsum=}\n{seed=}\n{entrophy=}\n{start_seed=}\n{len(seed)=}")
        return seed, entrophy, start_seed

    def open_page(self):
        self.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        # remove unnecessary tabs
        tabs = len(self.window_handles)
        if tabs >=2:
            for idx in range(tabs):
                self.switch_to.window(self.window_handles[-idx])
                self.close()
                self.switch_to.window(self.window_handles[idx])
                if len(self.window_handles) == 1:
                    break
    
    def get_started(self):
        self.find_element_by_css_selector('button[class="button btn--rounded btn-primary first-time-flow__button"]').click()
        self.find_element_by_css_selector('button[class="button btn--rounded btn-primary first-time-flow__button"]').click()
        self.find_element_by_css_selector('button[data-testid="page-container-footer-next"]').click()

    def import_wallet(self):
        time.sleep(5000)
        self.seed, self.entrophy, self.previous_seed = self.gen_wordlist(12)
        inputs = self.find_elements_by_xpath('//input')
        inputs[0].send_keys(' '.join(self.seed))
        self.find_element_by_css_selector('.first-time-flow__checkbox').click()
        inputs[1].send_keys('qwertyqwerty')
        inputs[2].send_keys('qwertyqwerty')
        self.find_element_by_css_selector('.first-time-flow__terms').click()
        self.find_element_by_css_selector('.first-time-flow__button').click()
        time.sleep(2)
        self.find_element_by_css_selector('.first-time-flow__button').click()
        # self.find_element_by_css_selector('.popover-header__button').click()
    
    def get_values(self) -> float:
        time.sleep(0.3)
        balance = self.find_element_by_css_selector('.eth-overview__secondary-balance').find_element_by_css_selector('.currency-display-component__text')
        val = balance.get_attribute('innerHTML')
        print(val+self.find_element_by_css_selector('.eth-overview__secondary-balance').find_element_by_css_selector('.currency-display-component__suffix').get_attribute('innerHTML'))
        return float(val[1:])

    def lock_wallet(self, restore=False):
        print("Locking...")
        if not restore:
            self.find_element_by_id('popover-content')
            self.find_element_by_css_selector('.popover-header__button').click()
        # time.sleep(5)
        # self.switch_to.frame(self.find_elements_by_tag_name('iframe')[0])
        self.find_element_by_css_selector('.account-menu__icon').click()
        self.find_element_by_css_selector('.account-menu__lock-button').click()
        self.find_element_by_css_selector('.unlock-page__link--import').click()
    
    def restore_wallet(self):
        self.seed, self.entrophy, self.previous_seed = self.gen_wordlist(12)
        inputs = self.find_elements_by_xpath('//input')
        inputs[0].send_keys(' '.join(self.seed))
        print("seed wrote...")
        inputs[1].send_keys('qwertyqwerty')
        print("pass1...")
        inputs[2].send_keys('qwertyqwerty')
        print("pass2...")
        # time.sleep(2)
        self.find_element_by_css_selector('.first-time-flow__button').click()

# list-item__subheading
# currency-display-component__text
# currency-display-component eth-overview__secondary-balance
with Metamask() as a:
    a.open_page()
    a.get_started()
    a.import_wallet()
    restore = False
    while True:
        if a.get_values() == 0:
            a.lock_wallet(restore)
            a.restore_wallet()
            restore=True
        else:
            print("something found !")
            sys.exit(0)
        


    time.sleep(500)