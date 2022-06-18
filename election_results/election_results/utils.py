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