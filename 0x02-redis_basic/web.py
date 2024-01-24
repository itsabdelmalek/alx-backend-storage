#!/usr/bin/env python3
"""
Redis module with Cache class and decorators.
"""

import requests
import redis
import time
from functools import wraps
from typing import Callable


def count_calls_and_cache(url_func: Callable) -> Callable:
    """
    Decorator to count the number of times a URL is accessed.
    """
    @wraps(url_func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        result_key = f"result:{url}"

        # Increment the access count
        redis_client.incr(count_key)

        # Check if the result is already cached
        cached_result = redis_client.get(result_key)
        if cached_result:
            return cached_result.decode("utf-8")

        # If not cached, fetch the result from the URL
        response = url_func(url)

        # Cache the result with an expiration time of 10 seconds
        redis_client.setex(result_key, 10, response)

        return response

    return wrapper


@count_calls_and_cache
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL using the requests module.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Initialize Redis client
    redis_client = redis.Redis()

    # Example usage
    s_ul = "http://slowwly.robertomurray.co.uk/delay/5000/url/www.google.com"
    fast_url = "http://www.google.com"

    for _ in range(3):
        print(get_page(s_ul))

    for _ in range(3):
        print(get_page(fast_url))

    # Display access count for the slow URL
    slow_url_count = redis_client.get(f"count:{s_ul}")
    print(f"Access count for {s_ul}: {slow_url_count.decode('utf-8')}")
