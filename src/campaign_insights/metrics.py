"""KPI calculations for ad campaigns."""


def ctr(clicks, impressions):
    """Click-through rate, as a percentage."""
    if impressions == 0:
        return 0.0
    return (clicks / impressions) * 100


def conversion_rate(purchases, clicks):
    """Share of clicks that led to a purchase, as a percentage."""
    if clicks == 0:
        return 0.0
    return (purchases / clicks) * 100


def cpa(spent, purchases):
    """Cost per acquisition: money spent per purchase."""
    if purchases == 0:
        return 0.0
    return spent / purchases


def roas(revenue, spent):
    """Return on ad spend: revenue earned per unit spent."""
    if spent == 0:
        return 0.0
    return revenue / spent


def profit(revenue, spent):
    """Revenue minus ad spend."""
    return revenue - spent