#!/usr/bin/env python3
"""A function that lists all documents in a MongoDB collection"""


def list_all(mongo_collection):
    """
    A function that lists all documents in a MongoDB collection.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of documents in the collection,
        or an empty list if there are no documents.
    """
    if mongo_collection.count() == 0:
        return []
    else:
        return mongo_collection.find()
