from candy import Candy

import time

with Candy() as bot:
    bot.open_page()
    bot.candy_icon()
    bot.login()
    bot.candy_icon()
    bot.get_points()
    


