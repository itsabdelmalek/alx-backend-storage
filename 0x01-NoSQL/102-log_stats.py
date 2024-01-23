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
        list of sorted ip adresses
    """
    m_client = MongoClient('mongodb://127.0.0.1:27017')
    log_collect = m_client.logs.nginx
    total_m = log_collect.count_documents({})
    get_m = log_collect.count_documents({"method": "GET"})
    post_m = log_collect.count_documents({"method": "POST"})
    put_m = log_collect.count_documents({"method": "PUT"})
    patch_m = log_collect.count_documents({"method": "PATCH"})
    delete_m = log_collect.count_documents({"method": "DELETE"})
    path_m = log_collect.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{total_m} logs")
    print("Methods:")
    print(f"\tmethod GET: {get_m}")
    print(f"\tmethod POST: {post_m}")
    print(f"\tmethod PUT: {put_m}")
    print(f"\tmethod PATCH: {patch_m}")
    print(f"\tmethod DELETE: {delete_m}")
    print(f"{path_m} status check")
    print("IPs:")
    sorted_ipss = log_collect.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    i = 0
    for j in sorted_ipss:
        if i == 10:
            break
        print(f"\t{j.get('_id')}: {j.get('count')}")
        i += 1


if __name__ == "__main__":
    log_stats()
