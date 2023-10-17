#!/usr/bin/env python3
"""
a function that inserts a a new document
in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into the provided MongoDB collection.

    Args:
    mongo_collection:
    The collection where the document will be inserted.
    **kwargs:
    Keyword arguments representing
    the fields and values for the new document.

    Returns:
    str: The new _id of the inserted document.
    """
    new_document = mongo_collection.insert_one(kwargs)

    return new_document.inserted_id
