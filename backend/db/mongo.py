from pymongo import MongoClient
import gridfs

class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client.spydercrawl
        self.fs = gridfs.GridFS(self.db)   # ✅ NEW

    def insert_raw(self, record):
        self.db.raw_market_data.insert_one(record)

    def get_raw(self):
        return list(self.db.raw_market_data.find({}, {"_id": 0}))

    def insert_processed(self, record):
        self.db.processed_intel.insert_one(record)

    def get_processed(self):
        return list(self.db.processed_intel.find({}, {"_id": 0}))

    # ✅ NEW: store image in GridFS
    def store_image(self, image_bytes, filename):
        return self.fs.put(image_bytes, filename=filename)