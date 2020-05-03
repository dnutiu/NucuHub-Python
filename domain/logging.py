import logging


def get_logger(name):
    return logging.getLogger(name)


if __name__ != "__main__":
    logging.basicConfig()
    get_logger("logging").info("initialized logger")
