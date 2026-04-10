import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Municipal Grievance Dashboard", layout="wide", page_icon="🏙️")

st.markdown("""
<style>
    .kpi-card {
        background: #1e2130; border-radius: 12px; padding: 18px 22px;
        text-align: center; border: 1px solid #2e3250;
    }
    .kpi-label { font-size: 13px; color: #9aa0b4; margin-bottom: 4px; }
    .kpi-value { font-size: 28px; font-weight: 700; color: #e8eaf6; }
    .kpi-sub   { font-size: 12px; color: #6c7293; margin-top: 2px; }
    .section-title {
        font-size: 17px; font-weight: 600; color: #c5cae9;
        margin: 18px 0 8px 0; border-left: 4px solid #5c6bc0; padding-left: 10px;
    }
    .chart-placeholder {
        background: #1e2130; border: 1px dashed #2e3250; border-radius: 10px;
        min-height: 300px; display: flex; align-items: center; justify-content: center;
        color: #6c7293; font-size: 14px; margin: 4px 0;
    }
    .chart-placeholder-sm {
        background: #1e2130; border: 1px dashed #2e3250; border-radius: 10px;
        min-height: 220px; display: flex; align-items: center; justify-content: center;
        color: #6c7293; font-size: 14px; margin: 4px 0;
    }
    div[data-testid="stSidebar"] { background: #12141f; }
    /* Force all pyplot containers to never collapse */
    div[data-testid="stImage"] img { min-height: 200px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    import requests
    url = "https://github.com/VRAJPATEL621204/grievance-analytics-project/releases/download/version/grievance_dataset.json"
    response = requests.get(url, timeout=120)
    if response.status_code != 200:
        st.error("Failed to fetch dataset from GitHub releases.")
        st.stop()
    data = response.json()
    df = pd.json_normalize(data)

    df['recvd_date'] = pd.to_datetime(df['recvd_date.$date'], errors='coerce').dt.tz_localize(None)
    df['closing_date'] = pd.to_datetime(df['closing_date.$date'], errors='coerce').dt.tz_localize(None)

    df['resolution_days'] = (df['closing_date'] - df['recvd_date']).dt.days

    df['main_category'] = (
        df['subject_content_text'].astype(str)
        .str.split(">>").str[0].str.strip()
    )
    # Drop rows where category looks like free-form complaint text (not a real category)
    # Real categories: short, no newlines, don't start with salutations
    junk_patterns = r'^(dear|respected|sir|madam|to\s|sub:|subject:|i\s|we\s|this\s|please|kindly|my\s|our\s)'
    df['main_category'] = df['main_category'].where(
        (df['main_category'].str.len() <= 80) &
        (~df['main_category'].str.contains('\n', na=True)) &
        (~df['main_category'].str.lower().str.match(junk_patterns, na=True)),
        other='Uncategorized'
    )
    df = df[df['main_category'] != 'Uncategorized']  # exclude junk from analysis

    df['state'] = df['state'].astype(str).str.upper().str.strip()

    state_map = {
    "UP": "Uttar Pradesh",
    "MH": "Maharashtra",
    "BR": "Bihar",
    "BH": "Bihar",
    "RJ": "Rajasthan",
    "MP": "Madhya Pradesh",
    "GJ": "Gujarat",
    "WB": "West Bengal",
    "TN": "Tamil Nadu",
    "HY": "Haryana",
    "PB": "Punjab",
    "AS": "Assam",
    "SK": "Sikkim",
    "JH": "Jharkhand",
    "DH": "Delhi",
    "LD": "Lakshadweep",
    "JK": "Jammu & Kashmir",
    "LK": "Ladakh",
    "PC": "Puducherry",
    "TG": "Telangana",
    "OR": "Odisha",
    "AP": "Andhra Pradesh",
    "CG": "Chhattisgarh",
    "CH": "Chandigarh",
    "DD": "Daman & Diu",
    "DN": "Dadra & Nagar Haveli",
    "GD": "Goa",
    "HP": "Himachal Pradesh",
    "KN": "Karnataka",
    "KL": "Kerala",
    "MN": "Manipur",
    "MG": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "TR": "Tripura",
    "UC": "Uttarakhand",
    "AN": "Andaman & Nicobar",
    "AR": "Arunachal Pradesh"
}

    df['state_full'] = df['state'].map(state_map).fillna(df['state'])

    df['district_clean'] = df['dist_name']

    df = df.dropna(subset=['recvd_date'])

    df = df[[
        'state_full',
        'main_category',
        'resolution_days',
        'recvd_date',
        'closing_date',
        'district_clean'
    ]]

    top_cats = df['main_category'].value_counts().head(10).index.tolist()

    return df, top_cats

# LOAD DATA
with st.spinner("Loading data... please wait ⏳"):
    df, TOP_CATS = load_data()

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.caption(f"📦 Dataset total: {len(df):,} rows")
    st.markdown("---")

    sel_state = st.selectbox("🗺️ State", ["All"] + sorted(df['state_full'].dropna().unique()), key="sel_state")

    sel_district = "All"
    if sel_state != "All":
        dists = sorted(
            d for d in df[df['state_full'] == sel_state]['district_clean'].dropna().unique()
            if d not in ('', 'N/A', 'Nan', 'None')
        )
        if dists:
            sel_district = st.selectbox("🏘️ District", ["All"] + dists, key="sel_district")

    sel_cats = st.multiselect(
        "📂 Category (top 10)", options=TOP_CATS, default=TOP_CATS, key="sel_cats",
        help="Select one or more complaint categories"
    )
    if not sel_cats:
        sel_cats = TOP_CATS

    valid_res = df['resolution_days'].dropna()
    res_max = min(int(valid_res.max()) if len(valid_res) > 0 else 365, 365)
    res_range = st.slider("⏱️ Resolution Days (max)", 0, res_max, res_max, step=1, key="res_slider")

    if 'recvd_date' in df.columns and df['recvd_date'].notna().any():
        ds_min = df['recvd_date'].dropna().min().date()
        ds_max = df['recvd_date'].dropna().max().date()
    else:
        # fallback to avoid crash
        ds_min = pd.Timestamp("2023-01-01").date()
        ds_max = pd.Timestamp("2023-12-31").date()
    date_range = st.date_input(
        "Date Range", value=(ds_min, ds_max),
        min_value=ds_min, max_value=ds_max, key="date_range"
    )
    # Guard: if user is mid-selection (only start picked), default to full range
    if not isinstance(date_range, (list, tuple)) or len(date_range) < 2:
        date_range = (ds_min, ds_max)

# ── Apply Filters ───────────────────────────────────────────────────────────
fdf = df.copy()

if sel_state != "All":
    fdf = fdf[fdf['state_full'] == sel_state]

if sel_district != "All":
    fdf = fdf[fdf['district_clean'] == sel_district]

if set(sel_cats) != set(TOP_CATS):
    fdf = fdf[fdf['main_category'].isin(sel_cats)]

fdf = fdf[fdf['resolution_days'].fillna(0) <= res_range]

if isinstance(date_range, tuple) and 'recvd_date' in fdf.columns:
    fdf = fdf[
        (fdf['recvd_date'] >= pd.Timestamp(date_range[0])) &
        (fdf['recvd_date'] <= pd.Timestamp(date_range[1]) + pd.Timedelta(days=1))
    ]

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("# 🏙️ Municipal Grievance Intelligence Dashboard")
st.caption("Dynamically adapts visualizations based on filters — only meaningful insights are shown.")
st.markdown("---")

# ── KPIs ────────────────────────────────────────────────────────────────────
total     = len(fdf)
avg_res   = fdf['resolution_days'].mean()
max_delay = fdf['resolution_days'].max()
pct_7days = ((fdf['resolution_days'] <= 7).sum() / total * 100) if total > 0 else 0

def kpi(col, icon, label, value, sub=""):
    col.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{icon} {label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>',
        unsafe_allow_html=True
    )

k1, k2, k3, k4 = st.columns(4)
kpi(k1, "📌", "Total Complaints",  f"{total:,}")
kpi(k2, "⏱️", "Avg Resolution",    f"{avg_res:.1f} days" if pd.notna(avg_res) else "N/A")
kpi(k3, "🚨", "Max Delay",         f"{int(max_delay)} days" if pd.notna(max_delay) else "N/A")
kpi(k4, "✅", "Resolved ≤ 7 Days", f"{pct_7days:.1f}%", sub="of filtered complaints")
st.markdown("<br>", unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

def placeholder(msg, small=False):
    cls = "chart-placeholder-sm" if small else "chart-placeholder"
    st.markdown(f'<div class="{cls}">ℹ️ {msg}</div>', unsafe_allow_html=True)

def make_fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor('#1e2130')
    ax.set_facecolor('#1e2130')
    return fig, ax

def style_ax(ax):
    ax.tick_params(colors='#9aa0b4', labelsize=9)
    for s in ax.spines.values():
        s.set_edgecolor('#2e3250')

if total == 0:
    st.warning("No data matches the current filters. Please adjust the sidebar filters.")
    st.stop()

# ── Category Bar ─────────────────────────────────────────────────────────────
cat_counts = fdf['main_category'].value_counts().head(10)
# Truncate long labels so they never overflow the chart
cat_counts.index = [l[:40] + '…' if len(l) > 40 else l for l in cat_counts.index]

section("📊 Complaints by Category")
if len(cat_counts) >= 1:
    n = max(len(cat_counts), 3)
    fig, ax = make_fig(12, max(n * 0.7, 4))
    style_ax(ax)
    ax.barh(cat_counts.index[::-1], cat_counts.values[::-1],
            color=sns.color_palette("viridis", len(cat_counts))[::-1])
    ax.set_xlabel("Count", color='#9aa0b4')
    # Give enough left margin for long labels
    plt.subplots_adjust(left=0.35)
    st.pyplot(fig, use_container_width=True); plt.close(fig)
else:
    placeholder("No category data available.")

# ── Pie Chart ────────────────────────────────────────────────────────────────
section("🥧 Category Distribution")
if len(cat_counts) > 2:
    fig, ax = make_fig(12, 7)
    style_ax(ax)
    # Use short labels on the pie itself, full in legend
    short_labels = [l[:25] + '…' if len(l) > 25 else l for l in cat_counts.index]
    wedges, texts, autotexts = ax.pie(
        cat_counts.values, labels=None,   # no inline labels — use legend only
        autopct='%1.1f%%', startangle=140, pctdistance=0.75,
        textprops={'color': '#ffffff', 'fontsize': 10}
    )
    for at in autotexts:
        at.set_color('#ffffff'); at.set_fontsize(10)
    ax.legend(wedges, short_labels, loc="center left",
              bbox_to_anchor=(1.0, 0.5), fontsize=10, frameon=False, labelcolor='#9aa0b4')
    plt.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)
else:
    placeholder("Need more than 2 categories for a meaningful pie chart.")

# ── Daily Trend + Resolution Histogram ──────────────────────────────────────
c3, c4 = st.columns(2)
with c3:
    section("📅 Daily Complaint Trend")
    daily = fdf.groupby(fdf['recvd_date'].dt.date).size()
    if len(daily) > 1:
        fig, ax = make_fig(6, 3.5)
        style_ax(ax)
        ax.plot(daily.index, daily.values, color='#66bb6a', linewidth=1.8)
        ax.fill_between(daily.index, daily.values, alpha=0.15, color='#66bb6a')
        plt.xticks(rotation=40, ha='right')
        ax.set_ylabel("Complaints", color='#9aa0b4')
        plt.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)
    else:
        placeholder("Not enough date variation for a trend line.", small=True)

with c4:
    section("⏱️ Resolution Time Distribution")
    res_data = fdf['resolution_days'].dropna()
    if len(res_data) > 0:
        bins = min(30, max(len(res_data) // 2, 5))
        fig, ax = make_fig(6, 3.5)
        style_ax(ax)
        ax.hist(res_data, bins=bins, color='#ffa726', edgecolor='#1e2130')
        ax.set_xlabel("Days", color='#9aa0b4'); ax.set_ylabel("Count", color='#9aa0b4')
        plt.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close(fig)
    else:
        placeholder("No resolution data available.", small=True)

# ── Geographic Analysis ──────────────────────────────────────────────────────
section("📍 Geographic Analysis")
if sel_state == "All":
    geo_counts = fdf['state_full'].value_counts().head(15)
    palette = "coolwarm"
else:
    geo_counts = fdf['district_clean'].value_counts().head(15)
    geo_counts = geo_counts[~geo_counts.index.isin(['N/A', 'Nan', 'None', 'nan', ''])]
    palette = "magma"

if len(geo_counts) >= 1:
    n = max(len(geo_counts), 3)
    # Truncate long district/state names
    geo_counts.index = [l[:35] + '…' if len(l) > 35 else l for l in geo_counts.index]
    fig, ax = make_fig(10, max(n * 0.6, 4))
    style_ax(ax)
    ax.barh(geo_counts.index[::-1], geo_counts.values[::-1],
            color=sns.color_palette(palette, len(geo_counts))[::-1])
    ax.set_xlabel("Complaints", color='#9aa0b4')
    plt.subplots_adjust(left=0.35)
    st.pyplot(fig, use_container_width=True); plt.close(fig)
else:
    placeholder("Not enough geographic data to display.")

# ── Outlier Detection ────────────────────────────────────────────────────────
section("🚨 Outlier Detection — Extreme Delays (> 50 Days)")
outliers = fdf[fdf['resolution_days'] > 50].copy()
if len(outliers) > 0:
    display_cols = [c for c in ['recvd_date', 'closing_date', 'resolution_days',
                                 'main_category', 'state_full'] if c in outliers.columns]
    out_display = (outliers[display_cols]
                   .sort_values('resolution_days', ascending=False)
                   .head(50).reset_index(drop=True))
    out_display.columns = [c.replace('_', ' ').title() for c in out_display.columns]
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.dataframe(out_display, use_container_width=True, height=280)
    with col_r:
        st.metric("Outlier Count", f"{len(outliers):,}")
        st.metric("Avg Outlier Delay", f"{outliers['resolution_days'].mean():.1f} days")
        st.metric("Max Outlier Delay", f"{int(outliers['resolution_days'].max())} days")
else:
    st.success("No extreme delays (> 50 days) found in the current filter selection.")

st.markdown("---")
st.caption("Municipal Grievance Intelligence Dashboard · Data-driven insights for authorities")