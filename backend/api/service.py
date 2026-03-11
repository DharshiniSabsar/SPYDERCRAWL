from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.spydercrawl

def get_latest_records(limit=50):
    return list(db.intelligence.find().sort("timestamp", -1).limit(limit))
