import pandas as pd
import numpy as np
import os

# ==========================================
# PROJECT PATH
# ==========================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(PROJECT_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

# ==========================================
# CREATE DATASET
# ==========================================

np.random.seed(42)

n = 1000

data = pd.DataFrame({
    "Project_ID": [f"AI-{i:04d}" for i in range(1, n + 1)],

    "Industry": np.random.choice(
        [
            "Banking",
            "Healthcare",
            "Retail",
            "Manufacturing",
            "Telecom",
            "Logistics"
        ],
        n
    ),

    "AI_Use_Case": np.random.choice(
        [
            "Fraud Detection",
            "Demand Forecasting",
            "Customer Support",
            "Predictive Maintenance",
            "Recommendation",
            "Document Intelligence"
        ],
        n
    ),

    "Model_Type": np.random.choice(
        [
            "Classification",
            "Regression",
            "NLP",
            "Computer Vision",
            "Recommendation"
        ],
        n
    ),

    "Monthly_Cost": np.random.randint(5000, 100000, n),

    "Annual_Benefit": np.random.randint(
        20000,
        500000,
        n
    ),

    "Accuracy": np.round(
        np.random.uniform(0.65, 0.99, n),
        3
    ),

    "Latency_ms": np.round(
        np.random.uniform(20, 500, n),
        2
    ),

    "Data_Drift": np.round(
        np.random.uniform(0, 0.30, n),
        3
    ),

    "Compliance_Risk": np.round(
        np.random.uniform(0, 1, n),
        3
    ),

    "Model_Downtime": np.round(
        np.random.uniform(0, 15, n),
        2
    ),

    "User_Adoption": np.round(
        np.random.uniform(0.30, 1.00, n),
        3
    )
})

# ==========================================
# CALCULATED COLUMNS
# ==========================================

data["Annual_Cost"] = (
    data["Monthly_Cost"] * 12
)

data["ROI_Percent"] = np.round(
    (
        (
            data["Annual_Benefit"]
            - data["Annual_Cost"]
        )
        / data["Annual_Cost"]
    ) * 100,
    2
)

data["Governance_Risk_Score"] = np.round(
    (
        data["Compliance_Risk"] * 0.45
        + data["Data_Drift"] * 0.30
        + (data["Model_Downtime"] / 15) * 0.25
    ) * 100,
    2
)

data["Performance_Score"] = np.round(
    (
        data["Accuracy"] * 0.50
        + (1 - data["Latency_ms"] / 500) * 0.15
        + (1 - data["Data_Drift"] / 0.30) * 0.15
        + data["User_Adoption"] * 0.20
    ) * 100,
    2
)

# ==========================================
# SAVE CSV
# ==========================================

DATA_FILE = os.path.join(
    DATA_DIR,
    "ai_projects.csv"
)

data.to_csv(
    DATA_FILE,
    index=False
)

print("Dataset created successfully ✅")
print("Rows:", data.shape[0])
print("Columns:", data.shape[1])
print("Saved at:", DATA_FILE)

print("\nFirst 5 rows:")
print(data.head())

# ==========================================
# STEP 4 — DATA QUALITY CHECK
# ==========================================

print("\n===== DATA QUALITY CHECK =====")

print("\nDataset Shape:")
print(data.shape)

print("\nData Types:")
print(data.dtypes)

print("\nMissing Values:")
print(data.isnull().sum())

print("\nDuplicate Rows:")
print(data.duplicated().sum())

print("\nBasic Statistics:")
print(data.describe())

# ==========================================
# STEP 5 — EDA + BUSINESS KPI ANALYSIS
# ==========================================

print("\n===== ENTERPRISE AI KPI SUMMARY =====")

total_projects = data["Project_ID"].nunique()
avg_roi = data["ROI_Percent"].mean()
avg_performance = data["Performance_Score"].mean()
avg_risk = data["Governance_Risk_Score"].mean()
total_cost = data["Annual_Cost"].sum()
total_benefit = data["Annual_Benefit"].sum()

print(f"Total AI Projects       : {total_projects}")
print(f"Average ROI             : {avg_roi:.2f}%")
print(f"Average Performance     : {avg_performance:.2f}/100")
print(f"Average Governance Risk : {avg_risk:.2f}/100")
print(f"Total Annual Cost       : ${total_cost:,.0f}")
print(f"Total Annual Benefit    : ${total_benefit:,.0f}")


# ==========================================
# INDUSTRY-WISE ANALYSIS
# ==========================================

industry_summary = (
    data.groupby("Industry")
    .agg(
        Projects=("Project_ID", "count"),
        Avg_ROI=("ROI_Percent", "mean"),
        Avg_Performance=("Performance_Score", "mean"),
        Avg_Risk=("Governance_Risk_Score", "mean"),
        Annual_Cost=("Annual_Cost", "sum"),
        Annual_Benefit=("Annual_Benefit", "sum")
    )
    .round(2)
    .sort_values("Avg_ROI", ascending=False)
)

print("\n===== INDUSTRY ANALYSIS =====")
print(industry_summary)


# ==========================================
# VISUALIZATION
# ==========================================

import matplotlib.pyplot as plt

# ROI by Industry
industry_summary["Avg_ROI"].plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Average ROI by Industry")
plt.xlabel("Industry")
plt.ylabel("Average ROI (%)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


# Performance by Industry
industry_summary["Avg_Performance"].plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("AI Performance by Industry")
plt.xlabel("Industry")
plt.ylabel("Performance Score")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


# Governance Risk by Industry
industry_summary["Avg_Risk"].plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Governance Risk by Industry")
plt.xlabel("Industry")
plt.ylabel("Risk Score")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# ==========================================
# STEP 6 — GOVERNANCE RISK CLASSIFICATION
# ==========================================

def risk_category(score):
    if score < 35:
        return "Low"
    elif score < 65:
        return "Medium"
    else:
        return "High"


data["Risk_Category"] = data[
    "Governance_Risk_Score"
].apply(risk_category)


# Risk summary
risk_summary = (
    data["Risk_Category"]
    .value_counts()
    .rename_axis("Risk_Category")
    .reset_index(name="Project_Count")
)

risk_summary["Percentage"] = (
    risk_summary["Project_Count"]
    / len(data)
    * 100
).round(2)

print("\n===== GOVERNANCE RISK SUMMARY =====")
print(risk_summary)


# ==========================================
# RISK DISTRIBUTION
# ==========================================

import matplotlib.pyplot as plt

risk_order = ["Low", "Medium", "High"]

risk_counts = (
    data["Risk_Category"]
    .value_counts()
    .reindex(risk_order)
    .fillna(0)
)

risk_counts.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("AI Governance Risk Distribution")
plt.xlabel("Risk Category")
plt.ylabel("Number of Projects")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# ==========================================
# STEP 7 — ML GOVERNANCE RISK PREDICTION
# ==========================================

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Features
features = [
    "Accuracy",
    "Latency_ms",
    "Data_Drift",
    "Compliance_Risk",
    "Model_Downtime",
    "User_Adoption",
    "ROI_Percent",
    "Performance_Score"
]

X = data[features]
y = data["Risk_Category"]


# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Random Forest Model
risk_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)

risk_model.fit(X_train, y_train)


# Prediction
y_pred = risk_model.predict(X_test)


# Model Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n===== ML MODEL RESULTS =====")
print(f"Model Accuracy: {accuracy:.2%}")


print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, y_pred))


# ==========================================
# CONFUSION MATRIX
# ==========================================

import matplotlib.pyplot as plt
import seaborn as sns

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=risk_model.classes_
)

plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    xticklabels=risk_model.classes_,
    yticklabels=risk_model.classes_
)

plt.title("Governance Risk Prediction - Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

feature_importance = pd.DataFrame({
    "Feature": features,
    "Importance": risk_model.feature_importances_
}).sort_values(
    "Importance",
    ascending=False
)

print("\n===== FEATURE IMPORTANCE =====")
print(feature_importance)

# ==========================================
# STEP 8 — MODEL SAVE + ROI INTELLIGENCE
# ==========================================

import joblib
import os

MODEL_DIR = os.path.join(
    PROJECT_DIR,
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================================
# SAVE ML MODEL
# ==========================================

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "roi_risk_model.pkl"
)

joblib.dump(
    risk_model,
    MODEL_FILE
)

print("\nModel saved successfully ✅")
print("Model location:", MODEL_FILE)


# ==========================================
# ROI CLASSIFICATION
# ==========================================

def roi_category(roi):
    if roi < 0:
        return "Negative ROI"
    elif roi < 50:
        return "Low ROI"
    elif roi < 150:
        return "Healthy ROI"
    else:
        return "High ROI"


data["ROI_Category"] = data[
    "ROI_Percent"
].apply(roi_category)


# ==========================================
# BUSINESS PRIORITY SCORE
# ==========================================

data["Business_Priority_Score"] = np.round(
    (
        data["Performance_Score"] * 0.35
        +
        np.clip(
            data["ROI_Percent"],
            0,
            200
        ) / 2 * 0.35
        +
        (
            100
            - data["Governance_Risk_Score"]
        ) * 0.30
    ),
    2
)


def priority_category(score):
    if score >= 75:
        return "Strategic"
    elif score >= 50:
        return "Monitor"
    else:
        return "Review"


data["Business_Priority"] = (
    data["Business_Priority_Score"]
    .apply(priority_category)
)


# ==========================================
# TOP STRATEGIC PROJECTS
# ==========================================

top_projects = data[
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


print("\n===== TOP 10 STRATEGIC AI PROJECTS =====")
print(top_projects.to_string(index=False))

# ==========================================
# STEP 9 — SQL DATABASE + BUSINESS QUERIES
# ==========================================

import sqlite3

DB_FILE = os.path.join(
    PROJECT_DIR,
    "data",
    "enterprise_ai.db"
)

# Connect to SQLite
conn = sqlite3.connect(DB_FILE)

# Save dataframe into SQL table
data.to_sql(
    "ai_projects",
    conn,
    if_exists="replace",
    index=False
)

print("\nSQL Database created successfully ✅")
print("Database:", DB_FILE)


# ==========================================
# QUERY 1 — TOP ROI PROJECTS
# ==========================================

high_roi = pd.read_sql_query(
    """
    SELECT
        Project_ID,
        Industry,
        AI_Use_Case,
        ROI_Percent,
        Performance_Score
    FROM ai_projects
    ORDER BY ROI_Percent DESC
    LIMIT 10
    """,
    conn
)

print("\n===== TOP 10 HIGH ROI PROJECTS =====")
print(high_roi.to_string(index=False))


# ==========================================
# QUERY 2 — HIGH GOVERNANCE RISK
# ==========================================

high_risk = pd.read_sql_query(
    """
    SELECT
        Project_ID,
        Industry,
        AI_Use_Case,
        Governance_Risk_Score,
        Compliance_Risk
    FROM ai_projects
    WHERE Governance_Risk_Score >= 65
    ORDER BY Governance_Risk_Score DESC
    """,
    conn
)

print("\n===== HIGH GOVERNANCE RISK PROJECTS =====")
print(high_risk.head(20).to_string(index=False))


# ==========================================
# QUERY 3 — INDUSTRY PERFORMANCE
# ==========================================

industry_sql = pd.read_sql_query(
    """
    SELECT
        Industry,
        COUNT(*) AS Total_Projects,
        ROUND(AVG(ROI_Percent), 2) AS Avg_ROI,
        ROUND(AVG(Performance_Score), 2) AS Avg_Performance,
        ROUND(AVG(Governance_Risk_Score), 2) AS Avg_Risk
    FROM ai_projects
    GROUP BY Industry
    ORDER BY Avg_ROI DESC
    """,
    conn
)

print("\n===== INDUSTRY BUSINESS ANALYSIS =====")
print(industry_sql.to_string(index=False))


# ==========================================
# CLOSE DATABASE
# ==========================================

conn.close()

print("\nSQL analysis completed successfully ✅")

# ==========================================
# STEP 10 — AI INSIGHTS & ALERTS
# ==========================================

def generate_alert(row):
    alerts = []

    if row["ROI_Percent"] < 0:
        alerts.append("Negative ROI")

    if row["Governance_Risk_Score"] >= 65:
        alerts.append("High Governance Risk")

    if row["Performance_Score"] < 60:
        alerts.append("Low AI Performance")

    if row["Data_Drift"] >= 0.20:
        alerts.append("High Data Drift")

    if row["Model_Downtime"] >= 10:
        alerts.append("High Downtime")

    if row["User_Adoption"] < 0.50:
        alerts.append("Low User Adoption")

    if not alerts:
        return "Healthy"

    return " | ".join(alerts)


data["AI_Alert"] = data.apply(
    generate_alert,
    axis=1
)


# ==========================================
# MANAGEMENT INSIGHT
# ==========================================

def generate_insight(row):

    if row["AI_Alert"] == "Healthy":
        return "AI project is performing within acceptable business and governance limits."

    if row["ROI_Percent"] < 0:
        return "Financial review required due to negative ROI."

    if row["Governance_Risk_Score"] >= 65:
        return "Governance review required before further scaling."

    if row["Performance_Score"] < 60:
        return "Model performance optimization is recommended."

    if row["Data_Drift"] >= 0.20:
        return "Data monitoring and model retraining should be considered."

    return "Project requires management monitoring."


data["Management_Insight"] = data.apply(
    generate_insight,
    axis=1
)


# ==========================================
# CREATE INSIGHTS DATASET
# ==========================================

ai_insights = data[
    [
        "Project_ID",
        "Industry",
        "AI_Use_Case",
        "ROI_Percent",
        "Performance_Score",
        "Governance_Risk_Score",
        "Risk_Category",
        "Business_Priority",
        "AI_Alert",
        "Management_Insight"
    ]
].copy()


# ==========================================
# SAVE OUTPUT
# ==========================================

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "outputs"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

INSIGHTS_FILE = os.path.join(
    OUTPUT_DIR,
    "ai_insights.csv"
)

ai_insights.to_csv(
    INSIGHTS_FILE,
    index=False
)

print("\nAI Insights generated successfully ✅")
print("Saved at:", INSIGHTS_FILE)

print("\n===== SAMPLE AI ALERTS =====")
print(
    ai_insights[
        ai_insights["AI_Alert"] != "Healthy"
    ].head(10).to_string(index=False)
) 

# ==========================================
# STEP 11 — FINAL DASHBOARD ANALYSIS
# ==========================================

# ==========================================
# ENTERPRISE KPI SUMMARY
# ==========================================

dashboard_kpis = {
    "Total Projects": len(data),

    "Average ROI (%)":
        round(data["ROI_Percent"].mean(), 2),

    "Average Performance":
        round(data["Performance_Score"].mean(), 2),

    "Average Governance Risk":
        round(data["Governance_Risk_Score"].mean(), 2),

    "Total Annual Cost":
        round(data["Annual_Cost"].sum(), 2),

    "Total Annual Benefit":
        round(data["Annual_Benefit"].sum(), 2),

    "High Risk Projects":
        int(
            (data["Risk_Category"] == "High").sum()
        ),

    "Negative ROI Projects":
        int(
            (data["ROI_Percent"] < 0).sum()
        )
}


print("\n===================================")
print(" ENTERPRISE AI DASHBOARD KPIs")
print("===================================")

for key, value in dashboard_kpis.items():
    print(f"{key}: {value}")


# ==========================================
# ROI VS PERFORMANCE
# ==========================================

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=data,
    x="ROI_Percent",
    y="Performance_Score",
    hue="Risk_Category",
    alpha=0.7
)

plt.axhline(60, linestyle="--")
plt.axvline(0, linestyle="--")

plt.title("AI ROI vs Performance")
plt.xlabel("ROI (%)")
plt.ylabel("Performance Score")

plt.tight_layout()
plt.show()


# ==========================================
# GOVERNANCE RISK VS ROI
# ==========================================

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=data,
    x="Governance_Risk_Score",
    y="ROI_Percent",
    hue="Business_Priority",
    alpha=0.7
)

plt.axvline(65, linestyle="--")

plt.title("Governance Risk vs ROI")
plt.xlabel("Governance Risk Score")
plt.ylabel("ROI (%)")

plt.tight_layout()
plt.show()


# ==========================================
# SAVE FINAL DATASET
# ==========================================

FINAL_FILE = os.path.join(
    OUTPUT_DIR,
    "enterprise_ai_final.csv"
)

data.to_csv(
    FINAL_FILE,
    index=False
)

print("\nFinal dataset saved successfully ✅")
print("Saved at:", FINAL_FILE)