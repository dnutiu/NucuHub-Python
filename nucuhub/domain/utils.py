import datetime


def is_string(value):
    """
        Checks if the value is a string.
    :return: True of value is a string False otherwise.
    """
    return isinstance(value, str)


def get_now_timestamp():
    """Gets the now timestamp in UTC"""
    return datetime.datetime.utcnow().timestamp()
