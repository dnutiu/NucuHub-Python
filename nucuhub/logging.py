import logging

from nucuhub.config import ApplicationConfig


def level_name_to_level(level_name: str) -> int:
    if not level_name:
        level_name = ""
    log_levels = {
        "CRITICAL": 50,
        "FATAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10,
    }
    return log_levels.get(level_name.upper(), 20)


def basic_configuration():
    logging_level = level_name_to_level(ApplicationConfig.LOGGING_LEVEL)
    logging.basicConfig(level=logging_level)


def get_logger(name):
    return logging.getLogger(name)


def get_null_logger():
    logger_ = logging.getLogger("NullLogger")
    logger_.addHandler(logging.NullHandler())
    return logger_


if __name__ != "__main__":
    basic_configuration()
    logger = get_logger("logging")
    logger.info(f"initialized logger, {logger.getEffectiveLevel()}")
