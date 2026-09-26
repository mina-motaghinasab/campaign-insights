"""Charts for comparing campaign performance."""

import matplotlib.pyplot as plt


def plot_ctr_by_campaign(campaigns, output_path):
    """Bar chart of each campaign's CTR, saved to output_path.

    The CTR comes from the campaign's summed clicks and impressions,
    the same numbers used in the printed summary.
    """
    names = [campaign.name for campaign in campaigns]
    values = [campaign.click_through_rate() for campaign in campaigns]

    fig, ax = plt.subplots()
    ax.bar(names, values)
    ax.set_xlabel("Campaign")
    ax.set_ylabel("CTR (%)")
    ax.set_title("Click-Through Rate by Campaign")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_spend_vs_purchases(df, output_path):
    """Scatter plot of ad spend against purchases, saved to output_path."""
    fig, ax = plt.subplots()
    ax.scatter(df["spent"], df["purchases"])
    ax.set_xlabel("Amount Spent")
    ax.set_ylabel("Purchases")
    ax.set_title("Ad Spend vs. Purchases")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
