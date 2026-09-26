"""Load and prepare Facebook ad campaign data."""

import pandas as pd

NUMERIC_COLUMNS = [
    "Impressions",
    "Clicks",
    "Spent",
    "Total_Conversion",
    "Approved_Conversion",
]

REQUIRED_COLUMNS = ["xyz_campaign_id"] + NUMERIC_COLUMNS

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

    Raises a ValueError if a required column is missing, or if a numeric
    column contains missing, non-numeric or negative values.
    """
    df = pd.read_csv(path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().any():
            raise ValueError(f"Column '{col}' has missing or non-numeric values")
        if (df[col] < 0).any():
            raise ValueError(f"Column '{col}' has negative values")

    df = df.rename(columns=COLUMN_NAMES)
    return df
