"""Campaign classes: shared behaviour plus paid/organic specifics."""

from campaign_insights.metrics import conversion_rate, cpa, ctr


class Campaign:
    """Base campaign: metrics that apply to any ad, paid or not."""

    def __init__(self, name, impressions, clicks, purchases):
        self.name = name
        self.impressions = impressions
        self.clicks = clicks
        self.purchases = purchases

    def click_through_rate(self):
        return ctr(self.clicks, self.impressions)

    def conversion_rate(self):
        return conversion_rate(self.purchases, self.clicks)

    def summary(self):
        return (
            f"{self.name}: CTR={self.click_through_rate():.2f}%, "
            f"Conversion Rate={self.conversion_rate():.2f}%"
        )


class PaidCampaign(Campaign):
    """A campaign with an ad spend, so cost metrics apply."""

    def __init__(self, name, impressions, clicks, purchases, spent):
        super().__init__(name, impressions, clicks, purchases)
        self.spent = spent

    def cost_per_acquisition(self):
        return cpa(self.spent, self.purchases)

    def summary(self):
        base = super().summary()
        return f"{base}, CPA={self.cost_per_acquisition():.2f}"


class OrganicCampaign(Campaign):
    """A campaign with no ad spend."""

    def summary(self):
        base = super().summary()
        return f"{base}, Spend=0 (organic)"