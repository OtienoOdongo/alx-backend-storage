#!/usr/bin/env python3
"""
a function that changes all topics
of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    Update the topics of a school document based on the name.

    Args:
        mongo_collection: The pymongo collection object.
        name: The name of the school to update.
        topics: A list of topics to set for the school.

    Returns:
        updated topics of a school document
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
