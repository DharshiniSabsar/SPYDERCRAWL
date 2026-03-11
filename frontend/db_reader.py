from pymongo import MongoClient
import pandas as pd

def load_market_data():
    client = MongoClient("mongodb://localhost:27017")
    db = client.spydercrawl

    records = list(db.raw_market_data.find({}))

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # --- Normalise for UI ---
    df.rename(
        columns={
            "title": "Title",
            "vendor": "Vendor",
            "price": "Price",
            "url": "URL",
            "description": "Description",
        },
        inplace=True
    )

    # Threat inference heuristic
    high_risk_terms = [
        "illegal",
        "black market",
        "rogue",
        "illicit",
        "underground",
        "crispr",
        "gain-of-function",
        "synthetic pathogen",
        "human experimentation",
    ]

    def infer_threat(desc):
        if not isinstance(desc, str):
            return "MEDIUM"
        return "HIGH" if any(k in desc.lower() for k in high_risk_terms) else "MEDIUM"

    df["Threat Level"] = df["Description"].apply(infer_threat)

    # Timestamp from MongoDB ObjectId
    if "_id" in df.columns:
        df["Timestamp"] = df["_id"].apply(lambda x: x.generation_time)
    else:
        df["Timestamp"] = pd.Timestamp.now()

    return df