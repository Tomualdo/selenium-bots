import platform
import os
from logger import my_logger

logger = my_logger(__name__)

if platform.system() == 'Linux':
    from pyvirtualdisplay import Display

from basic import Basic
import time

pwd = os.path.abspath(os.curdir)


class VirtualDisplay:
    def __init__(self, platform) -> None:
        if platform == 'Linux':
            print('Running LINUX !!!')
            logger.info("Running Linux")
            self.display = Display(visible=0, size=(1280,1024))
            self.display.start()
        pass

    def __enter__(self):
        if platform.system() == 'Linux':
            print("Started Virtual diplay")
            # return self.display.start()
        pass

    def __exit__(self, type, value, traceback):
        if platform.system() == 'Linux':
            print("Virtual display Stop")
            self.display.stop()
        else:
            print("no linux ?")


with VirtualDisplay(platform.system()):
    for _ in range(1):
        with Basic() as bot:
            bot.duck()
            # bot.check_ip()
