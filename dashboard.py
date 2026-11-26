import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

# ─────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Project Intelligence Hub",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────
# GLOBAL CSS – soft sage/slate professional palette
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Root palette ── */
:root {
    --sage:    #7c9e8f;
    --sage-lt: #a8c5b5;
    --slate:   #4a6274;
    --navy:    #2c3e50;
    --sand:    #f0ece4;
    --cream:   #faf9f7;
    --white:   #ffffff;
    --accent:  #e8836e;
    --gold:    #c9a84c;
    --muted:   #8a9db0;
    --border:  #dde4eb;
    --shadow:  rgba(74,98,116,.10);
}

/* ── App background ── */
.stApp {
    background: linear-gradient(155deg, #f4f7f5 0%, #eef2f7 50%, #f5f0eb 100%);
    min-height: 100vh;
}

/* ── Sidebar: scope all overrides strictly ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2c3e50 0%, #3d5168 100%);
    border-right: none;
    box-shadow: 4px 0 20px rgba(0,0,0,.10);
}
[data-testid="stSidebar"] > div > div > div * {
    color: #d4dfe6 !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: var(--sage) !important;
    color: #ffffff !important;
}
/* ── Main area widgets: always light bg, dark text ── */
.main [data-baseweb="select"] > div,
.main [data-baseweb="select"] input,
.main [data-baseweb="popover"] * {
    background-color: #ffffff !important;
    color: #2c3e50 !important;
}
.main .stRadio label,
.main .stRadio span,
.main .stSelectbox label,
.main .stMultiSelect label,
.main .stSlider label {
    color: #2c3e50 !important;
}
/* ── Dropdown option list ── */
[data-baseweb="menu"] {
    background: #ffffff !important;
}
[data-baseweb="menu"] li {
    color: #2c3e50 !important;
}
[data-baseweb="menu"] li:hover {
    background: #eef2f7 !important;
}

/* ── Header banner ── */
.hero-banner {
    background: linear-gradient(135deg, #2c3e50 0%, #3d5168 60%, #4a6274 100%);
    border-radius: 18px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(44,62,80,.25);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -80px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(124,158,143,.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(201,168,76,.10) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 14px;
    color: rgba(255,255,255,.60);
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.3px;
}
.hero-badge {
    display: inline-block;
    background: rgba(124,158,143,.30);
    color: #a8c5b5;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 30px;
    margin-bottom: 12px;
    border: 1px solid rgba(124,158,143,.40);
}

/* ── KPI cards ── */
.kpi-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 22px 24px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 12px var(--shadow);
    transition: transform .2s ease, box-shadow .2s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(74,98,116,.14);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.kpi-card.sage::before   { background: linear-gradient(90deg, #7c9e8f, #a8c5b5); }
.kpi-card.slate::before  { background: linear-gradient(90deg, #4a6274, #6f8fa3); }
.kpi-card.accent::before { background: linear-gradient(90deg, #e8836e, #f0a593); }
.kpi-card.gold::before   { background: linear-gradient(90deg, #c9a84c, #e0c473); }
.kpi-icon {
    font-size: 22px;
    margin-bottom: 10px;
    display: block;
}
.kpi-value {
    font-size: 32px;
    font-weight: 700;
    color: var(--navy);
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-label {
    font-size: 12px;
    color: var(--muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.kpi-delta {
    font-size: 12px;
    margin-top: 8px;
    font-weight: 500;
}
.kpi-delta.up   { color: #5a9e7c; }
.kpi-delta.down { color: #e8836e; }

/* ── Section headers ── */
.section-header {
    font-size: 18px;
    font-weight: 600;
    color: var(--navy);
    margin: 28px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--border);
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Chart container ── */
.chart-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 12px var(--shadow);
    margin-bottom: 20px;
}

/* ── Performance badge ── */
.perf-best {
    background: linear-gradient(135deg, #e8f5ee, #d4eddf);
    border: 1px solid #a3d4b8;
    color: #2d7a52;
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 14px;
    font-weight: 500;
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 12px;
}
.perf-worst {
    background: linear-gradient(135deg, #fdf2ee, #faddd6);
    border: 1px solid #f0b8a4;
    color: #c45c38;
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 14px;
    font-weight: 500;
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 12px;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border);
    gap: 2px;
    box-shadow: 0 2px 8px var(--shadow);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    color: var(--muted) !important;
    padding: 8px 18px !important;
    transition: all .15s ease !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: var(--navy) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(44,62,80,.25) !important;
}

/* ── Selectboxes & multiselects (main area only) ── */
.main [data-baseweb="select"] {
    border-radius: 10px !important;
    background: #ffffff !important;
}
.main [data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #2c3e50 !important;
}

/* ── Table ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border) !important;
}

/* ── Progress bar pills ── */
.prog-bar-wrap {
    background: #eef2f7;
    border-radius: 20px;
    height: 8px;
    overflow: hidden;
    margin-top: 4px;
}
.prog-bar-fill {
    height: 8px;
    border-radius: 20px;
    transition: width .4s ease;
}

/* ── Prediction card ── */
.pred-result {
    background: linear-gradient(135deg, #2c3e50, #4a6274);
    border-radius: 14px;
    padding: 24px 28px;
    color: #ffffff;
    text-align: center;
    box-shadow: 0 6px 24px rgba(44,62,80,.25);
    margin-bottom: 20px;
}
.pred-value {
    font-size: 48px;
    font-weight: 700;
    color: #a8c5b5;
    line-height: 1;
}
.pred-label {
    font-size: 13px;
    color: rgba(255,255,255,.65);
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Sidebar logo area ── */
.sidebar-logo {
    text-align: center;
    padding: 20px 16px 24px;
    border-bottom: 1px solid rgba(255,255,255,.10);
    margin-bottom: 20px;
}
.sidebar-logo-icon {
    font-size: 36px;
    display: block;
    margin-bottom: 8px;
}
.sidebar-logo-title {
    font-size: 15px;
    font-weight: 600;
    color: #d4dfe6 !important;
    margin: 0;
}
.sidebar-logo-sub {
    font-size: 11px;
    color: rgba(255,255,255,.40) !important;
    margin: 2px 0 0;
}

/* ── Status pill ── */
.status-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.status-ongoing  { background: #e8f5ee; color: #2d7a52; border: 1px solid #a3d4b8; }
.status-complete { background: #e8f0ff; color: #3a56b0; border: 1px solid #a3b8f0; }
.status-delayed  { background: #fdf2ee; color: #c45c38; border: 1px solid #f0b8a4; }

/* ── Divider ── */
hr { border: none; border-top: 1px solid var(--border); margin: 20px 0; }

/* ── Streamlit native metric widget — ensure dark readable text ── */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px !important;
}
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] {
    color: #5a7080 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] > div {
    color: #2c3e50 !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    color: #5a9e7c !important;
}

/* ── Hide streamlit default elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 24px !important; padding-bottom: 40px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────
PALETTE = ["#7c9e8f", "#4a6274", "#e8836e", "#c9a84c", "#6b9eb8", "#b07eb8"]
CHART_LAYOUT = dict(
    font_family="DM Sans, sans-serif",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#2c3e50",
    title_font_size=15,
    title_font_color="#2c3e50",
    margin=dict(t=50, b=30, l=10, r=10),
    legend=dict(
        bgcolor="rgba(255,255,255,0.95)",
        bordercolor="#c8d4de",
        borderwidth=1,
        font_size=13,
        font_color="#2c3e50",
        title_font_color="#2c3e50"
    )
)

def style_chart(fig, show_grid=True):
    fig.update_layout(**CHART_LAYOUT)
    axis_style = dict(
        tickfont=dict(color="#2c3e50", size=12, family="DM Sans, sans-serif"),
        title_font=dict(color="#2c3e50", size=13, family="DM Sans, sans-serif"),
        tickcolor="#2c3e50",
        linecolor="#c8d4de",
        linewidth=1,
        zeroline=False,
    )
    if show_grid:
        fig.update_xaxes(showgrid=True, gridcolor="#e4eaf0", **axis_style)
        fig.update_yaxes(showgrid=True, gridcolor="#e4eaf0", **axis_style)
    else:
        fig.update_xaxes(showgrid=False, **axis_style)
        fig.update_yaxes(showgrid=False, **axis_style)
    return fig


# ─────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="sidebar-logo-icon">🏗️</span>
        <p class="sidebar-logo-title">Project Hub</p>
        <p class="sidebar-logo-sub">INTELLIGENCE DASHBOARD</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📤 Data Source")
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx"],
        help="Upload your Master Progress Report (.xlsx)"
    )

    st.markdown("---")

# ─────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────
if uploaded_file is None:
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">PROJECT INTELLIGENCE HUB</div>
        <p class="hero-title">🏗️ Advanced Progress Dashboard</p>
        <p class="hero-subtitle">Upload your Master Progress Report to unlock full analytics, forecasting & insights</p>
    </div>
    """, unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1,2,1])
    with col_b:
        st.info("👈  Use the sidebar to upload your **Master Progress Report (.xlsx)** to get started.")
    st.stop()

df = pd.read_excel(uploaded_file)
df["Month_Label"] = pd.to_datetime(df["Month"]).dt.strftime("%b %Y")
df["Month_Num"] = pd.to_datetime(df["Month"]).dt.month
month_order = df.drop_duplicates("Month").sort_values("Month")["Month_Label"].tolist()
df["Month_Label"] = pd.Categorical(df["Month_Label"], categories=month_order, ordered=True)

# ─────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filters")

    all_areas = sorted(df["Area"].unique())
    area_filter = st.multiselect(
        "📍 Select Area(s)",
        options=all_areas,
        default=all_areas
    )

    all_months = month_order
    month_filter = st.multiselect(
        "📅 Select Month(s)",
        options=all_months,
        default=all_months
    )

    st.markdown("---")
    st.markdown("### 🎛️ Chart Style")
    chart_style = st.radio(
        "Bar chart mode",
        options=["Grouped", "Stacked"],
        horizontal=True
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px; color:rgba(255,255,255,.35); text-align:center; padding-top:8px;">
        Project Intelligence Hub v2.0<br>Advanced Analytics & Forecasting
    </div>
    """, unsafe_allow_html=True)

filtered_df = df[
    (df["Area"].isin(area_filter)) &
    (df["Month_Label"].isin(month_filter))
].copy()

if filtered_df.empty:
    st.warning("⚠️ No data matches your filter selection. Please adjust the filters.")
    st.stop()

# ─────────────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────────────
latest_month = df.sort_values("Month")["Month_Label"].iloc[-1]
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-badge">PROJECT INTELLIGENCE HUB</div>
    <p class="hero-title">🏗️ Advanced Project Progress Dashboard</p>
    <p class="hero-subtitle">Real-time analytics · Trend forecasting · Area-wise insights &nbsp;|&nbsp; Latest data: {latest_month}</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────────────
total_boq    = filtered_df.groupby("Area")["Planned_Target (BOQ)"].max().sum()
# Use latest month's completed per area (not cumulative across months)
latest_comp  = filtered_df.sort_values("Month").groupby("Area")["Actual_Completed"].last().sum()
completed    = latest_comp
balance      = filtered_df.sort_values("Month").groupby("Area")["Balance_Work"].last().sum()
boq_pct      = round((completed / total_boq) * 100, 1) if total_boq > 0 else 0
avg_physical  = round(filtered_df["Physical_Progress (%)"].mean(), 1)
avg_financial = round(filtered_df["Financial_Progress (%)"].mean(), 1)
eff_gap = round(avg_physical - avg_financial, 1)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card sage">
        <span class="kpi-icon">🏙️</span>
        <div class="kpi-value">{filtered_df['Area'].nunique()}</div>
        <div class="kpi-label">Active Areas</div>
        <div class="kpi-delta up">▲ {len(month_filter)} months tracked</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card slate">
        <span class="kpi-icon">📦</span>
        <div class="kpi-value">{int(completed):,}</div>
        <div class="kpi-label">Units Completed</div>
        <div class="kpi-delta {'up' if boq_pct >= 50 else 'down'}">{boq_pct}% of BOQ target</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card accent">
        <span class="kpi-icon">📈</span>
        <div class="kpi-value">{avg_physical}%</div>
        <div class="kpi-label">Avg Physical Progress</div>
        <div class="kpi-delta {'up' if eff_gap >= 0 else 'down'}">{'↑' if eff_gap >= 0 else '↓'} {abs(eff_gap)}% vs financial</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card gold">
        <span class="kpi-icon">⚖️</span>
        <div class="kpi-value">{int(balance):,}</div>
        <div class="kpi-label">Balance Work</div>
        <div class="kpi-delta down">Remaining units</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📌 Executive Summary",
    "📊 Comparison Charts",
    "📉 Trend Analysis",
    "📍 Data Explorer",
    "🔮 AI Forecast"
])


# ══════════════════════════════════════════════════════
# TAB 1 – EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">📌 Area Performance Overview</div>', unsafe_allow_html=True)

    area_perf = filtered_df.groupby("Area").agg(
        Avg_Physical=("Physical_Progress (%)", "mean"),
        Avg_Financial=("Financial_Progress (%)", "mean"),
        Total_Completed=("Actual_Completed", "sum"),
        Total_BOQ=("Planned_Target (BOQ)", "max"),
        Balance=("Balance_Work", "min"),
    ).reset_index()
    # Use the latest month's Actual_Completed (not cumulative sum) vs BOQ target
    latest_completed = filtered_df.sort_values("Month").groupby("Area")["Actual_Completed"].last().reset_index()
    latest_completed.columns = ["Area", "Latest_Completed"]
    area_perf = area_perf.merge(latest_completed, on="Area", how="left")
    area_perf["BOQ_Pct"] = (area_perf["Latest_Completed"] / area_perf["Total_BOQ"] * 100).round(1)
    area_perf["Gap"] = (area_perf["Avg_Physical"] - area_perf["Avg_Financial"]).round(1)

    best  = area_perf.loc[area_perf["Avg_Physical"].idxmax()]
    worst = area_perf.loc[area_perf["Avg_Physical"].idxmin()]

    ca, cb = st.columns(2)
    with ca:
        st.markdown(f"""
        <div class="perf-best">
            <span style="font-size:22px">🏆</span>
            <div>
                <strong>Best Performing</strong><br>
                <span style="font-size:18px;font-weight:700;">{best['Area']}</span>
                &nbsp;—&nbsp; {round(best['Avg_Physical'],1)}% avg physical progress
            </div>
        </div>""", unsafe_allow_html=True)
    with cb:
        st.markdown(f"""
        <div class="perf-worst">
            <span style="font-size:22px">⚠️</span>
            <div>
                <strong>Needs Attention</strong><br>
                <span style="font-size:18px;font-weight:700;">{worst['Area']}</span>
                &nbsp;—&nbsp; {round(worst['Avg_Physical'],1)}% avg physical progress
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">📊 Area Scorecard</div>', unsafe_allow_html=True)

    for _, row in area_perf.iterrows():
        with st.expander(f"📍 {row['Area']}  ·  Physical {round(row['Avg_Physical'],1)}%  |  Financial {round(row['Avg_Financial'],1)}%", expanded=False):
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Physical Progress", f"{round(row['Avg_Physical'],1)}%")
            mc2.metric("Financial Progress", f"{round(row['Avg_Financial'],1)}%")
            mc3.metric("BOQ Completion", f"{row['BOQ_Pct']}%")
            mc4.metric("Balance Work", int(row['Balance']))

            phys_val = row['Avg_Physical'] / 100
            fin_val = row['Avg_Financial'] / 100

            fig_g = go.Figure(go.Bar(
                x=["Physical", "Financial", "BOQ Progress"],
                y=[row['Avg_Physical'], row['Avg_Financial'], row['BOQ_Pct']],
                marker_color=[PALETTE[0], PALETTE[1], PALETTE[3]],
                text=[f"{row['Avg_Physical']:.1f}%", f"{row['Avg_Financial']:.1f}%", f"{row['BOQ_Pct']:.1f}%"],
                textposition="outside",
                width=0.5
            ))
            fig_g.update_layout(
                height=240,
                showlegend=False,
                title=f"{row['Area']} — Progress Summary",
                **CHART_LAYOUT
            )
            style_chart(fig_g)
            fig_g.update_yaxes(range=[0, 115])
            st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">🎯 Overall BOQ Achievement Gauge</div>', unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=boq_pct,
            delta={"reference": 50, "valueformat": ".1f", "suffix": "%"},
            title={"text": "Overall BOQ Completion", "font": {"size": 14, "color": "#2c3e50"}},
            gauge={"axis": {"range": [0, 100],"tickmode": "linear","tick0": 0,"dtick": 10,"tickwidth": 2,"tickcolor": "#2c3e50","tickfont": {
                "size": 14,
                "color": "#2c3e50"
                }
                            },
                "bar": {"color": "#7c9e8f"},
                "bgcolor": "#f4f7f5",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 33],  "color": "#fdf2ee"},
                    {"range": [33, 66], "color": "#faf8ee"},
                    {"range": [66, 100],"color": "#e8f5ee"},
                ],
                "threshold": {
                    "line": {"color": "#c9a84c", "width": 3},
                    "thickness": 0.75,
                    "value": 50
                }
            },
            number={"suffix": "%", "font": {"size": 36, "color": "#2c3e50"}}
        ))
        fig_gauge.update_layout(height=260, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=10,l=20,r=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with g2:
        fig_gauge2 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_physical,
            delta={"reference": avg_financial, "valueformat": ".1f", "suffix": "%"},
            title={"text": "Avg Physical vs Financial Gap", "font": {"size": 14, "color": "#2c3e50"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": "#4a6274"},
                "bgcolor": "#f0f4f7",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 33],  "color": "#fdf2ee"},
                    {"range": [33, 66], "color": "#faf8ee"},
                    {"range": [66, 100],"color": "#e8f5ee"},
                ],
                "threshold": {
                    "line": {"color": "#e8836e", "width": 3},
                    "thickness": 0.75,
                    "value": avg_financial
                }
            },
            number={"suffix": "%", "font": {"size": 36, "color": "#2c3e50"}}
        ))
        fig_gauge2.update_layout(height=260, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=10,l=20,r=20))
        st.plotly_chart(fig_gauge2, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 2 – COMPARISON CHARTS
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">📊 Planned vs Actual (BOQ) – Area Wise</div>', unsafe_allow_html=True)

    boq_grouped = filtered_df.groupby("Area").agg(
        Planned=("Planned_Target (BOQ)", "max"),
        Actual=("Actual_Completed", "sum")
    ).reset_index()

    barmode = "group" if chart_style == "Grouped" else "stack"
    fig_boq = go.Figure()
    fig_boq.add_trace(go.Bar(name="Planned (BOQ)", x=boq_grouped["Area"], y=boq_grouped["Planned"],
                              marker_color=PALETTE[0], text=boq_grouped["Planned"], textposition="outside"))
    fig_boq.add_trace(go.Bar(name="Actual Completed", x=boq_grouped["Area"], y=boq_grouped["Actual"],
                              marker_color=PALETTE[2], text=boq_grouped["Actual"], textposition="outside"))
    fig_boq.update_layout(barmode=barmode, height=380, **CHART_LAYOUT)
    style_chart(fig_boq)
    fig_boq.update_xaxes(title_text="Area")
    fig_boq.update_yaxes(title_text="Units")
    st.plotly_chart(fig_boq, use_container_width=True)

    st.markdown("---")
    cc1, cc2 = st.columns(2)

    with cc1:
        st.markdown('<div class="section-header">📈 Physical vs Financial Progress</div>', unsafe_allow_html=True)
        area_avg = filtered_df.groupby("Area").agg(
            Physical=("Physical_Progress (%)", "mean"),
            Financial=("Financial_Progress (%)", "mean")
        ).reset_index()

        fig_pf = go.Figure()
        fig_pf.add_trace(go.Bar(name="Physical %", x=area_avg["Area"], y=area_avg["Physical"].round(1),
                                 marker_color=PALETTE[0], text=area_avg["Physical"].round(1), textposition="outside"))
        fig_pf.add_trace(go.Bar(name="Financial %", x=area_avg["Area"], y=area_avg["Financial"].round(1),
                                 marker_color=PALETTE[3], text=area_avg["Financial"].round(1), textposition="outside"))
        fig_pf.update_layout(barmode="group", height=340, **CHART_LAYOUT)
        style_chart(fig_pf)
        fig_pf.update_xaxes(title_text="Area")
        fig_pf.update_yaxes(title_text="Progress (%)")
        st.plotly_chart(fig_pf, use_container_width=True)

    with cc2:
        st.markdown('<div class="section-header">⚖️ Physical–Financial Gap Analysis</div>', unsafe_allow_html=True)
        area_avg["Gap"] = (area_avg["Physical"] - area_avg["Financial"]).round(1)
        colors = [PALETTE[0] if g >= 0 else PALETTE[2] for g in area_avg["Gap"]]

        fig_gap = go.Figure(go.Bar(
            x=area_avg["Area"], y=area_avg["Gap"],
            marker_color=colors,
            text=[f"{g:+.1f}%" for g in area_avg["Gap"]],
            textposition="outside"
        ))
        fig_gap.add_hline(y=0, line_color="#8a9db0", line_dash="dash", line_width=1.5)
        fig_gap.update_layout(height=340, showlegend=False, **CHART_LAYOUT)
        style_chart(fig_gap)
        fig_gap.update_xaxes(title_text="Area")
        fig_gap.update_yaxes(title_text="Gap (%)")
        st.plotly_chart(fig_gap, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">🫧 Bubble Chart — Multi-Dimension View</div>', unsafe_allow_html=True)

    fig_bubble = px.scatter(
        filtered_df,
        x="Physical_Progress (%)",
        y="Financial_Progress (%)",
        size="Planned_Target (BOQ)",
        color="Area",
        hover_name="Area",
        hover_data=["Month_Label", "Actual_Completed", "Balance_Work"],
        title="Physical vs Financial Progress (bubble size = BOQ target)",
        color_discrete_sequence=PALETTE,
        size_max=45,
        labels={
            "Physical_Progress (%)": "Physical Progress (%)",
            "Financial_Progress (%)": "Financial Progress (%)",
            "Month_Label": "Month"
        }
    )
    fig_bubble.add_shape(type="line", x0=0, y0=0, x1=100, y1=100,
                         line=dict(color="#c9a84c", dash="dot", width=1.5))
    fig_bubble.add_annotation(x=85, y=88, text="Ideal line", showarrow=False,
                               font=dict(color="#c9a84c", size=11))
    fig_bubble.update_layout(height=420, **CHART_LAYOUT)
    style_chart(fig_bubble)
    st.plotly_chart(fig_bubble, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">🥧 Balance Work Distribution</div>', unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        bal_area = filtered_df.groupby("Area")["Balance_Work"].min().reset_index()
        fig_pie = px.pie(bal_area, names="Area", values="Balance_Work",
                         title="Balance Work by Area",
                         color_discrete_sequence=PALETTE,
                         hole=0.48)
        fig_pie.update_traces(textposition="outside", textinfo="percent+label",
                               hovertemplate="%{label}: %{value} units<extra></extra>")
        fig_pie.update_layout(height=340, **CHART_LAYOUT)
        st.plotly_chart(fig_pie, use_container_width=True)

    with p2:
        comp_area = filtered_df.groupby("Area")["Actual_Completed"].sum().reset_index()
        fig_pie2 = px.pie(comp_area, names="Area", values="Actual_Completed",
                          title="Completed Work Share by Area",
                          color_discrete_sequence=[PALETTE[2], PALETTE[3], PALETTE[1], PALETTE[0]],
                          hole=0.48)
        fig_pie2.update_traces(textposition="outside", textinfo="percent+label",
                                hovertemplate="%{label}: %{value} units<extra></extra>")
        fig_pie2.update_layout(height=340, **CHART_LAYOUT)
        st.plotly_chart(fig_pie2, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 3 – TREND ANALYSIS
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">📉 Month-over-Month Progress Trends</div>', unsafe_allow_html=True)

    trend_select = st.selectbox(
        "Select Metric to Track",
        options=["Physical_Progress (%)", "Financial_Progress (%)", "Actual_Completed", "Balance_Work"],
        format_func=lambda x: x.replace("_", " ").replace("(", "(")
    )

    fig_line = px.line(
        filtered_df.sort_values("Month"),
        x="Month_Label", y=trend_select,
        color="Area",
        markers=True,
        title=f"{trend_select.replace('_',' ')} — Monthly Trend",
        color_discrete_sequence=PALETTE,
        labels={"Month_Label": "Month", trend_select: trend_select.replace("_", " ")}
    )
    fig_line.update_traces(line_width=2.5, marker_size=8)
    fig_line.update_layout(height=400, **CHART_LAYOUT)
    style_chart(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    t1, t2 = st.columns(2)

    with t1:
        st.markdown('<div class="section-header">🔥 Heatmap — Physical Progress</div>', unsafe_allow_html=True)
        pivot = filtered_df.pivot_table(
            index="Area", columns="Month_Label", values="Physical_Progress (%)", aggfunc="mean"
        )
        fig_heat = px.imshow(
            pivot,
            color_continuous_scale=["#fdf2ee", "#e8f5ee", "#7c9e8f", "#2c3e50"],
            text_auto=True,
            title="Physical Progress Heatmap (%)",
            aspect="auto"
        )
        fig_heat.update_layout(height=320, **CHART_LAYOUT)
        style_chart(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)

    with t2:
        st.markdown('<div class="section-header">🔥 Heatmap — Financial Progress</div>', unsafe_allow_html=True)
        pivot_f = filtered_df.pivot_table(
            index="Area", columns="Month_Label", values="Financial_Progress (%)", aggfunc="mean"
        )
        fig_heat2 = px.imshow(
            pivot_f,
            color_continuous_scale=["#fdf2ee", "#faf8ee", "#c9a84c", "#2c3e50"],
            text_auto=True,
            title="Financial Progress Heatmap (%)",
            aspect="auto"
        )
        fig_heat2.update_layout(height=320, **CHART_LAYOUT)
        style_chart(fig_heat2)
        st.plotly_chart(fig_heat2, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">📊 Stacked Area — Cumulative Progress</div>', unsafe_allow_html=True)

    cum_df = filtered_df.sort_values("Month").groupby(["Month_Label","Area"])["Actual_Completed"].sum().reset_index()
    fig_area = px.area(
        cum_df,
        x="Month_Label", y="Actual_Completed",
        color="Area",
        title="Cumulative Completion by Area over Months",
        color_discrete_sequence=PALETTE,
        line_shape="spline",
        labels={"Month_Label": "Month", "Actual_Completed": "Units Completed"}
    )
    fig_area.update_layout(height=380, **CHART_LAYOUT)
    style_chart(fig_area)
    st.plotly_chart(fig_area, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">🏃 Velocity — Month-over-Month Change</div>', unsafe_allow_html=True)

    vel_area = st.selectbox("Area for velocity chart", options=sorted(df["Area"].unique()), key="vel_area")
    vel_df = df[df["Area"] == vel_area].sort_values("Month").copy()
    vel_df["Δ Physical"] = vel_df["Physical_Progress (%)"].diff()
    vel_df["Δ Financial"] = vel_df["Financial_Progress (%)"].diff()
    vel_df = vel_df.dropna()

    fig_vel = go.Figure()
    fig_vel.add_trace(go.Bar(name="Δ Physical %", x=vel_df["Month_Label"], y=vel_df["Δ Physical"],
                              marker_color=PALETTE[0]))
    fig_vel.add_trace(go.Bar(name="Δ Financial %", x=vel_df["Month_Label"], y=vel_df["Δ Financial"],
                              marker_color=PALETTE[3]))
    fig_vel.update_layout(barmode="group", height=320, title=f"Month-over-Month Progress Velocity — {vel_area}", **CHART_LAYOUT)
    style_chart(fig_vel)
    fig_vel.update_xaxes(title_text="Month")
    fig_vel.update_yaxes(title_text="Change (%)")
    st.plotly_chart(fig_vel, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 4 – DATA EXPLORER
# ══════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">📍 Interactive Data Explorer</div>', unsafe_allow_html=True)

    col_search1, col_search2 = st.columns([3,1])
    with col_search1:
        sort_col = st.selectbox("Sort by column", options=filtered_df.columns.drop(["Month","Month_Num","Month_Label"]).tolist(), index=0)
    with col_search2:
        sort_dir = st.radio("Order", ["Ascending","Descending"], horizontal=True)

    display_df = filtered_df.drop(columns=["Month","Month_Num"]).sort_values(
        sort_col, ascending=(sort_dir == "Ascending")
    ).reset_index(drop=True)

    # Rename for display
    display_df = display_df.rename(columns={"Month_Label": "Month"})

    st.dataframe(
        display_df.style
            .format({"Physical_Progress (%)": "{:.0f}%", "Financial_Progress (%)": "{:.0f}%"})
            .background_gradient(subset=["Physical_Progress (%)","Financial_Progress (%)"],
                                  cmap="Greens", vmin=0, vmax=100)
            .background_gradient(subset=["Balance_Work"], cmap="Oranges_r"),
        use_container_width=True,
        height=400
    )

    st.markdown("---")
    st.markdown('<div class="section-header">📊 Balance Work — Area & Status Breakdown</div>', unsafe_allow_html=True)

    latest_data = filtered_df.sort_values("Month").groupby("Area").last().reset_index()

    fig_bal = px.bar(
        latest_data,
        x="Area",
        y="Balance_Work",
        color="Status",
        title="Remaining Balance Work by Area (Latest Month)",
        text="Balance_Work",
        color_discrete_sequence=[PALETTE[0], PALETTE[1], PALETTE[2]],
        labels={"Balance_Work": "Balance Work (Units)", "Area": "Area"}
    )
    fig_bal.update_traces(textposition="outside")
    fig_bal.update_layout(height=360, **CHART_LAYOUT)
    style_chart(fig_bal)
    st.plotly_chart(fig_bal, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="section-header">📈 Radar — Area Multi-Metric Comparison</div>', unsafe_allow_html=True)

    radar_data = filtered_df.groupby("Area").agg(
        Physical=("Physical_Progress (%)", "mean"),
        Financial=("Financial_Progress (%)", "mean"),
        Latest_Completed=("Actual_Completed", "last"),
        BOQ_Target=("Planned_Target (BOQ)", "max"),
    ).reset_index()
    radar_data["BOQ_Pct"] = (radar_data["Latest_Completed"] / radar_data["BOQ_Target"] * 100).round(1)

    categories = ["Physical Progress", "Financial Progress", "BOQ Completion"]
    fig_radar = go.Figure()
    for _, row in radar_data.iterrows():
        vals = [row["Physical"], row["Financial"], row["BOQ_Pct"]]
        vals += vals[:1]
        cats = categories + [categories[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals, theta=cats, fill="toself",
            name=row["Area"], opacity=0.7,
            line=dict(width=2)
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        height=420,
        **CHART_LAYOUT,
        colorway=PALETTE
    )
    st.plotly_chart(fig_radar, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 5 – AI FORECAST
# ══════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">🔮 AI-Powered Forecast Engine</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns([1,2])
    with fc1:
        pred_area = st.selectbox("📍 Select Area", options=sorted(df["Area"].unique()))
        pred_metric = st.selectbox("📊 Metric to Forecast",
                                   options=["Physical_Progress (%)", "Financial_Progress (%)","Actual_Completed"],
                                   format_func=lambda x: x.replace("_"," "))
        model_type = st.radio("🧮 Model Type", ["Linear", "Polynomial (Degree 2)"], horizontal=False)
        months_ahead = st.slider("⏭️ Months to Forecast", min_value=1, max_value=6, value=3)

    area_df = df[df["Area"] == pred_area].sort_values("Month").copy()
    area_df["Month_Index"] = np.arange(len(area_df))

    X = area_df[["Month_Index"]].values
    y = area_df[pred_metric].values

    with fc2:
        if len(area_df) >= 2:
            if model_type == "Linear":
                model = LinearRegression()
                X_fit = X
            else:
                poly = PolynomialFeatures(degree=2)
                X_fit = poly.fit_transform(X)
                model = LinearRegression()

            model.fit(X_fit, y)

            # Future indices
            last_idx = area_df["Month_Index"].max()
            future_indices = np.arange(last_idx + 1, last_idx + 1 + months_ahead).reshape(-1, 1)

            if model_type == "Linear":
                predictions = model.predict(future_indices)
            else:
                predictions = model.predict(poly.transform(future_indices))

            # Next month labels
            last_month = pd.to_datetime(area_df["Month"].max())
            future_months = [(last_month + pd.DateOffset(months=i+1)).strftime("%b %Y") for i in range(months_ahead)]

            st.markdown(f"""
            <div class="pred-result">
                <div style="font-size:12px;color:rgba(255,255,255,.5);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">
                    Next Month Forecast · {pred_area}
                </div>
                <div class="pred-value">{round(predictions[0], 1)}{'%' if '%' in pred_metric else ''}</div>
                <div class="pred-label">{pred_metric.replace('_',' ')}</div>
            </div>
            """, unsafe_allow_html=True)

            # All forecast months
            for i, (month, pred) in enumerate(zip(future_months[1:], predictions[1:]), 2):
                st.markdown(f"""
                <div style="background:#f4f7f5;border:1px solid #dde4eb;border-radius:10px;
                            padding:10px 16px;margin-bottom:8px;display:flex;
                            justify-content:space-between;align-items:center;">
                    <span style="color:#4a6274;font-weight:500">📅 {month}</span>
                    <span style="color:#2c3e50;font-weight:700;font-size:18px">
                        {round(pred,1)}{'%' if '%' in pred_metric else ''}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Not enough data for forecasting (minimum 2 data points required).")

    if len(area_df) >= 2:
        st.markdown("---")
        st.markdown('<div class="section-header">📈 Forecast Chart</div>', unsafe_allow_html=True)

        # Fitted values
        X_all = np.arange(len(area_df)).reshape(-1, 1)
        if model_type == "Linear":
            fitted = model.predict(X_all)
        else:
            fitted = model.predict(poly.transform(X_all))

        fig_pred = go.Figure()

        # Actual
        fig_pred.add_trace(go.Scatter(
            x=area_df["Month_Label"].astype(str),
            y=area_df[pred_metric],
            mode="lines+markers",
            name="Actual",
            line=dict(color=PALETTE[1], width=2.5),
            marker=dict(size=9, color=PALETTE[1])
        ))

        # Fitted
        fig_pred.add_trace(go.Scatter(
            x=area_df["Month_Label"].astype(str),
            y=fitted,
            mode="lines",
            name="Trend (fitted)",
            line=dict(color=PALETTE[0], width=2, dash="dot")
        ))

        # Forecast
        fig_pred.add_trace(go.Scatter(
            x=future_months,
            y=predictions,
            mode="lines+markers",
            name="Forecast",
            line=dict(color=PALETTE[2], width=2.5, dash="dash"),
            marker=dict(size=10, symbol="diamond", color=PALETTE[2])
        ))

        # Shaded forecast zone
        fig_pred.add_vrect(
            x0=future_months[0], x1=future_months[-1],
            fillcolor=PALETTE[2], opacity=0.05,
            layer="below", line_width=0
        )

        fig_pred.update_layout(
            height=420,
            title=f"{pred_metric.replace('_',' ')} Forecast — {pred_area} ({model_type})",
            **CHART_LAYOUT
        )
        style_chart(fig_pred)
        fig_pred.update_xaxes(title_text="Month")
        fig_pred.update_yaxes(title_text=pred_metric.replace("_", " "))
        st.plotly_chart(fig_pred, use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="section-header">🏁 Completion Estimator — Days to 100%</div>', unsafe_allow_html=True)

        ec1, ec2, ec3 = st.columns(3)
        for i, area_name in enumerate(sorted(df["Area"].unique())):
            adf = df[df["Area"] == area_name].sort_values("Month").copy()
            adf["MI"] = np.arange(len(adf))
            if len(adf) >= 2:
                lm = LinearRegression().fit(adf[["MI"]], adf["Physical_Progress (%)"])
                slope = lm.coef_[0]
                current = adf["Physical_Progress (%)"].iloc[-1]
                if slope > 0:
                    months_left = (100 - current) / slope
                    color = "sage" if months_left <= 6 else ("gold" if months_left <= 12 else "accent")
                    col = [ec1, ec2, ec3][i % 3]
                    with col:
                        st.markdown(f"""
                        <div class="kpi-card {color}">
                            <span class="kpi-icon">🏁</span>
                            <div class="kpi-value">{months_left:.1f}</div>
                            <div class="kpi-label">months to 100%</div>
                            <div class="kpi-delta">📍 {area_name} · at current rate</div>
                        </div><br>
                        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:16px 0 8px;color:#8a9db0;font-size:12px;">
    🏗️ <strong>Project Intelligence Hub</strong> &nbsp;·&nbsp; Advanced Analytics & Forecasting Dashboard &nbsp;·&nbsp;
    Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
