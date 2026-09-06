"""Rule-based checks run before any AI interpretation."""

import pandas as pd


REQUIRED = ["revenue", "operating_income", "net_income", "operating_cash_flow", "capex"]


def validate_metrics(wide_df: pd.DataFrame) -> pd.DataFrame:
    issues = []
    for _, row in wide_df.iterrows():
        key = {"company": row["company"], "fiscal_year": row["fiscal_year"]}
        for metric in REQUIRED:
            if pd.isna(row.get(metric)):
                issues.append({**key, "rule": "missing_required_metric", "detail": metric, "severity": "error"})
        if pd.notna(row.get("revenue")) and row["revenue"] <= 0:
            issues.append({**key, "rule": "non_positive_revenue", "detail": str(row["revenue"]), "severity": "error"})
        if pd.notna(row.get("operating_margin")) and not -1 <= row["operating_margin"] <= 1:
            issues.append({**key, "rule": "implausible_operating_margin", "detail": str(row["operating_margin"]), "severity": "warning"})
    return pd.DataFrame(issues, columns=["company", "fiscal_year", "rule", "detail", "severity"])
