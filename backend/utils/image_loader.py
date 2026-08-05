import gridfs
from pymongo import MongoClient
from PIL import Image
import io

client = MongoClient("mongodb://localhost:27017")
db = client.spydercrawl
fs = gridfs.GridFS(db)

def load_image_from_db(image_id):
    try:
        image_bytes = fs.get(image_id).read()
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except:
        return None