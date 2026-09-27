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
    """Scatter plot of ad spend against purchases, one colour per campaign.

    The x-axis uses a symmetric log scale, so that small and large budgets
    are both visible and ads with zero spend can still be shown.
    """
    fig, ax = plt.subplots()
    groups = list(df.groupby("campaign_id"))
    # Draw the largest campaign first, so the smaller ones stay visible on top.
    groups.sort(key=lambda item: len(item[1]), reverse=True)
    for campaign_id, group in groups:
        ax.scatter(
            group["spent"],
            group["purchases"],
            label=f"Campaign {campaign_id}",
            alpha=0.6,
        )
    ax.set_xscale("symlog", linthresh=1)
    ax.set_xlabel("Amount spent (symmetric log scale)")
    ax.set_ylabel("Purchases")
    ax.set_title("Ad Spend vs. Purchases")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
