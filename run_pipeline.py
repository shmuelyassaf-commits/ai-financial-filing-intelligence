"""Run SEC ingestion, normalization, and validation for the project universe."""

import argparse
import os

from src.config import COMPANIES, PROCESSED_DIR
from src.sec_client import fetch_company_facts
from src.transform import normalize_company, pivot_metrics
from src.validation import validate_metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Re-download raw SEC facts")
    parser.add_argument("--years", nargs="+", type=int, default=[2023, 2024, 2025])
    args = parser.parse_args()

    if not os.getenv("SEC_USER_AGENT"):
        raise SystemExit("SEC_USER_AGENT is required. Copy .env.example and export its value first.")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    frames = []
    for company, details in COMPANIES.items():
        facts = fetch_company_facts(details["cik"], company, refresh=args.refresh)
        frames.append(normalize_company(company, details["ticker"], facts, args.years))

    long_df = __import__("pandas").concat(frames, ignore_index=True)
    wide_df = pivot_metrics(long_df)
    issues_df = validate_metrics(wide_df)
    long_df.to_csv(PROCESSED_DIR / "financial_facts_long.csv", index=False)
    wide_df.to_csv(PROCESSED_DIR / "financial_metrics.csv", index=False)
    issues_df.to_csv(PROCESSED_DIR / "validation_issues.csv", index=False)
    print(f"Saved {len(long_df)} source facts, {len(wide_df)} company-year rows, {len(issues_df)} validation issues.")


if __name__ == "__main__":
    main()
