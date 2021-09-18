from functools import lru_cache, wraps
from datetime import datetime, timedelta


def split_comma(message: str) -> list:
    if not message:
        return []
    else:
        return [x.strip() for x in message.split(',')]


def tuple_split_comma(message: tuple) -> list:
    """
    Concatenates message list and split the message by comma ignoring any empty entries

    :param message:
    :return:
    """

    val = ' '.join([y.strip() for y in [''.join(x) for x in message]])
    return [x.strip() for x in val.split(',') if x.strip() != '']


def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)
        return wrapped_func
    return wrapper_cache
