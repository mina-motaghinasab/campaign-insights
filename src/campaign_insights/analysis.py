"""Summarise campaign performance and turn it into recommendations."""

from campaign_insights.campaigns import PaidCampaign
from campaign_insights.metrics import format_value

MIN_PURCHASES_FOR_RELIABLE_RESULT = 30


def summarize_by_campaign(df):
    """Add up the numbers of all ads, grouped by campaign."""
    columns = ["impressions", "clicks", "enquiries", "purchases", "spent"]
    totals = df.groupby("campaign_id")[columns].sum()
    totals["ads"] = df.groupby("campaign_id").size()
    return totals


def build_campaigns(totals):
    """Turn each row of the summary table into a PaidCampaign object."""
    campaigns = []
    for campaign_id, row in totals.iterrows():
        campaign = PaidCampaign(
            name=f"Campaign {campaign_id}",
            ads=int(row["ads"]),
            impressions=int(row["impressions"]),
            clicks=int(row["clicks"]),
            enquiries=int(row["enquiries"]),
            purchases=int(row["purchases"]),
            spent=float(row["spent"]),
        )
        campaigns.append(campaign)
    return campaigns


def recommend(campaigns, order_value):
    """Return a list of plain-English recommendations.

    order_value is the average revenue of one purchase, because the
    dataset records purchases but not revenue.
    """
    messages = []
    reliable = []

    for campaign in campaigns:
        campaign_roas = campaign.return_on_ad_spend(order_value)
        roas_text = format_value(campaign_roas)

        if campaign_roas is None:
            messages.append(f"{campaign.name} has no spend, so ROAS is n/a.")
        elif campaign_roas < 1:
            messages.append(
                f"{campaign.name} loses money (ROAS {roas_text}). "
                "Consider pausing it or improving its targeting."
            )
        else:
            messages.append(f"{campaign.name} is profitable (ROAS {roas_text}).")

        if campaign.purchases < MIN_PURCHASES_FOR_RELIABLE_RESULT:
            messages.append(
                f"{campaign.name} has only {campaign.purchases} purchases, "
                "so its results are not reliable."
            )
        elif campaign_roas is not None:
            reliable.append(campaign)

    if len(reliable) >= 2:
        best = max(reliable, key=lambda c: c.return_on_ad_spend(order_value))
        worst = min(reliable, key=lambda c: c.return_on_ad_spend(order_value))
        if worst.return_on_ad_spend(order_value) < 1:
            messages.append(
                f"Test moving part of {worst.name}'s budget to {best.name}. "
                f"{best.name} spent much less, so its CPA may not hold "
                "at a larger budget."
            )

    return messages