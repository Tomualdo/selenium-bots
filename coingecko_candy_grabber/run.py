import platform
import os
import logging
if platform.system() == 'Linux':
    from pyvirtualdisplay import Display

from candy import Candy
import time

pwd = os.path.abspath(os.curdir)


class VirtualDisplay:
    def __init__(self, platform) -> None:
        if platform == 'Linux':
            print('Running LINUX !!!')
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
        with Candy() as bot:
            bot.markiza()
            # bot.check_ip()
