import pandas as pd

from src.validation import validate_metrics


def test_missing_revenue_is_an_error():
    data = pd.DataFrame([{
        "company": "Example", "fiscal_year": 2025, "fiscal_period": "FY", "revenue": None,
        "operating_income": 2, "net_income": 1, "operating_cash_flow": 3, "capex": 1,
        "operating_margin": None,
    }])
    issues = validate_metrics(data)
    assert "missing_required_metric" in issues.rule.values
