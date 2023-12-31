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
    A decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator to record input and output history of a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ':inputs'
        output_key = method.__qualname__ + ':outputs'
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output

    return wrapper


def replay(fn: Callable) -> None:
    """
    Display the history of calls of a particular function.

    Args:
        fn (Callable): The function whose history to display.
    """
    fn_name = fn.__name__
    input_key = f'{fn_name}:inputs'
    output_key = f'{fn_name}:outputs'
    cache = redis.Redis()

    if not cache.exists(input_key):
        print(f"{fn_name} was never called.")
        return

    call_count = cache.llen(input_key)
    print(f"{fn_name} was called {call_count} times:")

    inputs = [
        cache.lindex(input_key, i).decode('utf-8')
        for i in range(call_count)
    ]
    outputs = [
        cache.lindex(output_key, i).decode('utf-8')
        for i in range(call_count)
    ]

    for i, o in zip(inputs, outputs):
        print(f"{fn_name}(*{i}) -> {o}")
