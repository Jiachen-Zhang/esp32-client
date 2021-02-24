import logging


def get_logger(name: str):
    print('init logger')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s %(filename)s[:%(lineno)d]',
                        datefmt='%H:%M:%S')
    return logging.getLogger(name)


log = get_logger(__name__)
