"""Tests for the loader, the campaign classes and the recommendations."""

import pytest

from campaign_insights.analysis import recommend
from campaign_insights.campaigns import PaidCampaign
from campaign_insights.loader import load_campaign_data


def make_campaign(name, purchases, spent):
    """Create a PaidCampaign with fixed traffic numbers for testing."""
    return PaidCampaign(
        name=name,
        ads=10,
        impressions=10000,
        clicks=100,
        enquiries=100,
        purchases=purchases,
        spent=spent,
    )


def test_paid_campaign_summary_shows_na_for_zero_purchases():
    campaign = make_campaign("Test", purchases=0, spent=100)
    assert "CPA=n/a" in campaign.summary()


def test_recommend_suggests_budget_test_when_a_campaign_loses_money():
    good = make_campaign("Good", purchases=50, spent=500)
    bad = make_campaign("Bad", purchases=40, spent=4000)
    messages = recommend([good, bad], order_value=50)
    assert any("Test moving part of Bad's budget to Good" in m for m in messages)


def test_recommend_no_budget_test_when_all_campaigns_are_profitable():
    first = make_campaign("First", purchases=50, spent=500)
    second = make_campaign("Second", purchases=40, spent=1000)
    messages = recommend([first, second], order_value=50)
    assert not any("Test moving" in m for m in messages)


def test_recommend_flags_campaign_with_few_purchases():
    small = make_campaign("Small", purchases=5, spent=50)
    messages = recommend([small], order_value=50)
    assert any("not reliable" in m for m in messages)


def test_loader_rejects_negative_values(tmp_path):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text(
        "xyz_campaign_id,Impressions,Clicks,Spent,"
        "Total_Conversion,Approved_Conversion\n"
        "1,-5,1,1.0,1,1\n"
    )
    with pytest.raises(ValueError, match="negative"):
        load_campaign_data(csv_file)


def test_loader_rejects_missing_columns(tmp_path):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text("xyz_campaign_id,Impressions\n1,100\n")
    with pytest.raises(ValueError, match="Missing required columns"):
        load_campaign_data(csv_file)
