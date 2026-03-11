import pandas as pd

def get_market_data():
    return pd.DataFrame([
        {
            "Title": "CRISPR Gene Editing Kit",
            "Vendor": "BioLabX",
            "Price": "$1200",
            "Threat Level": "HIGH"
        },
        {
            "Title": "Synthetic DNA Samples",
            "Vendor": "GeneMarket",
            "Price": "$800",
            "Threat Level": "MEDIUM"
        },
        {
            "Title": "Lab Equipment Bundle",
            "Vendor": "OpenBio",
            "Price": "$500",
            "Threat Level": "LOW"
        }
    ])
