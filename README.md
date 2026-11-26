# Project Pulse | Infrastructure Monitoring Dashboard

A Streamlit project monitoring application for tracking physical and financial progress, BOQ achievement, project comparisons and trends.

## Features
- Monthly progress entry and SQLite storage
- City, project and month filters
- RAG status, heatmaps and gap analysis
- Trend-based forecasts and Excel export
- Separate Excel-driven analytics dashboard with regression forecasting

## Getting started
```bash
python -m pip install -r requirements.txt
streamlit run code.py
```
Use the Entry tab to add fictional project records. Enter months in the format Jan-2026. The SQLite database is created locally.

For the Excel-driven dashboard, run `streamlit run dashboard.py` and upload `sample_progress.xlsx`.

## Source files
- `code.py`: Project Pulse, nine-tab SQLite dashboard (recommended entry point).
- `dashboard.py`: Excel-driven analytics dashboard.
- `project.py`: Earlier SQLite dashboard variant.
- `app.py`: MongoDB prototype; requires a running local MongoDB instance and pymongo.

## Data and limitations
The included Excel sample is synthetic. Original workbooks and databases are excluded. Forecasts are exploratory trend extrapolations, not validated predictions. Source code was syntax-checked; full runtime testing is pending. Publish only if authorised to share the original source code.
