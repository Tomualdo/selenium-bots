from candy import Candy
import logging
import time

logging.basicConfig(filename='run.log',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)

with Candy() as bot:
    bot.open_page()
    bot.sing_in()
    bot.login()
    bot.open_page_candy()
    # bot.candys_available()
    # bot.get_points()
    bot.candy_qty()


