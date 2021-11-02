import platform
import os
import logging
if platform.system() == 'Linux':
    from pyvirtualdisplay import Display

from metamask import Metamask
import time

pwd = os.path.abspath(os.curdir)
logging.basicConfig(filename=pwd+r'/run.log',format='%(asctime)s %(message)s', level=logging.INFO)


class VirtualDisplay:
    def __init__(self, platform) -> None:
        if platform == 'Linux':
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
    threads = []
    for i in range(1):
        threads.append(Metamask(i))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread._join()
