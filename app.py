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

year = st.selectbox("Fiscal year", sorted(df.fiscal_year.unique(), reverse=True))
view = df[df.fiscal_year == year].copy()
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

st.plotly_chart(px.bar(view, x="company", y="revenue_bn", color="company", title=f"Revenue — FY {year} ($B)"), use_container_width=True)
trend = df.melt(id_vars=["company", "fiscal_year"], value_vars=["operating_margin", "net_margin"], var_name="metric", value_name="margin")
st.plotly_chart(px.line(trend, x="fiscal_year", y="margin", color="company", facet_col="metric", markers=True, title="Profitability trend"), use_container_width=True)

issues = pd.read_csv(ISSUES)
with st.expander("Data-quality checks"):
    st.dataframe(issues if not issues.empty else pd.DataFrame({"status": ["All configured checks passed"]}), use_container_width=True)
