#!/usr/bin/env python3
"""
Nginx Logs Statistics in Python
"""


from pymongo import MongoClient


def log_stats():
    """
    Display statistics about Nginx logs stored in a MongoDB collection.

    Args:
        mongo_collection: The PyMongo collection object.

    Returns:
        None
    """
    m_client = MongoClient('mongodb://127.0.0.1:27017')
    log_collec = m_client.logs.nginx
    total_m = log_collec.count_documents({})
    get_m = log_collec.count_documents({"method": "GET"})
    post_m = log_collec.count_documents({"method": "POST"})
    put_m = log_collec.count_documents({"method": "PUT"})
    patch_m = log_collec.count_documents({"method": "PATCH"})
    delete_m = log_collec.count_documents({"method": "DELETE"})
    path_m = log_collec.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{total_m} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_m}")
    print(f"\tmethod POST: {post_m}")
    print(f"\tmethod PUT: {put_m}")
    print(f"\tmethod PATCH: {patch_m}")
    print(f"\tmethod DELETE: {delete_m}")
    print(f"{path_m} status check")


if __name__ == "__main__":
    log_stats()
