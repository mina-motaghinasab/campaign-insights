"""Tests for the KPI functions in metrics.py."""

from campaign_insights.metrics import (
    approval_rate,
    cpa,
    ctr,
    format_value,
    purchases_per_100_clicks,
    roas,
)


def test_ctr():
    assert ctr(clicks=10, impressions=1000) == 1.0


def test_ctr_without_impressions_is_none():
    assert ctr(clicks=0, impressions=0) is None


def test_purchases_per_100_clicks():
    assert purchases_per_100_clicks(purchases=5, clicks=20) == 25.0


def test_purchases_per_100_clicks_without_clicks_is_none():
    assert purchases_per_100_clicks(purchases=3, clicks=0) is None


def test_approval_rate():
    assert approval_rate(purchases=3, enquiries=12) == 25.0


def test_cpa():
    assert cpa(spent=50, purchases=5) == 10.0


def test_cpa_without_purchases_is_none():
    assert cpa(spent=50, purchases=0) is None


def test_roas():
    assert roas(revenue=100, spent=50) == 2.0


def test_roas_without_spend_is_none():
    assert roas(revenue=100, spent=0) is None


def test_format_value():
    assert format_value(1.23456, 4) == "1.2346"
    assert format_value(None) == "n/a"
