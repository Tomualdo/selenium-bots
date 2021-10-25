import platform
if platform.system() == 'Linux':
    from pyvirtualdisplay import Display

from candy import Candy


import time

class VirtualDisplay:
    def __init__(self, platform) -> None:
        if platform == 'Linux':
            self.display = Display(visible=0, size=(1650,1200))
            self.display.start()
        pass

    def __enter__(self):
        if platform == 'Linux':
            print("Started Virtual diplay")
            # return self.display.start()
        pass

    def __exit__(self, type, value, traceback):
        if platform == 'Linux':
            self.display.stop()
            print("Virtual display Stop")
        pass

with VirtualDisplay(platform.system()):
    with Candy() as bot:
        bot.open_page()
        bot.sing_in()
        bot.login()
        bot.open_page_candy()
        bot.candys_available()
        # bot.get_points()
