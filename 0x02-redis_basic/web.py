#!/usr/bin/env python3
"""
Redis module with Cache class and decorators.
"""

import redis
import requests
from typing import Callable
from functools import wraps

redis = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """
    wrapping decortors for requests
    """

    @wraps(fn)
    def wrapper(url):
        """
        wrapping fucntors for requests
        """
        redis.incr(f"count:{url}")
        cash_resp = redis.get(f"cached:{url}")
        if cash_resp:
            return cash_resp.decode('utf-8')
        rslt = fn(url)
        redis.setex(f"cached:{url}", 10, rslt)
        return rslt

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """
    gets the page
    """
    resp = requests.get(url)
    return resp.text
