"""Load and prepare Facebook ad campaign data."""

import pandas as pd

REQUIRED_COLUMNS = [
    "xyz_campaign_id",
    "age",
    "gender",
    "Impressions",
    "Clicks",
    "Spent",
    "Total_Conversion",
    "Approved_Conversion",
]

COLUMN_NAMES = {
    "xyz_campaign_id": "campaign_id",
    "Impressions": "impressions",
    "Clicks": "clicks",
    "Spent": "spent",
    "Total_Conversion": "enquiries",
    "Approved_Conversion": "purchases",
}


def load_campaign_data(path):
    """Read the campaign CSV file and return a cleaned DataFrame.

    Raises a ValueError if a required column is missing.
    """
    df = pd.read_csv(path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.rename(columns=COLUMN_NAMES)
    return df
