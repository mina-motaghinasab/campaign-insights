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


def intervals_overlap(first, second):
    """Return True if two (low, high) intervals share any values."""
    return first[0] <= second[1] and second[0] <= first[1]


def compare_approval(small, reference):
    """Explain whether a small campaign's approval rate differs clearly."""
    small_interval = small.approval_interval()
    reference_interval = reference.approval_interval()
    if small_interval is None or reference_interval is None:
        return None

    first = f"{small.name}'s approval rate (95% CI {small.approval_interval_text()})"
    second = f"{reference.name}'s ({reference.approval_interval_text()})"
    if intervals_overlap(small_interval, reference_interval):
        return f"{first} overlaps with {second}, so there is no clear difference."
    if small_interval[0] > reference_interval[1]:
        return f"{first} is clearly higher than {second}."
    return f"{first} is clearly lower than {second}."


def recommend(campaigns, order_value):
    """Return a list of plain-English recommendations.

    order_value is the average revenue of one purchase, because the
    dataset records purchases but not revenue.
    """
    messages = []
    reliable = []
    unreliable = []

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
            unreliable.append(campaign)
        elif campaign_roas is not None:
            reliable.append(campaign)

    if not reliable:
        return messages

    best = max(reliable, key=lambda c: c.return_on_ad_spend(order_value))
    for campaign in unreliable:
        comparison = compare_approval(campaign, best)
        if comparison is not None:
            messages.append(comparison)

    if len(reliable) >= 2:
        worst = min(reliable, key=lambda c: c.return_on_ad_spend(order_value))
        if worst.return_on_ad_spend(order_value) < 1:
            messages.append(
                f"Test moving part of {worst.name}'s budget to {best.name}. "
                f"{best.name} spent much less, so its CPA may not hold "
                "at a larger budget."
            )

    return messages
