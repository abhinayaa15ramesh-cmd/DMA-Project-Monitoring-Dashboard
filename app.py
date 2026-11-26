import streamlit as st
import pandas as pd
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["progress_dashboard"]
collection = db["monthly_progress"]

st.title("Monthly Progress Dashboard")

# Upload Excel
uploaded_file = st.file_uploader("Upload Progress Report", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Excel Preview")
    st.dataframe(df)

    processed_data = []

    for index, row in df.iterrows():

        planned = row.get("Total BOQ Qty", 0)
        achieved = row.get("Since last month", 0)

        if planned != 0:
            physical = (achieved / planned) * 100
        else:
            physical = 0

        record = {
            "Component": row.get("Component"),
            "Unit": row.get("Unit"),
            "Planned Qty": planned,
            "Achieved Qty": achieved,
            "Physical %": round(physical,2),
            "Financial %": 0,
            "BOQ Achieved": achieved,
            "Remarks": ""
        }

        processed_data.append(record)

    st.subheader("Dashboard Data")

    dashboard_df = pd.DataFrame(processed_data)

    st.dataframe(dashboard_df)

    if st.button("Save to Database"):
        collection.insert_many(processed_data)
        st.success("Data saved successfully!")

# Show stored data
st.subheader("Saved Dashboard Data")

saved_data = list(collection.find({}, {"_id":0}))

if saved_data:
    st.dataframe(pd.DataFrame(saved_data))
