import logging


def basic_configuration():
    logging.basicConfig(level=logging.INFO)


def get_logger(name):
    return logging.getLogger(name)


if __name__ != "__main__":
    basic_configuration()
    get_logger("logging").info("initialized logger")
