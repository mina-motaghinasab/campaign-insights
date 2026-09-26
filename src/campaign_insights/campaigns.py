"""Campaign classes: shared behaviour plus paid/organic specifics."""

from campaign_insights.metrics import (
    approval_rate,
    cpa,
    ctr,
    format_value,
    purchases_per_100_clicks,
    roas,
)


class Campaign:
    """Base campaign: metrics that apply to any ad, paid or not."""

    def __init__(self, name, ads, impressions, clicks, enquiries, purchases):
        self.name = name
        self.ads = ads
        self.impressions = impressions
        self.clicks = clicks
        self.enquiries = enquiries
        self.purchases = purchases

    def click_through_rate(self):
        return ctr(self.clicks, self.impressions)

    def purchases_per_100_clicks(self):
        return purchases_per_100_clicks(self.purchases, self.clicks)

    def approval_rate(self):
        return approval_rate(self.purchases, self.enquiries)

    def summary(self):
        return (
            f"{self.name}: CTR={format_value(self.click_through_rate(), 4)}%, "
            f"Purchases per 100 clicks={format_value(self.purchases_per_100_clicks())}, "
            f"Approval rate={format_value(self.approval_rate())}%"
        )


class PaidCampaign(Campaign):
    """A campaign with an ad spend, so cost metrics apply."""

    def __init__(self, name, ads, impressions, clicks, enquiries, purchases, spent):
        super().__init__(name, ads, impressions, clicks, enquiries, purchases)
        self.spent = spent

    def cost_per_acquisition(self):
        return cpa(self.spent, self.purchases)

    def return_on_ad_spend(self, order_value):
        return roas(self.purchases * order_value, self.spent)

    def summary(self):
        base = super().summary()
        return f"{base}, CPA={format_value(self.cost_per_acquisition())}"


class OrganicCampaign(Campaign):
    """A campaign with no ad spend.

    The Facebook dataset only contains paid campaigns, so this class is not
    used by the command-line tool. It shows how the base class can be
    extended for other data sources.
    """

    def summary(self):
        base = super().summary()
        return f"{base}, Spend=0 (organic)"
