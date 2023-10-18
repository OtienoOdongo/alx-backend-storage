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
        """
        A decorator that counts the number of times
        a method is called and stores it in Redis.

        Args: method (Callable):
        The method to be wrapped and tracked.

        Returns:
        Callable: The decorated method.
        """
        key = method.__qualname__

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            """
            Wrapper function for counting method calls
            and calling the original method.

            Args:
            self: The instance of the class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

            Returns:
            Any: The result of the original method.
            """
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

        def call_history(method: Callable) -> Callable:
            """
            A decorator that stores the inputs
            and outputs of a method in Redis.

            Args:
            method (Callable):
            The method to be wrapped and tracked.

            Returns:
            Callable: The decorated method.
            """
            @wraps(method)
            def wrapper(self, *args, **kwargs):
                """
                Wrapper function for storing method
                inputs and outputs in Redis.

                Args:
                self: The instance of the class.
                *args: Positional arguments passed to the method.
                **kwargs: Keyword arguments passed to the method.

                Returns:
                Any: The result of the original method.
                """
                input_key = method.__qualname__ + ":inputs"
                output_key = method.__qualname__ + ":outputs"

                output = method(self, *args, **kwargs)

                self._redis.rpush(input_key, str(args))
                self._redis.rpush(output_key, str(output))
                return output

            return wrapper
