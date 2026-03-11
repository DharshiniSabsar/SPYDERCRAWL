from db.mongo import MongoDB
from nlp.cti_classifier import classify_threat

db = MongoDB()
raw_records = db.get_raw()

for record in raw_records:
    description = record.get("description", "")

    threat_level = classify_threat(description)

    processed = {
        "title": record.get("title"),
        "vendor": record.get("vendor"),
        "price": record.get("price"),
        "url": record.get("url"),
        "description": description,
        "threat_level": threat_level,
    }

    db.insert_processed(processed)

print("✔ Security-BERT threat classification completed")


