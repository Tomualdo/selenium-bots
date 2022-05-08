import logging


def my_logger(name):
    logging.basicConfig(level=logging.INFO,
                        filename='log.log',
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s'
                        )
    logger = logging.getLogger(name)
    handler = logging.FileHandler('test.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
