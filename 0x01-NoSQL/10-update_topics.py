#!/usr/bin/env python3
"""
Update Topics for a School Document in Python
"""


def update_topics(mongo_collection, name, topics):
    """
    Update the topics of a school document in the specified MongoDB collection
    based on the school name.

    Args:
        mongo_collection: The PyMongo collection object.
        name (str): The school name to update.
        topics (list): The list of topics to set for the school.

    Returns:
        int: The number of documents updated.
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
