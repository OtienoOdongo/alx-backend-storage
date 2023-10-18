#!/usr/bin/env python3
"""writing a string in redis"""


import redis
import uuid
from typing import Union


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
