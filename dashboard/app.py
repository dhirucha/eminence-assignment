import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Reputation Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS  —  Redesigned: Deep Navy Command Center
# ============================================================

st.markdown("""
<style>

/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg-base:      #080E1A;
    --bg-surface:   #0D1526;
    --bg-card:      #111D35;
    --bg-card-hover:#152040;
    --border:       rgba(99,178,255,0.10);
    --border-glow:  rgba(99,178,255,0.28);
    --accent-blue:  #3B82F6;
    --accent-cyan:  #06B6D4;
    --accent-green: #10B981;
    --accent-amber: #F59E0B;
    --accent-red:   #EF4444;
    --text-primary: #E8F0FF;
    --text-secondary:#8FA8CC;
    --text-dim:     #4A6080;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.main {
    background-color: var(--bg-base) !important;
}

.block-container {
    padding: 1.5rem 2.5rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label {
    color: var(--text-secondary) !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] h2 {
    font-size: 13px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: var(--accent-blue) !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid var(--border) !important;
    margin-bottom: 1.2rem !important;
}

/* ── Header ── */
.dash-header {
    text-align: center;
    padding: 2rem 0 0.5rem;
}

.dash-header h1 {
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    background: linear-gradient(135deg, #E8F0FF 0%, #3B82F6 60%, #06B6D4 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 0.3rem !important;
    line-height: 1.15 !important;
}

.dash-header p {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.04em !important;
    margin: 0 !important;
}

.live-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--accent-green);
    box-shadow: 0 0 6px var(--accent-green);
    animation: pulse 2s infinite;
    margin-right: 6px;
    vertical-align: middle;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.35; }
}

/* ── Divider ── */
hr, [data-testid="stDivider"] > hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1.1rem 1.2rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--border-glow) !important;
    box-shadow: 0 0 18px rgba(59,130,246,0.12) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 10.5px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
    color: var(--text-secondary) !important;
}

[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
    font-family: 'JetBrains Mono', monospace !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.03em !important;
}

[data-testid="stMetricDelta"] {
    font-size: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
}

/* ── Section titles ── */
.section-title {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em !important;
    margin-bottom: 0.2rem !important;
}

.section-eyebrow {
    font-size: 10px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    color: var(--accent-blue) !important;
    margin-bottom: 0.25rem !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    padding-bottom: 0 !important;
}

[data-testid="stTabs"] button[role="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: var(--text-secondary) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.1rem !important;
    border-radius: 0 !important;
    transition: all 0.15s !important;
    letter-spacing: 0.01em !important;
}

[data-testid="stTabs"] button[role="tab"]:hover {
    color: var(--text-primary) !important;
    background: transparent !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--accent-blue) !important;
    border-bottom-color: var(--accent-blue) !important;
    background: transparent !important;
}

/* ── Subheaders ── */
h2, h3 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}

h3 {
    font-size: 1rem !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

[data-testid="stDataFrame"] th {
    background: var(--bg-surface) !important;
    color: var(--text-secondary) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}

[data-testid="stDataFrame"] td {
    color: var(--text-primary) !important;
    font-size: 13px !important;
    background: var(--bg-card) !important;
}

/* ── Info / Success / Warning boxes ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 3px !important;
    font-size: 13.5px !important;
    line-height: 1.65 !important;
}

div[data-baseweb="notification"][kind="info"] {
    background: rgba(59,130,246,0.08) !important;
    border-color: var(--accent-blue) !important;
}

div[data-baseweb="notification"][kind="positive"] {
    background: rgba(16,185,129,0.08) !important;
    border-color: var(--accent-green) !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 8px !important;
    color: var(--accent-blue) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.15s !important;
}

[data-testid="stDownloadButton"] button:hover {
    background: rgba(59,130,246,0.12) !important;
    box-shadow: 0 0 12px rgba(59,130,246,0.18) !important;
}

/* ── Selectbox in main area ── */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* ── Textarea ── */
textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12.5px !important;
}

/* ── Recommendation items ── */
.rec-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 14px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-bottom: 8px;
    font-size: 13.5px;
    color: var(--text-primary);
    transition: border-color 0.2s;
}

.rec-item:hover {
    border-color: var(--border-glow);
}

.rec-icon {
    color: var(--accent-green);
    font-size: 15px;
    margin-top: 1px;
    flex-shrink: 0;
}

/* ── Plotly chart containers ── */
.js-plotly-plot {
    border-radius: 10px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border-glow); border-radius: 99px; }

</style>
""", unsafe_allow_html=True)

# ============================================================
# PLOTLY DARK TEMPLATE  (applied to every chart)
# ============================================================

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#8FA8CC", size=12),
    title_font=dict(family="Inter, sans-serif", color="#E8F0FF", size=14, weight=700),
    xaxis=dict(
        gridcolor="rgba(99,178,255,0.07)",
        linecolor="rgba(99,178,255,0.10)",
        tickcolor="rgba(99,178,255,0.10)",
        tickfont=dict(color="#8FA8CC", size=11),
    ),
    yaxis=dict(
        gridcolor="rgba(99,178,255,0.07)",
        linecolor="rgba(99,178,255,0.10)",
        tickcolor="rgba(99,178,255,0.10)",
        tickfont=dict(color="#8FA8CC", size=11),
    ),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8FA8CC")),
    margin=dict(l=24, r=24, t=44, b=24),
)

COLORS_SENTIMENT = {
    "Positive": "#10B981",
    "Neutral":  "#3B82F6",
    "Negative": "#EF4444",
}

COLOR_SEQ = ["#3B82F6","#06B6D4","#10B981","#F59E0B","#8B5CF6","#EC4899","#EF4444"]

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/classified_dataset.csv")

df = load_data()

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="dash-header">
    <h1>🏦 AI Reputation Intelligence</h1>
    <p><span class="live-dot"></span>ICICI Prudential AMC · Digital Reputation Analysis</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🔍 Filters")

driver = st.sidebar.selectbox(
    "Driver",
    ["All"] + sorted(df["Driver"].dropna().unique().tolist())
)

sub_driver = st.sidebar.selectbox(
    "Sub Driver",
    ["All"] + sorted(df["Sub driver"].dropna().unique().tolist())
)

sentiment = st.sidebar.selectbox(
    "Sentiment",
    ["All"] + sorted(df["Sentiment"].dropna().unique().tolist())
)

search = st.sidebar.text_input("Search Article")

# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()

if driver != "All":
    filtered_df = filtered_df[filtered_df["Driver"] == driver]

if sub_driver != "All":
    filtered_df = filtered_df[filtered_df["Sub driver"] == sub_driver]

if sentiment != "All":
    filtered_df = filtered_df[filtered_df["Sentiment"] == sentiment]

if search:
    filtered_df = filtered_df[
        filtered_df["combined_text"].str.contains(search, case=False, na=False)
    ]

# ============================================================
# KPI SECTION
# ============================================================

st.markdown("<p class='section-title'>📈 Overview</p>", unsafe_allow_html=True)

total_mentions = len(filtered_df)
positive = (filtered_df["Sentiment"] == "Positive").sum()
neutral   = (filtered_df["Sentiment"] == "Neutral").sum()
negative  = (filtered_df["Sentiment"] == "Negative").sum()

positive_pct = round((positive / total_mentions) * 100, 1) if total_mentions else 0
neutral_pct  = round((neutral  / total_mentions) * 100, 1) if total_mentions else 0
negative_pct = round((negative / total_mentions) * 100, 1) if total_mentions else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Mentions", total_mentions)
with c2:
    st.metric("Positive",  f"{positive}",  f"{positive_pct}%")
with c3:
    st.metric("Neutral",   f"{neutral}",   f"{neutral_pct}%")
with c4:
    st.metric("Negative",  f"{negative}",  f"{negative_pct}%")

st.divider()

# ============================================================
# TABS
# ============================================================

overview_tab, explorer_tab, insights_tab = st.tabs([
    "📊 Overview",
    "🔍 Content Explorer",
    "🧠 AI Insights"
])

# ============================================================
# OVERVIEW TAB
# ============================================================

with overview_tab:

    st.subheader("📊 Reputation Overview")

    left, right = st.columns(2)

    # ── Sentiment Donut ──
    with left:
        sentiment_fig = px.pie(
            filtered_df,
            names="Sentiment",
            title="Sentiment Distribution",
            hole=0.52,
            color="Sentiment",
            color_discrete_map=COLORS_SENTIMENT,
        )
        sentiment_fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont=dict(size=12, color="#E8F0FF"),
            marker=dict(line=dict(color="#080E1A", width=2)),
        )
        sentiment_fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(sentiment_fig, use_container_width=True)

    # ── Driver Bar ──
    with right:
        driver_count = (
            filtered_df["Driver"].value_counts().reset_index()
        )
        driver_count.columns = ["Driver", "Mentions"]
        driver_fig = px.bar(
            driver_count,
            x="Driver", y="Mentions",
            title="Reputation Driver Distribution",
            text="Mentions",
            color="Mentions",
            color_continuous_scale=["#1E3A5F", "#3B82F6", "#06B6D4"],
        )
        driver_fig.update_traces(
            textfont=dict(color="#E8F0FF", size=11),
            textposition="outside",
        )
        driver_fig.update_layout(
            **PLOTLY_LAYOUT,
            coloraxis_showscale=False,
            xaxis_title="Driver",
            yaxis_title="Mentions",
        )
        st.plotly_chart(driver_fig, use_container_width=True)

    st.divider()

    # ── Sub-driver + Word Cloud ──
    left, right = st.columns([2, 1])

    with left:
        subdriver_count = (
            filtered_df["Sub driver"].value_counts().reset_index()
        )
        subdriver_count.columns = ["Sub Driver", "Mentions"]
        subdriver_fig = px.bar(
            subdriver_count,
            x="Sub Driver", y="Mentions",
            title="Sub-driver Distribution",
            text="Mentions",
            color="Mentions",
            color_continuous_scale=["#1E3A5F", "#06B6D4", "#10B981"],
        )
        subdriver_fig.update_traces(
            textfont=dict(color="#E8F0FF", size=11),
            textposition="outside",
        )
        subdriver_fig.update_layout(
            **PLOTLY_LAYOUT,
            coloraxis_showscale=False,
            xaxis_tickangle=-30,
        )
        st.plotly_chart(subdriver_fig, use_container_width=True)

    with right:
        st.subheader("☁️ Word Cloud")
        text = " ".join(filtered_df["combined_text"].astype(str))
        wordcloud = WordCloud(
            width=800, height=500,
            background_color="#111D35",
            colormap="Blues",
            max_words=120,
            prefer_horizontal=0.85,
        ).generate(text)
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor("#111D35")
        ax.set_facecolor("#111D35")
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    st.divider()

    # ── Top Discussion Themes ──
    st.subheader("🔥 Top Discussion Themes")

    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer(stop_words="english", max_features=15)
    X = vectorizer.fit_transform(filtered_df["combined_text"])
    themes = vectorizer.get_feature_names_out()
    freq   = X.sum(axis=0).A1

    theme_df = (
        pd.DataFrame({"Theme": themes, "Frequency": freq})
        .sort_values("Frequency", ascending=False)
    )

    theme_fig = px.bar(
        theme_df,
        x="Theme", y="Frequency",
        title="Top Discussion Themes",
        text="Frequency",
        color="Frequency",
        color_continuous_scale=["#1E3A5F", "#3B82F6", "#06B6D4"],
    )
    theme_fig.update_traces(
        textfont=dict(color="#E8F0FF", size=11),
        textposition="outside",
    )
    theme_fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
    st.plotly_chart(theme_fig, use_container_width=True)

    st.divider()

    # ── Recent Mentions ──
    st.subheader("📰 Recent Digital Mentions")

    display_columns = ["Date", "Source Name", "Title", "Driver", "Sub driver", "Sentiment"]
    available_columns = [c for c in display_columns if c in filtered_df.columns]

    st.dataframe(
        filtered_df[available_columns],
        use_container_width=True,
        height=350,
    )

# ============================================================
# CONTENT EXPLORER TAB
# ============================================================

with explorer_tab:

    st.subheader("🔍 Content Explorer")
    st.markdown(
        "<span style='color:#8FA8CC;font-size:13px;'>Browse and search digital mentions using filters.</span>",
        unsafe_allow_html=True,
    )
    st.divider()

    left, right = st.columns([1, 3])

    with left:
        st.metric("Showing", len(filtered_df))

    with right:
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name="filtered_mentions.csv",
            mime="text/csv",
        )

    st.divider()

    display_columns = ["Date", "Source Name", "Title", "Driver", "Sub driver", "Sentiment"]
    available_columns = [c for c in display_columns if c in filtered_df.columns]
    st.dataframe(filtered_df[available_columns], use_container_width=True, height=350)

    st.divider()

    if len(filtered_df) > 0:

        article_titles = filtered_df["Title"].fillna("Untitled Article").tolist()
        selected_title = st.selectbox("Select an Article", article_titles)

        selected_row = (
            filtered_df[filtered_df["Title"] == selected_title].iloc[0]
        )

        st.divider()
        st.subheader("📰 Article Details")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("### Metadata")
            st.write("**Date:**",       selected_row.get("Date", "N/A"))
            st.write("**Source:**",     selected_row.get("Source Name", "N/A"))
            st.write("**Sentiment:**",  selected_row.get("Sentiment", "N/A"))
            st.write("**Driver:**",     selected_row.get("Driver", "N/A"))
            st.write("**Sub Driver:**", selected_row.get("Sub driver", "N/A"))
            reach = selected_row.get("Reach", None)
            if pd.notna(reach):
                st.write("**Reach:**", reach)

        with c2:
            st.markdown("### Original Title")
            st.info(selected_row.get("Title", "No Title"))
            if pd.notna(selected_row.get("URL", None)):
                st.markdown(f"🔗 [Open Original Article]({selected_row['URL']})")

        st.divider()
        st.subheader("📄 Original Content")
        st.write(selected_row.get("combined_text", "No content available."))

    else:
        st.warning("No records match the selected filters.")

# ============================================================
# AI INSIGHTS TAB
# ============================================================

with insights_tab:

    st.subheader("🧠 AI Reputation Insights")
    st.markdown(
        "<span style='color:#8FA8CC;font-size:13px;'>Automatically generated insights based on the classified digital mentions.</span>",
        unsafe_allow_html=True,
    )
    st.divider()

    col1, col2 = st.columns(2)

    # ── Positive Drivers ──
    with col1:
        st.markdown("### ✅ Positive Reputation Drivers")
        positive_driver = (
            filtered_df[filtered_df["Sentiment"] == "Positive"]["Driver"]
            .value_counts().reset_index()
        )
        positive_driver.columns = ["Driver", "Mentions"]

        if len(positive_driver):
            fig = px.bar(
                positive_driver,
                x="Driver", y="Mentions",
                text="Mentions",
                title="Positive Reputation Drivers",
                color="Mentions",
                color_continuous_scale=["#064E3B", "#10B981", "#34D399"],
            )
            fig.update_traces(textfont=dict(color="#E8F0FF", size=11), textposition="outside")
            fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No positive mentions found.")

    # ── Negative Drivers ──
    with col2:
        st.markdown("### ❌ Negative Reputation Drivers")
        negative_driver = (
            filtered_df[filtered_df["Sentiment"] == "Negative"]["Driver"]
            .value_counts().reset_index()
        )
        negative_driver.columns = ["Driver", "Mentions"]

        if len(negative_driver):
            fig = px.bar(
                negative_driver,
                x="Driver", y="Mentions",
                text="Mentions",
                title="Negative Reputation Drivers",
                color="Mentions",
                color_continuous_scale=["#7F1D1D", "#EF4444", "#FCA5A5"],
            )
            fig.update_traces(textfont=dict(color="#E8F0FF", size=11), textposition="outside")
            fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No negative mentions found.")

    st.divider()

    # ── Key Findings ──
    st.subheader("📌 Key Findings")

    top_driver       = filtered_df["Driver"].value_counts().idxmax()
    top_driver_count = filtered_df["Driver"].value_counts().max()
    top_subdriver    = filtered_df["Sub driver"].value_counts().idxmax()

    st.success(f"""
• **Total Mentions:** {len(filtered_df)}

• **Dominant Reputation Driver:** {top_driver} ({top_driver_count} mentions)

• **Most Frequent Sub-driver:** {top_subdriver}

• **Positive Mentions:** {positive}

• **Neutral Mentions:** {neutral}

• **Negative Mentions:** {negative}
""")

    st.divider()

    # ── Executive Summary ──
    st.subheader("📈 Executive Summary")

    st.info(f"""
The analysis of **{len(filtered_df)} digital mentions** indicates that
**{top_driver}** is the dominant reputation driver.

Most media discussions revolve around **{top_subdriver}**, suggesting
that digital conversations primarily focus on leadership,
product strategy, and customer experience.

Overall sentiment is largely **Neutral**, followed by a healthy number
of **Positive** mentions, while **Negative** coverage remains relatively low.

This indicates that ICICI Prudential AMC maintains a generally stable
digital reputation with opportunities to further strengthen customer
experience and responsible business communication.
""")

    st.divider()

    # ── Recommendations ──
    st.subheader("💡 Recommendations")

    recommendations = [
        "Increase thought leadership articles from senior leadership.",
        "Promote positive customer success stories across digital channels.",
        "Strengthen digital engagement around new investment products.",
        "Improve communication around customer complaints and resolutions.",
        "Increase visibility of CSR and responsible business initiatives.",
    ]

    for rec in recommendations:
        st.markdown(
            f'<div class="rec-item"><span class="rec-icon">✓</span><span>{rec}</span></div>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Generated Insights Report ──
    st.subheader("📄 Generated Insights Report")

    try:
        with open("output/reports/insights.txt", "r", encoding="utf-8") as f:
            report = f.read()
        st.text_area("Insights Report", report, height=350)
    except FileNotFoundError:
        st.warning("Run insights.py to generate the report.")

    st.divider()

    # ── Footer ──
    st.markdown("""
<div style="text-align:center;padding:1rem 0 0.5rem;color:#4A6080;font-size:12px;letter-spacing:0.04em;">
    AI &amp; Data Solutions Specialist Assignment &nbsp;·&nbsp;
    Built with <span style="color:#3B82F6;">Python · Pandas · Mistral AI · Plotly · Streamlit</span>
</div>
""", unsafe_allow_html=True)