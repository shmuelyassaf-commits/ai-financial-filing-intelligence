import pandas as pd
import plotly.express as px
import streamlit as st

DATA = "data/processed/financial_metrics.csv"
ISSUES = "data/processed/validation_issues.csv"

st.set_page_config(page_title="AI Financial Filing Intelligence", layout="wide")
st.title("AI Financial Filing Intelligence")
st.caption("Alphabet · Meta · Amazon | SEC-sourced metrics; not investment advice")

try:
    df = pd.read_csv(DATA)
except FileNotFoundError:
    st.info("Run `python run_pipeline.py` after setting SEC_USER_AGENT to populate the dashboard.")
    st.stop()

period_options = df[["fiscal_year", "fiscal_period"]].drop_duplicates().sort_values(["fiscal_year", "fiscal_period"], ascending=[False, True])
labels = {"FY": "FY", "Q1": "Q1 YTD", "Q2": "Q2 YTD", "Q3": "Q3 YTD"}
selected = st.selectbox("Reporting period", period_options.apply(lambda x: f"{x.fiscal_year} {labels[x.fiscal_period]}", axis=1).tolist())
year, period = selected.split()[:2]
period = {"FY": "FY", "Q1": "Q1", "Q2": "Q2", "Q3": "Q3"}[period]
view = df[(df.fiscal_year == int(year)) & (df.fiscal_period == period)].copy()
view["revenue_bn"] = view.revenue / 1e9
view["free_cash_flow_bn"] = view.free_cash_flow / 1e9

left, middle, right = st.columns(3)
for column, company in zip((left, middle, right), view.company):
    row = view[view.company == company].iloc[0]
    with column:
        st.subheader(company)
        st.metric("Revenue", f"${row.revenue_bn:,.1f}B")
        st.metric("Operating margin", f"{row.operating_margin:.1%}")
        st.metric("Free cash flow", f"${row.free_cash_flow_bn:,.1f}B")

st.plotly_chart(px.bar(view, x="company", y="revenue_bn", color="company", title=f"Revenue — {selected} ($B)"), use_container_width=True)
trend = df.melt(id_vars=["company", "fiscal_year"], value_vars=["operating_margin", "net_margin"], var_name="metric", value_name="margin")
st.plotly_chart(px.line(trend, x="fiscal_year", y="margin", color="company", facet_col="metric", markers=True, title="Profitability trend"), use_container_width=True)

issues = pd.read_csv(ISSUES)
with st.expander("Data-quality checks"):
    st.dataframe(issues if not issues.empty else pd.DataFrame({"status": ["All configured checks passed"]}), use_container_width=True)
