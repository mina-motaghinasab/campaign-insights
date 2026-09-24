"""Summarise campaign performance and turn it into recommendations."""

from campaign_insights.campaigns import PaidCampaign
from campaign_insights.metrics import roas

MIN_ADS_FOR_RELIABLE_RESULT = 100


def summarize_by_campaign(df):
    """Add up the numbers of all ads, grouped by campaign."""
    columns = ["impressions", "clicks", "spent", "purchases"]
    totals = df.groupby("campaign_id")[columns].sum()
    totals["ads"] = df.groupby("campaign_id").size()
    return totals


def build_campaigns(totals):
    """Turn each row of the summary table into a PaidCampaign object."""
    campaigns = []
    for campaign_id, row in totals.iterrows():
        campaign = PaidCampaign(
            name=f"Campaign {campaign_id}",
            impressions=row["impressions"],
            clicks=row["clicks"],
            purchases=row["purchases"],
            spent=row["spent"],
        )
        campaigns.append(campaign)
    return campaigns


def recommend(totals, campaigns, order_value):
    """Return a list of plain-English recommendations.

    order_value is the average revenue of one purchase, because the
    dataset records purchases but not revenue.
    """
    messages = []
    reliable_roas = {}

    for ads, campaign in zip(totals["ads"], campaigns):
        revenue = campaign.purchases * order_value
        campaign_roas = roas(revenue, campaign.spent)

        if campaign_roas < 1:
            messages.append(
                f"{campaign.name} loses money (ROAS {campaign_roas:.2f}). "
                "Consider pausing it or improving its targeting."
            )
        else:
            messages.append(
                f"{campaign.name} is profitable (ROAS {campaign_roas:.2f})."
            )

        if ads < MIN_ADS_FOR_RELIABLE_RESULT:
            messages.append(
                f"{campaign.name} has only {ads} ads, "
                "so its results are less reliable."
            )
        else:
            reliable_roas[campaign.name] = campaign_roas

    if len(reliable_roas) >= 2:
        best = max(reliable_roas, key=reliable_roas.get)
        worst = min(reliable_roas, key=reliable_roas.get)
        messages.append(f"Shift budget from {worst} to {best}.")

    return messages