#!/usr/bin/env python3
"""
Web module with get_page function.
"""

import requests
from functools import wraps
from typing import Callable, Any
from datetime import datetime, timedelta


def cache_result(method: Callable) -> Callable[..., Any]:
    """
    A decorator to cache the result of a method with a expiration time.
    :param method: The method to be decorated.
    :return: The decorated method.
    """
    cache = {}

    @wraps(method)
    def wrapper(*args, **kwargs):
        """
        Wrapper function to cache the result of the original method.
        :param args: Arguments passed to the method.
        :param kwargs: Keyword arguments passed to the method.
        :return: The result of the original method, either from the cache or
                 by invoking the original method.
        """
        key, e_tme = args[0], timedelta(seconds=10)

        if key in cache and (datetime.now() - cache[key]['timestamp']) < e_tme:
            print(f"Using cached result for {key}")
            return cache[key]['result']
        else:
            result = method(*args, **kwargs)
            cache[key] = {'result': result, 'timestamp': datetime.now()}
            print(f"Result cached for {key}")
            return result

    return wrapper


@cache_result
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL using the requests module.
    :param url: The URL to fetch.
    :return: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
