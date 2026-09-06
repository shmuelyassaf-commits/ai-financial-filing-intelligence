"""Normalize SEC facts into a comparable annual financial model."""

from __future__ import annotations

from typing import Iterable

import pandas as pd

from .config import METRICS


def _period_candidates(facts: dict, tag: str) -> list[dict]:
    item = facts.get("facts", {}).get("us-gaap", {}).get(tag, {})
    units = item.get("units", {})
    values = next(iter(units.values()), [])
    return [
        value for value in values
        if value.get("form") in {"10-K", "10-Q"} and value.get("fy") and value.get("fp") in {"FY", "Q1", "Q2", "Q3"}
    ]


def _latest_by_period(values: Iterable[dict]) -> dict[tuple[int, str], dict]:
    result: dict[tuple[int, str], dict] = {}
    for value in values:
        # `fy` describes the filing's fiscal year, while 10-K comparative facts
        # may have a prior period end. The reporting period is the real key.
        year = int(value["end"][:4])
        period = value["fp"]
        # Annual-duration facts should end near the end of the year. Balance
        # sheet facts have no start date and are valid point-in-time values.
        if period == "FY" and value.get("start") and value.get("end", "") < f"{year}-12-15":
            continue
        if period != "FY" and value.get("start") and not value["start"].startswith(str(year)):
            continue
        key = (year, period)
        # For Q2/Q3 we intentionally use the cumulative YTD duration (earliest
        # start date) across all flow metrics. This avoids mixing a standalone
        # quarterly revenue fact with a YTD cash-flow or earnings fact.
        duration = (value.get("end", ""), value.get("start", "9999-99-99"))
        prior = result.get(key)
        if prior is None or duration < (prior.get("end", ""), prior.get("start", "9999-99-99")):
            result[key] = value
    return result


def normalize_company(company: str, ticker: str, facts: dict, periods: Iterable[tuple[int, str]]) -> pd.DataFrame:
    """Return one transparent row per requested company/year/metric."""
    periods = list(periods)
    rows: list[dict] = []
    for metric, tags in METRICS.items():
        candidates_by_tag = {
            tag: _latest_by_period(_period_candidates(facts, tag)) for tag in tags
        }
        # Prefer the tag that covers most fiscal years. This handles issuer-
        # specific tags without silently choosing a less complete fallback.
        selected_tag, selected = max(
            candidates_by_tag.items(),
            key=lambda item: sum(period in item[1] for period in periods),
            default=(None, {}),
        )
        for year, period in periods:
            fact = selected.get((year, period))
            rows.append({
                "company": company,
                "ticker": ticker,
                "fiscal_year": year,
                "fiscal_period": period,
                "metric": metric,
                "value_usd": fact.get("val") if fact else None,
                "xbrl_tag": selected_tag,
                "form": fact.get("form") if fact else None,
                "filed": fact.get("filed") if fact else None,
                "period_end": fact.get("end") if fact else None,
                "accession": fact.get("accn") if fact else None,
            })
    return pd.DataFrame(rows)


def pivot_metrics(long_df: pd.DataFrame) -> pd.DataFrame:
    wide = long_df.pivot_table(
        index=["company", "ticker", "fiscal_year", "fiscal_period"], columns="metric", values="value_usd", aggfunc="first"
    ).reset_index()
    wide["free_cash_flow"] = wide["operating_cash_flow"] - wide["capex"].abs()
    wide["operating_margin"] = wide["operating_income"] / wide["revenue"]
    wide["net_margin"] = wide["net_income"] / wide["revenue"]
    return wide
