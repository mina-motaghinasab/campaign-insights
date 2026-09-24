"""Command-line entry point for the campaign_insights package.

Usage:
    uv run -m campaign_insights data/facebook_ads.csv --order-value 50
"""

import argparse
from pathlib import Path

from campaign_insights.analysis import (
    build_campaigns,
    recommend,
    summarize_by_campaign,
)
from campaign_insights.loader import load_campaign_data
from campaign_insights.metrics import ctr
from campaign_insights.plotting import (
    plot_ctr_by_campaign,
    plot_spend_vs_purchases,
)


def parse_arguments():
    """Read the options the user typed on the command line."""
    parser = argparse.ArgumentParser(
        description="Analyse Facebook ad campaign performance."
    )
    parser.add_argument("csv_path", help="path to the campaign CSV file")
    parser.add_argument(
        "--order-value",
        type=float,
        default=50.0,
        help="average revenue of one purchase (default: 50)",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="folder where charts are saved (default: outputs)",
    )
    return parser.parse_args()


def main():
    """Load the data, print the analysis and save the charts."""
    args = parse_arguments()

    try:
        df = load_campaign_data(args.csv_path)
    except FileNotFoundError:
        print(f"Error: file not found: {args.csv_path}")
        return
    except ValueError as error:
        print(f"Error: {error}")
        return

    df["ctr"] = df.apply(
        lambda row: ctr(row["clicks"], row["impressions"]), axis=1
    )

    totals = summarize_by_campaign(df)
    campaigns = build_campaigns(totals)

    print("Campaign summary")
    print("-" * 40)
    for campaign in campaigns:
        print(campaign.summary())

    print()
    print(f"Recommendations (order value: {args.order_value:.2f})")
    print("-" * 40)
    for message in recommend(totals, campaigns, args.order_value):
        print(f"- {message}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    plot_ctr_by_campaign(df, output_dir / "ctr_by_campaign.png")
    plot_spend_vs_purchases(df, output_dir / "spend_vs_purchases.png")
    print()
    print(f"Charts saved to {output_dir}/")


if __name__ == "__main__":
    main()