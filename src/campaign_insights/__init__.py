"""campaign_insights: analyse the performance of Facebook ad campaigns."""

from campaign_insights.analysis import (
    build_campaigns,
    recommend,
    summarize_by_campaign,
)
from campaign_insights.campaigns import Campaign, OrganicCampaign, PaidCampaign
from campaign_insights.loader import load_campaign_data
from campaign_insights.metrics import (
    approval_rate,
    cpa,
    ctr,
    format_value,
    purchases_per_100_clicks,
    roas,
)
from campaign_insights.plotting import (
    plot_ctr_by_campaign,
    plot_spend_vs_purchases,
)

__all__ = [
    "Campaign",
    "OrganicCampaign",
    "PaidCampaign",
    "approval_rate",
    "build_campaigns",
    "cpa",
    "ctr",
    "format_value",
    "load_campaign_data",
    "plot_ctr_by_campaign",
    "plot_spend_vs_purchases",
    "purchases_per_100_clicks",
    "recommend",
    "roas",
    "summarize_by_campaign",
]
