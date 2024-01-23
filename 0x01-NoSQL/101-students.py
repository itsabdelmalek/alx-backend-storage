#!/usr/bin/env python3
"""
Top Students by Average Score in Python
"""


def top_students(mongo_collection):
    """
    Return all students sorted by average score.

    Args:
        mongo_collection: The PyMongo collection object.

    Returns:
        list: A list of students, sorted by average score.
    """
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
