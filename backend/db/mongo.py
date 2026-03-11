from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client.spydercrawl

    def insert_raw(self, record):
        self.db.raw_market_data.insert_one(record)

    def get_raw(self):
        return list(self.db.raw_market_data.find({}, {"_id": 0}))

    def insert_processed(self, record):
        self.db.processed_intel.insert_one(record)

    def get_processed(self):
        return list(self.db.processed_intel.find({}, {"_id": 0}))
