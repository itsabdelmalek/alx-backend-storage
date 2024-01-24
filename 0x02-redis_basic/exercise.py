#!/usr/bin/env python3
"""
This is the main module for the exercise.

It includes a Cache class with various methods and decorators.

Author: Your Name
"""

import redis
import uuid
from typing import Callable, Optional, Union

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    import functools
    
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.
    """
    import functools
    
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        
        # Append input arguments to Redis list
        self._redis.rpush(input_key, str(args))
        
        # Execute the original method to get the output
        output = method(self, *args, **kwargs)
        
        # Append the output to Redis list
        self._redis.rpush(output_key, str(output))
        
        return output
    
    return wrapper

class Cache:
    """
    Cache class with methods for storing, retrieving, and counting calls.
    """
    def __init__(self):
        """
        Initialize the Cache with a Redis instance and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key and optional conversion function.
        """
        result = self._redis.get(key)
        if result is not None and fn is not None:
            return fn(result)
        return result

    def get_str(self, key: str) -> Optional[str]:
        """
        Automatically parametrize Cache.get with the correct conversion function for strings.
        """
        return self.get(key, fn=lambda x: x.decode("utf-8") if x else None)

    def get_int(self, key: str) -> Optional[int]:
        """
        Automatically parametrize Cache.get with the correct conversion function for integers.
        """
        return self.get(key, fn=lambda x: int(x) if x else None)

def replay(func: Callable) -> None:
    """
    Display the history of calls for a particular function.
    """
    key = func.__qualname__
    input_key = key + ":inputs"
    output_key = key + ":outputs"
    
    inputs = [eval(args) for args in cache._redis.lrange(input_key, 0, -1)]
    outputs = [eval(output) for output in cache._redis.lrange(output_key, 0, -1)]
    
    print(f"{key} was called {len(inputs)} times:")
    for args, output in zip(inputs, outputs):
        print(f"{key}(*{args}) -> {output}")
