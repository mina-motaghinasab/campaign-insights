"""KPI calculations for ad campaigns.

Every ratio returns None when it cannot be calculated (for example a CPA
with zero purchases), so that "no data" is never mistaken for a real value.
"""

from math import sqrt


def ctr(clicks, impressions):
    """Click-through rate: clicks per 100 impressions."""
    if impressions == 0:
        return None
    return clicks / impressions * 100


def purchases_per_100_clicks(purchases, clicks):
    """Purchases per 100 clicks.

    This is not a share of clicks: some purchases come from people who saw
    the ad without clicking, so the value can exceed 100 for a single ad.
    """
    if clicks == 0:
        return None
    return purchases / clicks * 100


def approval_rate(purchases, enquiries):
    """Share of enquiries that turned into a purchase, as a percentage."""
    if enquiries == 0:
        return None
    return purchases / enquiries * 100


def cpa(spent, purchases):
    """Cost per acquisition: money spent per purchase."""
    if purchases == 0:
        return None
    return spent / purchases


def roas(revenue, spent):
    """Return on ad spend: revenue earned per unit spent."""
    if spent == 0:
        return None
    return revenue / spent


def wilson_interval(successes, trials, z=1.96):
    """95% Wilson confidence interval for a proportion, in percent.

    Returns a (low, high) tuple, or None if there are no trials.
    """
    if trials == 0:
        return None
    p = successes / trials
    denominator = 1 + z**2 / trials
    centre = (p + z**2 / (2 * trials)) / denominator
    margin = z * sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2)) / denominator
    return (centre - margin) * 100, (centre + margin) * 100


def format_value(value, decimals=2):
    """Format a number for printing, or "n/a" if it is None."""
    if value is None:
        return "n/a"
    return f"{value:.{decimals}f}"
