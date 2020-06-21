import datetime


def get_now_timestamp():
    """Gets the now timestamp in UTC"""
    return datetime.datetime.utcnow().timestamp()
