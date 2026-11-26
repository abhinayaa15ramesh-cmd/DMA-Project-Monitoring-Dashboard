import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import io

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Project Monitoring Dashboard", layout="wide")
st.title("📊 Integrated Project Progress Dashboard")

# --------------------------------------------------
# DATABASE
# --------------------------------------------------
conn = sqlite3.connect("progress.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS progress_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    project TEXT,
    month TEXT,
    component TEXT,
    unit TEXT,
    planned_qty REAL,
    achieved_qty REAL,
    physical REAL,
    financial REAL,
    boq_achieved REAL,
    remarks TEXT
)
""")
conn.commit()

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab_entry, tab_summary, tab_city, tab_project, tab_timeline, tab_prediction, tab_data = st.tabs([
    "📝 Data Entry",
    "🏠 Summary",
    "🏙️ City Analysis",
    "🏗️ Project Analysis",
    "📅 Timeline",
    "🔮 Prediction",
    "📄 Data Table"
])

# ==================================================
# DATA ENTRY
# ==================================================
with tab_entry:
    st.subheader("📝 Monthly Progress Entry")

    col1, col2, col3 = st.columns(3)
    city = col1.text_input("City")
    project = col2.text_input("Project")
    month = col3.text_input("Month (e.g. Jan-2026)")

    entry_df = pd.DataFrame({
        "Component": [""],
        "Unit": [""],
        "Planned Qty": [0.0],
        "Achieved Qty": [0.0],
        "Physical %": [0.0],
        "Financial %": [0.0],
        "BOQ Achieved": [0.0],
        "Remarks": [""]
    })

    edited_df = st.data_editor(entry_df, num_rows="dynamic", use_container_width=True)

    if st.button("💾 Save Data"):
        if city and project and month:
            for _, r in edited_df.iterrows():
                if r["Component"]:
                    cur.execute("""
                        INSERT INTO progress_master
                        (city, project, month, component, unit,
                         planned_qty, achieved_qty, physical,
                         financial, boq_achieved, remarks)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        city, project, month, r["Component"], r["Unit"],
                        r["Planned Qty"], r["Achieved Qty"],
                        r["Physical %"], r["Financial %"],
                        r["BOQ Achieved"], r["Remarks"]
                    ))
            conn.commit()
            st.success("✅ Data saved successfully")
        else:
            st.error("City, Project and Month are required")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_sql("SELECT * FROM progress_master", conn)

if df.empty:
    st.info("Please enter data to view dashboard")
    st.stop()

# --------------------------------------------------
# RAG STATUS
# --------------------------------------------------
def rag_status(p):
    if p < 40:
        return "🔴 Red"
    elif p < 70:
        return "🟠 Amber"
    else:
        return "🟢 Green"

df["RAG Status"] = df["physical"].apply(rag_status)

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
st.sidebar.header("🔍 Filters")
city_f = st.sidebar.multiselect("City", df["city"].unique(), df["city"].unique())
proj_f = st.sidebar.multiselect("Project", df["project"].unique(), df["project"].unique())
month_f = st.sidebar.multiselect("Month", df["month"].unique(), df["month"].unique())

fdf = df[
    (df["city"].isin(city_f)) &
    (df["project"].isin(proj_f)) &
    (df["month"].isin(month_f))
]

# ==================================================
# SUMMARY
# ==================================================
with tab_summary:
    st.subheader("🏠 Overall Snapshot")

    c1, c2, c3 = st.columns(3)
    c1.metric("Cities", fdf["city"].nunique())
    c2.metric("Projects", fdf["project"].nunique())
    c3.metric("Components", fdf["component"].nunique())

    avg_phy = fdf["physical"].mean()
    avg_fin = fdf["financial"].mean()

    st.markdown("### Physical Progress")
    st.progress(int(avg_phy))

    st.markdown("### Financial Progress")
    st.progress(int(avg_fin))

# ==================================================
# CITY ANALYSIS
# ==================================================
with tab_city:
    st.subheader("🏙️ City-wise Comparison")
    st.bar_chart(fdf.groupby("city")[["physical", "financial"]].mean())

# ==================================================
# PROJECT ANALYSIS
# ==================================================
with tab_project:
    st.subheader("🏗️ Project-wise Comparison")
    st.bar_chart(fdf.groupby("project")[["physical", "financial"]].mean())

# ==================================================
# TIMELINE
# ==================================================
with tab_timeline:
    st.subheader("📅 Month-wise Trend")
    st.line_chart(fdf.groupby("month")[["physical", "financial"]].mean())

# ==================================================
# PREDICTION
# ==================================================
with tab_prediction:
    st.subheader("🔮 Next 3 Months Physical Progress Prediction")

    trend = fdf.groupby("month")["physical"].mean().reset_index()
    trend["index"] = range(len(trend))

    if len(trend) >= 2:
        coef = np.polyfit(trend["index"], trend["physical"], 1)

        future_x = [trend["index"].max() + i for i in range(1, 4)]
        future_y = np.polyval(coef, future_x)

        pred_df = pd.DataFrame({
            "Month": ["Next-1", "Next-2", "Next-3"],
            "Predicted Physical %": future_y
        })

        st.line_chart(pd.concat([
            trend.set_index("month")["physical"],
            pd.Series(future_y, index=pred_df["Month"])
        ]))

        st.dataframe(pred_df)

    else:
        st.info("Not enough data for prediction")

# ==================================================
# DATA TABLE
# ==================================================
with tab_data:
    st.subheader("📄 Complete Data with RAG Status")
    st.dataframe(fdf, use_container_width=True)

    # Create Excel file in memory
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        fdf.to_excel(writer, index=False, sheet_name="Progress")

    excel_data = buffer.getvalue()

    st.download_button(
        label="⬇️ Download Excel",
        data=excel_data,
        file_name="Progress_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
