import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import io
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Project Pulse — Monitoring Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# GLOBAL CSS — Dark luxury editorial theme
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap');

:root {
    --bg-primary: #0a0a0f;
    --bg-card: #111118;
    --bg-glass: rgba(255,255,255,0.04);
    --border: rgba(255,255,255,0.08);
    --accent-gold: #f5c842;
    --accent-cyan: #00d4ff;
    --accent-rose: #ff4f7b;
    --accent-green: #00e5a0;
    --text-primary: #f0eff5;
    --text-muted: #6b6a7a;
}

/* Global reset */
.stApp {
    background: var(--bg-primary) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0,212,255,0.05) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 90%, rgba(245,200,66,0.04) 0%, transparent 60%);
    font-family: 'DM Mono', monospace;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 100% !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0d0d14 !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* Hero header */
.hero-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    line-height: 1;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.hero-badge {
    background: linear-gradient(135deg, rgba(245,200,66,0.15), rgba(245,200,66,0.05));
    border: 1px solid rgba(245,200,66,0.3);
    color: var(--accent-gold);
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    padding: 0.4rem 1rem;
    border-radius: 2rem;
}

/* KPI Cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: var(--accent-line, var(--accent-gold));
}
.kpi-card:hover { border-color: rgba(255,255,255,0.15); }
.kpi-icon { font-size: 1.4rem; margin-bottom: 0.8rem; }
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
}
.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.35rem;
}
.kpi-delta {
    position: absolute;
    top: 1.5rem; right: 1.5rem;
    font-size: 0.68rem;
    font-family: 'DM Mono', monospace;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
}
.delta-up { background: rgba(0,229,160,0.12); color: var(--accent-green); }
.delta-down { background: rgba(255,79,123,0.12); color: var(--accent-rose); }

/* Section headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Chart wrapper */
.chart-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* RAG Badge */
.rag-red { color: #ff4f7b; font-weight: 600; }
.rag-amber { color: #f5c842; font-weight: 600; }
.rag-green { color: #00e5a0; font-weight: 600; }

/* Progress bar custom */
.prog-row { margin-bottom: 1rem; }
.prog-label { display: flex; justify-content: space-between; margin-bottom: 0.3rem; }
.prog-name { font-size: 0.75rem; color: var(--text-primary); font-family: 'DM Mono'; }
.prog-pct { font-size: 0.75rem; color: var(--text-muted); font-family: 'DM Mono'; }
.prog-bar { height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }

/* Metric tile small */
.mini-stat {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    text-align: center;
}
.mini-stat-val { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; color: var(--text-primary); }
.mini-stat-lbl { font-size: 0.6rem; font-family: 'DM Mono'; color: var(--text-muted); letter-spacing: 0.1em; text-transform: uppercase; }

/* Tab styling override */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 0.2rem;
    border-bottom: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 6px 6px 0 0 !important;
    padding: 0.6rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(245,200,66,0.1) !important;
    color: var(--accent-gold) !important;
    border-bottom: 2px solid var(--accent-gold) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* Input fields */
.stTextInput input, .stSelectbox select {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
}
.stButton button {
    background: linear-gradient(135deg, #f5c842, #e8a800) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    letter-spacing: 0.05em;
}
label { color: var(--text-muted) !important; font-family: 'DM Mono' !important; font-size: 0.7rem !important; letter-spacing: 0.08em; text-transform: uppercase; }

/* Divider */
hr { border-color: var(--border) !important; }

/* DataFrame */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DATABASE
# --------------------------------------------------
conn = sqlite3.connect("progress.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS progress_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT, project TEXT, month TEXT, component TEXT, unit TEXT,
    planned_qty REAL, achieved_qty REAL, physical REAL,
    financial REAL, boq_achieved REAL, remarks TEXT
)
""")
conn.commit()

# --------------------------------------------------
# PLOTLY THEME
# --------------------------------------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#6b6a7a", size=11),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0eff5", size=10),
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
    ),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.06)", color="#6b6a7a"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.06)", color="#6b6a7a"),
)
C_GOLD  = "#f5c842"
C_CYAN  = "#00d4ff"
C_ROSE  = "#ff4f7b"
C_GREEN = "#00e5a0"
C_PURPLE= "#a78bfa"
PALETTE = [C_GOLD, C_CYAN, C_ROSE, C_GREEN, C_PURPLE, "#fb923c", "#60a5fa"]

def hex_rgba(hex_color, alpha=0.1):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

# --------------------------------------------------
# HERO HEADER
# --------------------------------------------------
now = datetime.datetime.now().strftime("%d %b %Y  •  %H:%M")
st.markdown(f"""
<div class="hero-header">
  <div>
    <div class="hero-title">Project Pulse</div>
    <div class="hero-sub">Integrated Infrastructure Monitoring Dashboard</div>
  </div>
  <div style="text-align:right">
    <div class="hero-badge">LIVE DASHBOARD</div>
    <div style="font-size:0.65rem;color:#6b6a7a;margin-top:0.5rem;font-family:'DM Mono'">{now}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab_entry, tab_summary, tab_city, tab_project, tab_timeline, tab_heatmap, tab_gap, tab_prediction, tab_data = st.tabs([
    "📝  Entry",
    "🏠  Overview",
    "🏙️  City",
    "🏗️  Project",
    "📅  Timeline",
    "🔥  Heatmap",
    "⚡  Gap Analysis",
    "🔮  Forecast",
    "📄  Data"
])

# ==================================================
# DATA ENTRY
# ==================================================
with tab_entry:
    st.markdown('<div class="section-header">Monthly Progress Entry</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    city = col1.text_input("City")
    project = col2.text_input("Project")
    month = col3.text_input("Month (e.g. Jan-2026)")

    entry_df = pd.DataFrame({
        "Component": [""], "Unit": [""],
        "Planned Qty": [0.0], "Achieved Qty": [0.0],
        "Physical %": [0.0], "Financial %": [0.0],
        "BOQ Achieved": [0.0], "Remarks": [""]
    })

    edited_df = st.data_editor(entry_df, num_rows="dynamic", use_container_width=True)

    c1, c2 = st.columns([1, 4])
    if c1.button("💾  Save Entry"):
        if city and project and month:
            saved = 0
            for _, r in edited_df.iterrows():
                if r["Component"]:
                    cur.execute("""
                        INSERT INTO progress_master
                        (city,project,month,component,unit,planned_qty,achieved_qty,physical,financial,boq_achieved,remarks)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)
                    """, (city, project, month, r["Component"], r["Unit"],
                          r["Planned Qty"], r["Achieved Qty"],
                          r["Physical %"], r["Financial %"],
                          r["BOQ Achieved"], r["Remarks"]))
                    saved += 1
            conn.commit()
            st.success(f"✅ {saved} row(s) saved successfully")
        else:
            st.error("City, Project, and Month are required")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_sql("SELECT * FROM progress_master", conn)

if df.empty:
    for t in [tab_summary, tab_city, tab_project, tab_timeline, tab_heatmap, tab_gap, tab_prediction, tab_data]:
        with t:
            st.markdown("""
            <div style="text-align:center;padding:5rem 0;color:#6b6a7a;">
                <div style="font-size:3rem;margin-bottom:1rem">📭</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.2rem;color:#f0eff5">No data yet</div>
                <div style="font-size:0.75rem;margin-top:0.5rem">Use the Entry tab to add project progress data</div>
            </div>""", unsafe_allow_html=True)
    st.stop()

# --------------------------------------------------
# RAG + EFFICIENCY
# --------------------------------------------------
def rag_status(p):
    if p < 40:   return "🔴 Red"
    elif p < 70: return "🟠 Amber"
    else:        return "🟢 Green"

def rag_color(p):
    if p < 40:   return C_ROSE
    elif p < 70: return C_GOLD
    else:        return C_GREEN

df["RAG Status"] = df["physical"].apply(rag_status)
df["Efficiency"] = (df["achieved_qty"] / df["planned_qty"].replace(0, np.nan) * 100).round(1)
df["Variance"] = (df["physical"] - df["financial"]).round(1)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.markdown("""
<div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#f0eff5;margin-bottom:1.2rem;padding-bottom:0.8rem;border-bottom:1px solid rgba(255,255,255,0.08)">
  🔍 Filters
</div>
""", unsafe_allow_html=True)

city_f  = st.sidebar.multiselect("City",    df["city"].unique(),    df["city"].unique())
proj_f  = st.sidebar.multiselect("Project", df["project"].unique(), df["project"].unique())
month_f = st.sidebar.multiselect("Month",   df["month"].unique(),   df["month"].unique())

fdf = df[
    df["city"].isin(city_f) &
    df["project"].isin(proj_f) &
    df["month"].isin(month_f)
].copy()

if fdf.empty:
    st.sidebar.warning("No data matches filters")
    st.stop()

# Sidebar mini-stats
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem">
  <div class="mini-stat"><div class="mini-stat-val">{fdf['city'].nunique()}</div><div class="mini-stat-lbl">Cities</div></div>
  <div class="mini-stat"><div class="mini-stat-val">{fdf['project'].nunique()}</div><div class="mini-stat-lbl">Projects</div></div>
  <div class="mini-stat"><div class="mini-stat-val">{fdf['component'].nunique()}</div><div class="mini-stat-lbl">Components</div></div>
  <div class="mini-stat"><div class="mini-stat-val">{fdf['month'].nunique()}</div><div class="mini-stat-lbl">Months</div></div>
</div>
""", unsafe_allow_html=True)

# rag counts
r_green = (fdf["physical"] >= 70).sum()
r_amber = ((fdf["physical"] >= 40) & (fdf["physical"] < 70)).sum()
r_red   = (fdf["physical"] < 40).sum()
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="font-family:'DM Mono';font-size:0.65rem;color:#6b6a7a;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.6rem">RAG Distribution</div>
<div style="display:flex;flex-direction:column;gap:0.4rem">
  <div style="display:flex;justify-content:space-between"><span style="color:#00e5a0">🟢 On Track</span><span style="color:#f0eff5;font-weight:600">{r_green}</span></div>
  <div style="display:flex;justify-content:space-between"><span style="color:#f5c842">🟠 At Risk</span><span style="color:#f0eff5;font-weight:600">{r_amber}</span></div>
  <div style="display:flex;justify-content:space-between"><span style="color:#ff4f7b">🔴 Critical</span><span style="color:#f0eff5;font-weight:600">{r_red}</span></div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SUMMARY / OVERVIEW
# ==================================================
with tab_summary:
    avg_phy = fdf["physical"].mean()
    avg_fin = fdf["financial"].mean()
    avg_eff = fdf["Efficiency"].mean()
    avg_boq = fdf["boq_achieved"].mean()

    # KPI Row
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card" style="--accent-line:{C_GOLD}">
        <div class="kpi-icon">📐</div>
        <div class="kpi-value">{avg_phy:.1f}%</div>
        <div class="kpi-label">Avg Physical Progress</div>
        <div class="kpi-delta {'delta-up' if avg_phy>=50 else 'delta-down'}">{"▲" if avg_phy>=50 else "▼"} {avg_phy:.1f}%</div>
      </div>
      <div class="kpi-card" style="--accent-line:{C_CYAN}">
        <div class="kpi-icon">💰</div>
        <div class="kpi-value">{avg_fin:.1f}%</div>
        <div class="kpi-label">Avg Financial Progress</div>
        <div class="kpi-delta {'delta-up' if avg_fin>=50 else 'delta-down'}">{"▲" if avg_fin>=50 else "▼"} {avg_fin:.1f}%</div>
      </div>
      <div class="kpi-card" style="--accent-line:{C_GREEN}">
        <div class="kpi-icon">⚙️</div>
        <div class="kpi-value">{avg_eff:.1f}%</div>
        <div class="kpi-label">Avg Execution Efficiency</div>
        <div class="kpi-delta {'delta-up' if avg_eff>=80 else 'delta-down'}">{"▲" if avg_eff>=80 else "▼"} Target 100%</div>
      </div>
      <div class="kpi-card" style="--accent-line:{C_ROSE}">
        <div class="kpi-icon">📦</div>
        <div class="kpi-value">{avg_boq:.1f}%</div>
        <div class="kpi-label">Avg BOQ Achieved</div>
        <div class="kpi-delta {'delta-up' if avg_boq>=60 else 'delta-down'}">{"▲" if avg_boq>=60 else "▼"} {avg_boq:.1f}%</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-header">Physical vs Financial Progress by Project</div>', unsafe_allow_html=True)
        proj_agg = fdf.groupby("project")[["physical", "financial", "boq_achieved"]].mean().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=proj_agg["project"], y=proj_agg["physical"],
            name="Physical %", marker_color=C_GOLD,
            marker_line_width=0, opacity=0.9,
        ))
        fig.add_trace(go.Bar(
            x=proj_agg["project"], y=proj_agg["financial"],
            name="Financial %", marker_color=C_CYAN,
            marker_line_width=0, opacity=0.9,
        ))
        fig.add_trace(go.Bar(
            x=proj_agg["project"], y=proj_agg["boq_achieved"],
            name="BOQ Achieved %", marker_color=C_PURPLE,
            marker_line_width=0, opacity=0.9,
        ))
        fig.update_layout(**PLOTLY_LAYOUT, barmode="group", height=320,
                          title=dict(text="", font=dict(size=13)))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">RAG Distribution</div>', unsafe_allow_html=True)
        rag_counts = fdf["RAG Status"].value_counts()
        colors_map = {"🟢 Green": C_GREEN, "🟠 Amber": C_GOLD, "🔴 Red": C_ROSE}
        fig2 = go.Figure(go.Pie(
            labels=rag_counts.index,
            values=rag_counts.values,
            hole=0.65,
            marker=dict(colors=[colors_map.get(l, C_CYAN) for l in rag_counts.index],
                        line=dict(color="#0a0a0f", width=3)),
            textfont=dict(family="DM Mono", size=10, color="#f0eff5"),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>"
        ))
        fig2.add_annotation(
            text=f"<b style='font-size:22px'>{len(fdf)}</b><br>Total",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="#f0eff5", size=13, family="Syne")
        )
        fig2.update_layout(**PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig2, use_container_width=True)

    # Top/Bottom performers
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">Top 5 Components</div>', unsafe_allow_html=True)
        top5 = fdf.groupby("component")["physical"].mean().nlargest(5).reset_index()
        html = ""
        for _, row in top5.iterrows():
            pct = min(row["physical"], 100)
            color = rag_color(pct)
            html += f"""
            <div class="prog-row">
              <div class="prog-label">
                <span class="prog-name">{row['component'][:28]}</span>
                <span class="prog-pct">{pct:.1f}%</span>
              </div>
              <div class="prog-bar"><div class="prog-fill" style="width:{pct}%;background:{color}"></div></div>
            </div>"""
        st.markdown(html, unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-header">Bottom 5 Components</div>', unsafe_allow_html=True)
        bot5 = fdf.groupby("component")["physical"].mean().nsmallest(5).reset_index()
        html = ""
        for _, row in bot5.iterrows():
            pct = min(row["physical"], 100)
            color = rag_color(pct)
            html += f"""
            <div class="prog-row">
              <div class="prog-label">
                <span class="prog-name">{row['component'][:28]}</span>
                <span class="prog-pct">{pct:.1f}%</span>
              </div>
              <div class="prog-bar"><div class="prog-fill" style="width:{pct}%;background:{color}"></div></div>
            </div>"""
        st.markdown(html, unsafe_allow_html=True)

# ==================================================
# CITY ANALYSIS
# ==================================================
with tab_city:
    st.markdown('<div class="section-header">City-level Deep Dive</div>', unsafe_allow_html=True)

    city_agg = fdf.groupby("city").agg(
        physical=("physical","mean"),
        financial=("financial","mean"),
        boq_achieved=("boq_achieved","mean"),
        efficiency=("Efficiency","mean"),
        projects=("project","nunique"),
        components=("component","nunique")
    ).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(city_agg, x="city", y=["physical","financial","boq_achieved"],
                     barmode="group", color_discrete_sequence=[C_GOLD, C_CYAN, C_PURPLE],
                     labels={"value":"Progress %","variable":"Metric"})
        fig.update_layout(**PLOTLY_LAYOUT, height=320, title=dict(text="Avg Progress by City"))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.scatter(city_agg, x="physical", y="financial", size="components",
                         color="city", text="city",
                         color_discrete_sequence=PALETTE,
                         labels={"physical":"Physical %","financial":"Financial %"})
        fig.add_shape(type="line", x0=0, y0=0, x1=100, y1=100,
                      line=dict(color="rgba(255,255,255,0.15)", dash="dot"))
        fig.update_traces(textposition="top center", textfont=dict(size=9, color="#f0eff5"))
        fig.update_layout(**PLOTLY_LAYOUT, height=320,
                          title=dict(text="Physical vs Financial (bubble = components)"))
        st.plotly_chart(fig, use_container_width=True)

    # City efficiency radar
    st.markdown('<div class="section-header">City Performance Radar</div>', unsafe_allow_html=True)
    metrics = ["physical","financial","boq_achieved","efficiency"]
    labels  = ["Physical %","Financial %","BOQ Achieved","Efficiency"]
    fig_r = go.Figure()
    for i, row in city_agg.iterrows():
        vals = [row[m] for m in metrics]
        vals.append(vals[0])
        fig_r.add_trace(go.Scatterpolar(
            r=vals, theta=labels+[labels[0]],
            fill="toself", name=row["city"],
            line=dict(color=PALETTE[i % len(PALETTE)], width=2),
            fillcolor=hex_rgba(PALETTE[i % len(PALETTE)], 0.1),
            opacity=0.8
        ))
    fig_r.update_layout(**PLOTLY_LAYOUT, height=400,
                        polar=dict(
                            bgcolor="rgba(0,0,0,0)",
                            radialaxis=dict(visible=True, range=[0,100],
                                           gridcolor="rgba(255,255,255,0.06)",
                                           color="#6b6a7a"),
                            angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", color="#6b6a7a")
                        ))
    st.plotly_chart(fig_r, use_container_width=True)

# ==================================================
# PROJECT ANALYSIS
# ==================================================
with tab_project:
    st.markdown('<div class="section-header">Project-level Analytics</div>', unsafe_allow_html=True)

    proj_agg = fdf.groupby("project").agg(
        physical=("physical","mean"),
        financial=("financial","mean"),
        boq_achieved=("boq_achieved","mean"),
        efficiency=("Efficiency","mean"),
        total_planned=("planned_qty","sum"),
        total_achieved=("achieved_qty","sum"),
        cities=("city","nunique"),
        components=("component","nunique")
    ).reset_index()
    proj_agg["completion_gap"] = proj_agg["physical"] - proj_agg["financial"]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(proj_agg.sort_values("physical", ascending=True),
                     x="physical", y="project", orientation="h",
                     color="physical", color_continuous_scale=["#ff4f7b","#f5c842","#00e5a0"],
                     range_color=[0, 100],
                     labels={"physical":"Physical Progress %","project":""})
        fig.update_layout(**PLOTLY_LAYOUT, height=380,
                          title=dict(text="Physical Progress Ranking"),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.funnel(proj_agg.sort_values("physical", ascending=False),
                        x="physical", y="project",
                        color_discrete_sequence=[C_CYAN])
        fig.update_layout(**PLOTLY_LAYOUT, height=380,
                          title=dict(text="Project Funnel — Physical Progress"))
        st.plotly_chart(fig, use_container_width=True)

    # Efficiency vs Physical scatter
    st.markdown('<div class="section-header">Efficiency vs Progress Matrix</div>', unsafe_allow_html=True)
    fig = px.scatter(proj_agg, x="physical", y="efficiency",
                     size="components", color="financial",
                     text="project",
                     color_continuous_scale=["#ff4f7b","#f5c842","#00e5a0"],
                     size_max=40,
                     labels={"physical":"Physical %","efficiency":"Efficiency %","financial":"Financial %"})
    fig.add_hline(y=100, line_dash="dot", line_color="rgba(255,255,255,0.15)",
                  annotation_text="100% Efficiency", annotation_font_color="#6b6a7a")
    fig.add_vline(x=70, line_dash="dot", line_color="rgba(255,255,255,0.15)",
                  annotation_text="70% threshold", annotation_font_color="#6b6a7a")
    fig.update_traces(textposition="top center", textfont=dict(size=9, color="#f0eff5"))
    fig.update_layout(**PLOTLY_LAYOUT, height=360,
                      title=dict(text="Projects: Efficiency vs Physical Progress (size = # components)"))
    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TIMELINE
# ==================================================
with tab_timeline:
    st.markdown('<div class="section-header">Month-wise Trend Analysis</div>', unsafe_allow_html=True)

    trend = fdf.groupby("month").agg(
        physical=("physical","mean"),
        financial=("financial","mean"),
        boq_achieved=("boq_achieved","mean"),
        efficiency=("Efficiency","mean"),
        entries=("id","count")
    ).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        for col_, color_, name_ in [
            ("physical", C_GOLD, "Physical %"),
            ("financial", C_CYAN, "Financial %"),
            ("boq_achieved", C_PURPLE, "BOQ Achieved %")
        ]:
            fig.add_trace(go.Scatter(
                x=trend["month"], y=trend[col_],
                mode="lines+markers", name=name_,
                line=dict(color=color_, width=2.5),
                marker=dict(size=7, color=color_),
                fill="tozeroy",
                fillcolor=hex_rgba(color_, 0.05)
            ))
        fig.update_layout(**PLOTLY_LAYOUT, height=320,
                          title=dict(text="Monthly Average Progress Trends"))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.area(trend, x="month", y="efficiency",
                      color_discrete_sequence=[C_GREEN],
                      labels={"efficiency":"Efficiency %","month":"Month"})
        fig.update_traces(fillcolor="rgba(0,229,160,0.1)")
        fig.add_hline(y=100, line_dash="dot", line_color="rgba(255,255,255,0.15)")
        fig.update_layout(**PLOTLY_LAYOUT, height=320,
                          title=dict(text="Execution Efficiency Over Time"))
        st.plotly_chart(fig, use_container_width=True)

    # Monthly city comparison
    if fdf["city"].nunique() > 1:
        st.markdown('<div class="section-header">City × Month Progress Matrix</div>', unsafe_allow_html=True)
        city_month = fdf.groupby(["month","city"])["physical"].mean().reset_index()
        fig = px.line(city_month, x="month", y="physical", color="city",
                      color_discrete_sequence=PALETTE,
                      markers=True,
                      labels={"physical":"Physical %","month":"Month","city":"City"})
        fig.update_layout(**PLOTLY_LAYOUT, height=320,
                          title=dict(text="City-wise Physical Progress Over Time"))
        st.plotly_chart(fig, use_container_width=True)

# ==================================================
# HEATMAP
# ==================================================
with tab_heatmap:
    st.markdown('<div class="section-header">Performance Heatmaps</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        pivot = fdf.pivot_table(values="physical", index="component", columns="month", aggfunc="mean")
        if not pivot.empty:
            fig = px.imshow(pivot, color_continuous_scale=["#ff4f7b","#f5c842","#00e5a0"],
                            zmin=0, zmax=100, aspect="auto",
                            labels=dict(color="Physical %"))
            fig.update_layout(**PLOTLY_LAYOUT, height=400,
                              title=dict(text="Component × Month — Physical %"))
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        pivot2 = fdf.pivot_table(values="financial", index="project", columns="city", aggfunc="mean")
        if not pivot2.empty:
            fig2 = px.imshow(pivot2, color_continuous_scale=["#ff4f7b","#f5c842","#00e5a0"],
                             zmin=0, zmax=100, aspect="auto",
                             labels=dict(color="Financial %"))
            fig2.update_layout(**PLOTLY_LAYOUT, height=400,
                               title=dict(text="Project × City — Financial %"))
            st.plotly_chart(fig2, use_container_width=True)

    # BOQ heatmap
    st.markdown('<div class="section-header">BOQ Achieved — City × Project</div>', unsafe_allow_html=True)
    pivot3 = fdf.pivot_table(values="boq_achieved", index="project", columns="city", aggfunc="mean")
    if not pivot3.empty:
        fig3 = px.imshow(pivot3, color_continuous_scale=["#0a0a0f","#a78bfa","#00d4ff"],
                         zmin=0, zmax=100, aspect="auto",
                         labels=dict(color="BOQ %"))
        fig3.update_layout(**PLOTLY_LAYOUT, height=300,
                           title=dict(text="BOQ Achieved % Heatmap"))
        st.plotly_chart(fig3, use_container_width=True)

# ==================================================
# GAP ANALYSIS
# ==================================================
with tab_gap:
    st.markdown('<div class="section-header">Physical vs Financial Gap Analysis</div>', unsafe_allow_html=True)

    gap_proj = fdf.groupby("project").agg(
        physical=("physical","mean"),
        financial=("financial","mean")
    ).reset_index()
    gap_proj["gap"] = gap_proj["physical"] - gap_proj["financial"]
    gap_proj["gap_type"] = gap_proj["gap"].apply(
        lambda x: "Physical Ahead" if x > 0 else ("Balanced" if x == 0 else "Financial Ahead"))

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(gap_proj.sort_values("gap"),
                     x="gap", y="project", orientation="h",
                     color="gap", color_continuous_scale=["#ff4f7b","#f5c842","#00e5a0"],
                     labels={"gap":"Gap (Physical − Financial)","project":""},
                     color_continuous_midpoint=0)
        fig.add_vline(x=0, line_dash="solid", line_color="rgba(255,255,255,0.2)")
        fig.update_layout(**PLOTLY_LAYOUT, height=340,
                          title=dict(text="Physical−Financial Gap by Project"),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        gap_city = fdf.groupby("city").agg(
            physical=("physical","mean"),
            financial=("financial","mean")
        ).reset_index()
        gap_city["gap"] = gap_city["physical"] - gap_city["financial"]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=gap_city["city"], y=gap_city["physical"],
                               name="Physical", marker_color=C_GOLD))
        fig2.add_trace(go.Bar(x=gap_city["city"], y=gap_city["financial"],
                               name="Financial", marker_color=C_CYAN))
        fig2.add_trace(go.Scatter(x=gap_city["city"], y=gap_city["gap"],
                                   name="Gap", mode="lines+markers",
                                   line=dict(color=C_ROSE, width=2),
                                   marker=dict(size=8, color=C_ROSE),
                                   yaxis="y2"))
        fig2.update_layout(**PLOTLY_LAYOUT, height=340,
                            barmode="group",
                            yaxis2=dict(overlaying="y", side="right",
                                        gridcolor="rgba(255,255,255,0.04)",
                                        color="#6b6a7a", title="Gap %"),
                            title=dict(text="City-wise Physical vs Financial + Gap"))
        st.plotly_chart(fig2, use_container_width=True)

    # Component-level deviation
    st.markdown('<div class="section-header">Component Planned vs Achieved Deviation</div>', unsafe_allow_html=True)
    comp_dev = fdf.groupby("component").agg(
        planned=("planned_qty","sum"),
        achieved=("achieved_qty","sum")
    ).reset_index()
    comp_dev["deviation"] = comp_dev["achieved"] - comp_dev["planned"]
    comp_dev = comp_dev.sort_values("deviation")

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=comp_dev["component"], y=comp_dev["planned"],
        name="Planned", marker_color="rgba(255,255,255,0.15)"
    ))
    fig3.add_trace(go.Bar(
        x=comp_dev["component"], y=comp_dev["achieved"],
        name="Achieved",
        marker_color=[C_GREEN if v >= 0 else C_ROSE
                      for v in comp_dev["deviation"]]
    ))
    fig3.update_layout(**PLOTLY_LAYOUT, height=320, barmode="group",
                        title=dict(text="Component: Planned vs Achieved Quantity"))
    st.plotly_chart(fig3, use_container_width=True)

# ==================================================
# FORECAST
# ==================================================
with tab_prediction:
    st.markdown('<div class="section-header">AI Forecast — Next 3 Months</div>', unsafe_allow_html=True)

    trend_data = fdf.groupby("month")[["physical","financial","boq_achieved"]].mean().reset_index()
    trend_data["idx"] = range(len(trend_data))

    if len(trend_data) >= 2:
        for metric, color_, label in [
            ("physical", C_GOLD, "Physical %"),
            ("financial", C_CYAN, "Financial %"),
            ("boq_achieved", C_PURPLE, "BOQ Achieved %")
        ]:
            coef = np.polyfit(trend_data["idx"], trend_data[metric], 1)
            future_x = [trend_data["idx"].max() + i for i in range(1, 4)]
            future_y = np.clip(np.polyval(coef, future_x), 0, 100)

            trend_data[f"pred_{metric}"] = None

        # Combined forecast chart
        fig = go.Figure()
        future_months = ["Next-1","Next-2","Next-3"]
        preds = {}
        for metric, color_, label in [
            ("physical", C_GOLD, "Physical %"),
            ("financial", C_CYAN, "Financial %"),
        ]:
            coef = np.polyfit(trend_data["idx"], trend_data[metric], 1)
            future_y = np.clip(np.polyval(coef, [trend_data["idx"].max()+i for i in range(1,4)]), 0, 100)
            preds[metric] = future_y

            # Historical line
            fig.add_trace(go.Scatter(
                x=trend_data["month"], y=trend_data[metric],
                name=label, mode="lines+markers",
                line=dict(color=color_, width=2.5),
                marker=dict(size=7, color=color_)
            ))
            # Forecast line (dashed)
            all_x = list(trend_data["month"]) + future_months
            all_y = list(trend_data[metric]) + list(future_y)
            fig.add_trace(go.Scatter(
                x=[trend_data["month"].iloc[-1]] + future_months,
                y=[trend_data[metric].iloc[-1]] + list(future_y),
                name=f"{label} Forecast",
                mode="lines+markers",
                line=dict(color=color_, width=1.5, dash="dash"),
                marker=dict(size=6, symbol="diamond", color=color_),
                opacity=0.7
            ))

        fig.add_vrect(
            x0=future_months[0], x1=future_months[-1],
            fillcolor="rgba(245,200,66,0.04)",
            layer="below", line_width=0,
            annotation_text="Forecast Zone", annotation_position="top left",
            annotation_font=dict(color="#6b6a7a", size=10)
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=380,
                          title=dict(text="Historical + 3-Month Forecast (Linear Regression)"))
        st.plotly_chart(fig, use_container_width=True)

        # Prediction table
        st.markdown('<div class="section-header">Predicted Values</div>', unsafe_allow_html=True)
        coef_phy = np.polyfit(trend_data["idx"], trend_data["physical"], 1)
        coef_fin = np.polyfit(trend_data["idx"], trend_data["financial"], 1)
        coef_boq = np.polyfit(trend_data["idx"], trend_data["boq_achieved"], 1)
        xs = [trend_data["idx"].max()+i for i in range(1,4)]
        pred_df = pd.DataFrame({
            "Month": future_months,
            "Predicted Physical %": np.clip(np.polyval(coef_phy, xs), 0, 100).round(1),
            "Predicted Financial %": np.clip(np.polyval(coef_fin, xs), 0, 100).round(1),
            "Predicted BOQ %": np.clip(np.polyval(coef_boq, xs), 0, 100).round(1),
            "Expected RAG": [rag_status(v) for v in np.clip(np.polyval(coef_phy, xs), 0, 100)]
        })
        st.dataframe(pred_df, use_container_width=True, hide_index=True)

        # Trend angle insight
        slope = coef_phy[0]
        st.markdown(f"""
        <div style="background:rgba(245,200,66,0.06);border:1px solid rgba(245,200,66,0.2);
                    border-radius:12px;padding:1.2rem 1.5rem;margin-top:1rem">
          <div style="font-family:'Syne',sans-serif;font-size:0.9rem;color:#f5c842;margin-bottom:0.3rem">
            📈 Trend Insight
          </div>
          <div style="font-family:'DM Mono',monospace;font-size:0.8rem;color:#f0eff5">
            Physical progress is {'improving' if slope > 0 else 'declining'} at 
            <strong>{abs(slope):.2f}%/month</strong>.
            {'At this rate, all projects may reach 80% within ' + str(int((80 - trend_data["physical"].mean()) / max(slope, 0.01))) + ' months.' if slope > 0 else 'Intervention recommended to reverse trend.'}
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("At least 2 months of data required for forecasting.")

# ==================================================
# DATA TABLE
# ==================================================
with tab_data:
    st.markdown('<div class="section-header">Complete Data Table</div>', unsafe_allow_html=True)

    col_order = ["city","project","month","component","unit",
                 "planned_qty","achieved_qty","physical","financial",
                 "boq_achieved","Efficiency","Variance","RAG Status","remarks"]
    display_cols = [c for c in col_order if c in fdf.columns]

    st.dataframe(fdf[display_cols], use_container_width=True, hide_index=True,
                 column_config={
                     "physical": st.column_config.ProgressColumn("Physical %", min_value=0, max_value=100),
                     "financial": st.column_config.ProgressColumn("Financial %", min_value=0, max_value=100),
                     "Efficiency": st.column_config.NumberColumn("Efficiency %", format="%.1f %%"),
                     "Variance": st.column_config.NumberColumn("P−F Variance", format="%.1f"),
                 })

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        fdf[display_cols].to_excel(writer, index=False, sheet_name="Progress")
    st.download_button(
        label="⬇️  Download Excel Report",
        data=buffer.getvalue(),
        file_name="Project_Pulse_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
