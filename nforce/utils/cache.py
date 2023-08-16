import functools
import time


def lru_cache_ttl(maxsize=128, typed=False, ttl=3600):
    """
    lru_cache decorator with ttl

    :param ttl: lru_cache ttl
    :param maxsize: If *maxsize* is set to None, the LRU features are disabled and
    the cache can grow without bound.
    :param typed: If *typed* is True, arguments of different types will be cached
    separately. For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.
    """

    def lru_cache_decorator(func):
        @functools.lru_cache(maxsize, typed)
        def cached_method(expiration, *args, **kwargs):
            result = func(*args, **kwargs)
            return result

        def wrapper(*args, **kwargs):
            expiration = round(time.time() // ttl)
            return cached_method(expiration, *args, **kwargs)

        return wrapper

    return lru_cache_decorator
