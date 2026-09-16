import streamlit as st
import pandas as pd
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Enterprise AI Intelligence",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# DATA FILE PATH
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# GitHub deployment:
# enterprise_ai_final.csv is in the same folder as app.py

DATA_FILE = os.path.join(
    CURRENT_DIR,
    "enterprise_ai_final.csv"
)

# Local project fallback:
# outputs/enterprise_ai_final.csv

if not os.path.exists(DATA_FILE):

    LOCAL_OUTPUT_FILE = os.path.join(
        CURRENT_DIR,
        "outputs",
        "enterprise_ai_final.csv"
    )

    if os.path.exists(LOCAL_OUTPUT_FILE):
        DATA_FILE = LOCAL_OUTPUT_FILE

# ============================================================
# LOAD DATA
# ============================================================

if not os.path.exists(DATA_FILE):
    st.error(
        "❌ enterprise_ai_final.csv not found."
    )
    st.info(
        "First run: notebooks/data_analysis.py"
    )
    st.stop()

data = pd.read_csv(DATA_FILE)

# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Project_ID",
    "Industry",
    "AI_Use_Case",
    "ROI_Percent",
    "Performance_Score",
    "Governance_Risk_Score",
    "Risk_Category",
    "Business_Priority_Score",
    "Business_Priority",
    "AI_Alert",
    "Annual_Cost",
    "Annual_Benefit"
]

missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]

if missing_columns:
    st.error("❌ Required columns are missing:")
    st.write(missing_columns)
    st.stop()

# ============================================================
# DARK PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* MAIN BACKGROUND */
    .stApp {
        background:
        linear-gradient(
            135deg,
            #020617 0%,
            #0f172a 50%,
            #172554 100%
        );
    }

    /* HEADER */
    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .main-subtitle {
        font-size: 16px;
        color: #94a3b8;
        margin-bottom: 30px;
    }

    /* SECTION TITLE */
    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 30px;
        margin-bottom: 18px;
        padding-left: 12px;
        border-left: 5px solid #38bdf8;
    }

    /* KPI CARD */
    .kpi-card {
        background:
        linear-gradient(
            145deg,
            #1e293b,
            #0f172a
        );

        padding: 20px;
        border-radius: 16px;

        border: 1px solid #334155;

        box-shadow:
        0 8px 25px rgba(0,0,0,0.35);

        min-height: 120px;
    }

    .kpi-label {
        font-size: 14px;
        color: #94a3b8;
        font-weight: 600;
    }

    .kpi-value {
        font-size: 32px;
        font-weight: 800;
        color: #38bdf8;
        margin-top: 8px;
    }

    /* STREAMLIT METRIC */
    [data-testid="stMetric"] {
        background: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: 800;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #020617;
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    /* ALERT */
    .alert-box {
        background: #450a0a;
        padding: 17px;
        border-radius: 12px;
        border-left: 5px solid #ef4444;
        color: #fecaca;
        margin-bottom: 15px;
    }

    /* INFO */
    .info-box {
        background: #172554;
        padding: 17px;
        border-radius: 12px;
        border-left: 5px solid #38bdf8;
        color: #bfdbfe;
        margin-bottom: 15px;
    }

    /* EXPANDER */
    [data-testid="stExpander"] {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 12px;
    }

    /* DIVIDER */
    hr {
        border-color: #334155;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🤖 Enterprise AI Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Performance • ROI • Governance • Business Intelligence'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR FILTER
# ============================================================

st.sidebar.header("🎯 Portfolio Filters")

industries = (
    ["All"]
    + sorted(
        data["Industry"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_industry = st.sidebar.selectbox(
    "Select Industry",
    industries
)

# ============================================================
# FILTER DATA
# IMPORTANT: filtered_data is created BEFORE KPIs
# ============================================================

if selected_industry == "All":

    filtered_data = data.copy()

else:

    filtered_data = data[
        data["Industry"] == selected_industry
    ].copy()

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_projects = len(filtered_data)

avg_roi = filtered_data[
    "ROI_Percent"
].mean()

avg_performance = filtered_data[
    "Performance_Score"
].mean()

avg_risk = filtered_data[
    "Governance_Risk_Score"
].mean()

high_risk = int(
    (
        filtered_data["Risk_Category"]
        == "High"
    ).sum()
)

negative_roi = int(
    (
        filtered_data["ROI_Percent"]
        < 0
    ).sum()
)

# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📌 Executive KPI Dashboard'
    '</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">
                AI Projects
            </div>
            <div class="kpi-value">
                {total_projects:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">
                Average ROI
            </div>
            <div class="kpi-value">
                {avg_roi:.1f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">
                AI Performance
            </div>
            <div class="kpi-value">
                {avg_performance:.1f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">
                Governance Risk
            </div>
            <div class="kpi-value">
                {avg_risk:.1f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">
                High Risk Projects
            </div>
            <div class="kpi-value">
                {high_risk:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# SECONDARY KPIs
# ============================================================

st.write("")

s1, s2, s3 = st.columns(3)

with s1:

    st.metric(
        "Negative ROI Projects",
        f"{negative_roi:,}"
    )

with s2:

    total_cost = filtered_data[
        "Annual_Cost"
    ].sum()

    st.metric(
        "Total Annual Cost",
        f"${total_cost:,.0f}"
    )

with s3:

    total_benefit = filtered_data[
        "Annual_Benefit"
    ].sum()

    st.metric(
        "Total Annual Benefit",
        f"${total_benefit:,.0f}"
    )

# ============================================================
# ALERT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🚨 AI Risk & Management Alerts'
    '</div>',
    unsafe_allow_html=True
)

alerts = filtered_data[
    filtered_data["AI_Alert"] != "Healthy"
][
    [
        "Project_ID",
        "Industry",
        "AI_Use_Case",
        "ROI_Percent",
        "Governance_Risk_Score",
        "AI_Alert"
    ]
].sort_values(
    "Governance_Risk_Score",
    ascending=False
)

if len(alerts) > 0:

    st.markdown(
        '<div class="alert-box">'
        '<b>⚠ Attention Required:</b> '
        'Projects requiring financial, performance '
        'or governance monitoring.'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        alerts.head(15),
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "✅ No critical AI alerts detected."
    )

# ============================================================
# PORTFOLIO ANALYTICS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📊 Portfolio Analytics'
    '</div>',
    unsafe_allow_html=True
)

chart1, chart2 = st.columns(
    [1, 1],
    gap="medium"
)

# ============================================================
# CHART 1 - ROI BY INDUSTRY
# ============================================================

with chart1:

    st.markdown(
        """
        <div style="
            background:#111827;
            border:1px solid #334155;
            border-radius:14px;
            padding:15px;
            height:70px;
        ">
            <h3 style="
                color:#ffffff;
                margin:0;
                font-size:20px;
            ">
            💰 Average ROI by Industry
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    industry_roi = (
        filtered_data
        .groupby("Industry")["ROI_Percent"]
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )

    st.bar_chart(
        industry_roi,
        use_container_width=True,
        height=330
    )


# ============================================================
# CHART 2 - RISK DISTRIBUTION
# ============================================================

with chart2:

    st.markdown(
        """
        <div style="
            background:#111827;
            border:1px solid #334155;
            border-radius:14px;
            padding:15px;
            height:70px;
        ">
            <h3 style="
                color:#ffffff;
                margin:0;
                font-size:20px;
            ">
            🛡️ Governance Risk Distribution
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    risk_distribution = (
        filtered_data["Risk_Category"]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High"]
        )
        .fillna(0)
    )

    st.bar_chart(
        risk_distribution,
        use_container_width=True,
        height=330
    )


# ============================================================
# ROI VS PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🎯 AI Performance vs Business ROI'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "Higher performance with positive ROI "
    "indicates stronger business potential."
)

st.scatter_chart(
    filtered_data,
    x="ROI_Percent",
    y="Performance_Score",
    color="Risk_Category",
    use_container_width=True
)

# ============================================================
# GOVERNANCE VS ROI
# ============================================================

st.markdown(
    '<div class="section-title">'
    '⚖️ Governance Risk vs ROI'
    '</div>',
    unsafe_allow_html=True
)

st.scatter_chart(
    filtered_data,
    x="Governance_Risk_Score",
    y="ROI_Percent",
    color="Business_Priority",
    use_container_width=True
)

# ============================================================
# TOP STRATEGIC PROJECTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🏆 Top Strategic AI Projects'
    '</div>',
    unsafe_allow_html=True
)

top_projects = filtered_data[
    [
        "Project_ID",
        "Industry",
        "AI_Use_Case",
        "ROI_Percent",
        "Performance_Score",
        "Governance_Risk_Score",
        "Business_Priority_Score",
        "Business_Priority"
    ]
].sort_values(
    "Business_Priority_Score",
    ascending=False
).head(10)

st.dataframe(
    top_projects,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# COMPLETE PORTFOLIO
# ============================================================

with st.expander(
    "📁 View Complete AI Portfolio"
):

    st.dataframe(
        filtered_data,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Enterprise AI Intelligence Platform | "
    "Performance • ROI • Governance"
)