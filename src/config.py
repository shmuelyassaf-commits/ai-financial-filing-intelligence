from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

COMPANIES = {
    "Alphabet": {"ticker": "GOOGL", "cik": "0001652044"},
    "Meta": {"ticker": "META", "cik": "0001326801"},
    "Amazon": {"ticker": "AMZN", "cik": "0001018724"},
}

# Each metric may use a different XBRL tag across issuers. The pipeline tries
# candidates in order and preserves the tag actually used for auditability.
METRICS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss", "ProfitLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "cash_and_equivalents": ["CashAndCashEquivalentsAtCarryingValue"],
    "long_term_debt": ["LongTermDebtNoncurrent", "LongTermDebtCurrent"],
}
