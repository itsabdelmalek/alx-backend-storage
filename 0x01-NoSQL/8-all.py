#!/usr/bin/env python3
"""
MongoDB Python Script

This script contains a function to list all documents in a MongoDB collection.
"""


def list_all(mongo_collection):
    """
    List all documents in the specified MongoDB collection.

    Args:
        mongo_collection : The PyMongo collection object.

    Returns:
        list: A list containing all documents in the collection.
              Returns an empty list if no documents are present.
    """
    return list(mongo_collection.find())
