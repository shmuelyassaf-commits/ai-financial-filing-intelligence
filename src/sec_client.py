"""Small, auditable client for SEC Company Facts data."""

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

from .config import RAW_DIR

BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"


def fetch_company_facts(cik: str, company: str, refresh: bool = False) -> dict:
    """Fetch a company's official XBRL facts and cache the raw response."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{company.lower().replace(' ', '_')}_facts.json"
    if path.exists() and not refresh:
        return json.loads(path.read_text())

    user_agent = os.getenv("SEC_USER_AGENT")
    if not user_agent:
        raise RuntimeError("Set SEC_USER_AGENT before downloading SEC data. See .env.example.")

    request = Request(
        BASE_URL.format(cik=cik),
        # Avoid compressed responses so the cache remains plain JSON and portable.
        headers={"User-Agent": user_agent, "Accept-Encoding": "identity"},
    )
    with urlopen(request, timeout=30) as response:  # nosec: fixed SEC HTTPS endpoint
        payload = json.loads(response.read().decode("utf-8"))
    path.write_text(json.dumps(payload, indent=2))
    return payload
