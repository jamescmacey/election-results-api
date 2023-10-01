"""
utils.py
"""

from pymongo.mongo_client import MongoClient
from .secrets import MONGO_CONNECTION
from .settings import ELECTION_CONFIG

def get_db_handle():
    client = MongoClient(MONGO_CONNECTION)
    db = client[ELECTION_CONFIG.get("database")]
    return db

def get_hamilton_db_handle():
    client = MongoClient(MONGO_CONNECTION)
    db = client["2022-ham-west-by-prod"]
    return db

def get_tauranga_db_handle():
    client = MongoClient(MONGO_CONNECTION)
    db = client["2022-tga-by-prod"]
    return db