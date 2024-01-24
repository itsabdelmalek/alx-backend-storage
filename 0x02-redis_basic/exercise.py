#!/usr/bin/env python3
"""
Redis module with Cache class and decorators.
"""

import sys
import redis
from functools import wraps
from uuid import uuid4
from typing import Union, Optional, Callable, Any


def count_calls(method: Callable) -> Callable[..., Any]:
    """
    A decorator to count how many times methods of the Cache class are called.
    :param method: The method to be decorated.
    :return: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count method calls.
        :param self: The instance of the Cache class.
        :param args: Arguments passed to the method.
        :param kwargs: Keyword arguments passed to the method.
        :return: The result of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable[..., Any]:
    """
    A decorator to store the history of inputs and outputs for a method.
    :param method: The method to be decorated.
    :return: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store input and output history.
        :param self: The instance of the Cache class.
        :param args: Arguments passed to the method.
        :param kwargs: Keyword arguments passed to the method.
        :return: The result of the original method.
        """
        key = method.__qualname__
        i, s = f"{key}:inputs", f"{key}:outputs"

        self._redis.rpush(i, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(s, str(result))
        return result

    return wrapper


class Cache:
    """
    Cache class for storing and retrieving data in Redis with decorators.
    """

    def __init__(self):
        """
        Constructor of the Cache class, initializes a Redis instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis with a randomly generated key.
        :param data: The data to be stored.
        :return: The randomly generated key used for storage.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> Union[str, bytes, int, None]:
        """
        Retrieve data from Redis based on the provided key and apply the
        optional conversion function.
        :param key: The key used to retrieve data from Redis.
        :param fn: A callable function to convert the data. Defaults to None.
        :return: The retrieved data, optionally converted using fn.
        """
        data = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_int(self: bytes) -> int:
        """
        Retrieve and automatically convert data from Redis as an integer.
        :return: The retrieved data as an integer.
        """
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """
        Retrieve and automatically convert data from Redis as a UTF-8 string.
        :return: The retrieved data as a UTF-8 string.
        """
        return self.decode("utf-8")
