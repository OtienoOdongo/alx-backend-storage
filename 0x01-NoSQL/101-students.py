#!/usr/bin/env python3
"""
a function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    Return all students sorted by average score.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of student documents sorted by average score
    """
    return mongo_collection.aggregate([
        {'$addFields': {'averageScore': {'$avg': "$topics.score"}}},
        {'$sort': {'averageScore': -1}}
    ])
