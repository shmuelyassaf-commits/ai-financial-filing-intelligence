# AI Financial Filing Intelligence

An auditable financial-document intelligence portfolio project for **Alphabet, Meta, and Amazon**. It ingests official SEC Company Facts (Inline XBRL), normalizes core annual metrics, validates the outputs, and presents a Streamlit dashboard.

## Why this is not just a chat with PDFs

The numerical layer is deterministic and traceable: every normalized metric retains its XBRL tag, filing date, period end, and SEC accession number. AI belongs **after** this layer: to map non-standard disclosures, explain material changes, and retrieve cited narrative evidence. Rule-based validation remains separate so the output stays auditable.

## MVP architecture

`SEC Company Facts → raw cache → normalized long table → financial model → validation checks → dashboard`

## Metrics in the first release

Revenue, operating income, net income, operating cash flow, capex, free cash flow, cash and equivalents, long-term debt, operating margin, and net margin. The dashboard includes FY 2023–2025 and Q1/Q2 2025–2026; quarterly flows are explicitly displayed as year-to-date figures so that the comparison is consistent. 2026 is not a full-year result.

## Run locally or in GitHub Codespaces

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SEC_USER_AGENT="Your Name your.email@example.com"
python run_pipeline.py
streamlit run app.py
```

The SEC user-agent is required by the SEC's fair-access guidance. The raw responses are cached under `data/raw/`; rerun with `--refresh` to retrieve a fresh copy.

## Next milestone: controlled AI layer

1. **Disclosure Mapping Agent** — maps company-specific segment disclosures to a reviewed schema.
2. **Narrative Evidence Agent** — explains a material change only if it returns filing and section citations.
3. **Review queue** — routes missing, conflicting, or low-confidence values for manual verification.

This project is for analytical and portfolio purposes only; it does not provide investment advice.
