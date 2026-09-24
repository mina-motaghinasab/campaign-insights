"""Charts for comparing campaign performance."""

import matplotlib.pyplot as plt


def plot_ctr_by_campaign(df, output_path):
    """Bar chart of average CTR per campaign, saved to output_path."""
    grouped = df.groupby("campaign_id")["ctr"].mean()

    fig, ax = plt.subplots()
    grouped.plot(kind="bar", ax=ax)
    ax.set_xlabel("Campaign ID")
    ax.set_ylabel("Average CTR (%)")
    ax.set_title("Average Click-Through Rate by Campaign")
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