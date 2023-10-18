#!/usr/bin/env python3
"""a redis exercise questions answered in a single file"""


import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache:
    """
    A simple caching class that uses Redis to store and retrieve data.

    Args:
        None

    Attributes:
        _redis (redis.Redis): An instance of the Redis client.

    Methods:
        __init__: Initializes the Redis client and flushes the database.
        store: Stores data in Redis using a random key and returns that key.

    Usage:
        cache = Cache()
        key = cache.store()
    """

    def __init__(self):
        """
        Initializes the Redis client and flushes the Redis database.
        Then create a Redis client instance and flush the database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis using a random key and returns the key.

        Args:
            data (Union[str, bytes, int, float]):
            The data to be stored in the cache.

        Returns:
            str: The random key used to store the data in Redis.
        """
        random_key = str(uuid.uuid4())

        """Store the input data in Redis using the random key"""
        if isinstance(data, (int, float)):
            data = str(data)
        self._redis.set(random_key, data)

        return random_key

    def get(self, key: str, fn: Callable = None):
        """
        Retrieve data from Redis using a key
        and apply a conversion function.

        Args:
            key (str): The key to retrieve data from Redis.
            fn (Callable, optional):
            a callable function to convert the data back to the desired format.

        Returns:
            Union[str, bytes, int, float]:
            The retrieved data after applying the conversion function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str):
        """
        Retrieve and return a string from Redis using a key.

        Args:
            key (str): The key to retrieve a string from Redis.

        Returns:
            str: The retrieved string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str):
        """
        Retrieve and return an integer from Redis using a key.

        Args:
            key (str): The key to retrieve an integer from Redis.

        Returns:
            int: The retrieved integer.
        """
        return self.get(key, fn=int)

    def count_calls(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            """Incrementing the count for the method"""
            key = f"{method.__qualname__}_count"
            count = self._redis.incr(key)
            """Executing the original method and return its result"""
            result = method(self, *args, **kwargs)
            return result

        return wrapper
