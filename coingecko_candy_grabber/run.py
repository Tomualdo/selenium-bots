from candy import Candy

import time

with Candy() as bot:
    bot.open_page()
    bot.sing_in()
    bot.login()
    bot.open_page_candy()
    bot.candys_available()
    # bot.get_points()
    


