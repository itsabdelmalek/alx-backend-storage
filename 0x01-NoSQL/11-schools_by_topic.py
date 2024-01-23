#!/usr/bin/env python3
"""
Get Schools by Topic in Python
"""


def schools_by_topic(mongo_collection, topic):
    """
    Get a list of schools from the specified MongoDB collection
    based on a specific topic.

    Args:
        mongo_collection: The PyMongo collection object.
        topic (str): The topic to search for.

    Returns:
        list: A list of dictionaries representing school documents
        with the specified topic.
    """
    return mongo_collection.find({"topics": topic})
