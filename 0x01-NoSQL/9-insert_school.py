#!/usr/bin/env python3
"""
Insert School Document in Python
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into the specified MongoDB collection
    based on keyword arguments.

    Args:
        mongo_collection: The PyMongo collection object.

    Returns:
        ObjectId: The new _id of the inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
