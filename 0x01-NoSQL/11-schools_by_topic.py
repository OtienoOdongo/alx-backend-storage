#!/usr/bin/env python3
"""
function that returns the list of school
having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Return a list of schools having a specific topic.

    Args:
        mongo_collection: The pymongo collection object.
        topic: The topic being searched

    Returns:
        list of school documents that have the specified topic.
    """
    return mongo_collection.find({"topics": topic})
