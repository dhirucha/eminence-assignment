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
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color:#F8FAFC;
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

.metric-card{
    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.08);
    text-align:center;
}

.section-title{
    font-size:28px;
    font-weight:700;
    color:#0F172A;
}

.small-title{
    font-size:20px;
    font-weight:600;
    color:#1E293B;
}

</style>
""", unsafe_allow_html=True)

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

st.markdown(
    "<h1 style='text-align:center;'>🏦 AI Reputation Intelligence Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center;color:gray;'>ICICI Prudential AMC Digital Reputation Analysis</h4>",
    unsafe_allow_html=True
)

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

search = st.sidebar.text_input(
    "Search Article"
)

# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()

if driver != "All":
    filtered_df = filtered_df[
        filtered_df["Driver"] == driver
    ]

if sub_driver != "All":
    filtered_df = filtered_df[
        filtered_df["Sub driver"] == sub_driver
    ]

if sentiment != "All":
    filtered_df = filtered_df[
        filtered_df["Sentiment"] == sentiment
    ]

if search:
    filtered_df = filtered_df[
        filtered_df["combined_text"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    "<p class='section-title'>📈 Overview</p>",
    unsafe_allow_html=True
)

total_mentions = len(filtered_df)

positive = (
    filtered_df["Sentiment"] == "Positive"
).sum()

neutral = (
    filtered_df["Sentiment"] == "Neutral"
).sum()

negative = (
    filtered_df["Sentiment"] == "Negative"
).sum()

positive_pct = round((positive / total_mentions) * 100, 1) if total_mentions else 0
neutral_pct = round((neutral / total_mentions) * 100, 1) if total_mentions else 0
negative_pct = round((negative / total_mentions) * 100, 1) if total_mentions else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Mentions",
        total_mentions
    )

with c2:
    st.metric(
        "Positive",
        f"{positive}",
        f"{positive_pct}%"
    )

with c3:
    st.metric(
        "Neutral",
        f"{neutral}",
        f"{neutral_pct}%"
    )

with c4:
    st.metric(
        "Negative",
        f"{negative}",
        f"{negative_pct}%"
    )

st.divider()

# ============================================================
# TABS
# ============================================================

overview_tab, explorer_tab, insights_tab = st.tabs(
    [
        "📊 Overview",
        "🔍 Content Explorer",
        "🧠 AI Insights"
    ]
)

# ============================================================
# OVERVIEW TAB
# ============================================================

with overview_tab:

    st.subheader("📊 Reputation Overview")

    left, right = st.columns(2)

    # --------------------------------------------------------
    # Sentiment Distribution
    # --------------------------------------------------------

    with left:

        sentiment_fig = px.pie(
            filtered_df,
            names="Sentiment",
            title="Sentiment Distribution",
            hole=0.45
        )

        sentiment_fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            sentiment_fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Driver Distribution
    # --------------------------------------------------------

    with right:

        driver_count = (
            filtered_df["Driver"]
            .value_counts()
            .reset_index()
        )

        driver_count.columns = [
            "Driver",
            "Mentions"
        ]

        driver_fig = px.bar(
            driver_count,
            x="Driver",
            y="Mentions",
            title="Reputation Driver Distribution",
            text="Mentions"
        )

        driver_fig.update_layout(
            xaxis_title="Driver",
            yaxis_title="Mentions"
        )

        st.plotly_chart(
            driver_fig,
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------------
    # Sub-driver Distribution
    # --------------------------------------------------------

    left, right = st.columns([2,1])

    with left:

        subdriver_count = (
            filtered_df["Sub driver"]
            .value_counts()
            .reset_index()
        )

        subdriver_count.columns = [
            "Sub Driver",
            "Mentions"
        ]

        subdriver_fig = px.bar(
            subdriver_count,
            x="Sub Driver",
            y="Mentions",
            title="Sub-driver Distribution",
            text="Mentions"
        )

        subdriver_fig.update_layout(
            xaxis_tickangle=-30
        )

        st.plotly_chart(
            subdriver_fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Word Cloud
    # --------------------------------------------------------

    with right:

        st.subheader("☁️ Word Cloud")

        text = " ".join(
            filtered_df["combined_text"]
            .astype(str)
        )

        wordcloud = WordCloud(
            width=800,
            height=500,
            background_color="white"
        ).generate(text)

        fig, ax = plt.subplots(
            figsize=(8,5)
        )

        ax.imshow(
            wordcloud,
            interpolation="bilinear"
        )

        ax.axis("off")

        st.pyplot(fig)

    st.divider()

    # --------------------------------------------------------
    # Top Discussion Themes
    # --------------------------------------------------------

    st.subheader("🔥 Top Discussion Themes")

    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer(
        stop_words="english",
        max_features=15
    )

    X = vectorizer.fit_transform(
        filtered_df["combined_text"]
    )

    themes = vectorizer.get_feature_names_out()

    freq = X.sum(axis=0).A1

    theme_df = pd.DataFrame({

        "Theme": themes,

        "Frequency": freq

    })

    theme_df = theme_df.sort_values(
        "Frequency",
        ascending=False
    )

    theme_fig = px.bar(

        theme_df,

        x="Theme",

        y="Frequency",

        title="Top Discussion Themes",

        text="Frequency"

    )

    st.plotly_chart(

        theme_fig,

        use_container_width=True

    )

    st.divider()

    # --------------------------------------------------------
    # Recent Mentions
    # --------------------------------------------------------

    st.subheader("📰 Recent Digital Mentions")

    display_columns = [

        "Date",

        "Source Name",

        "Title",

        "Driver",

        "Sub driver",

        "Sentiment"

    ]

    available_columns = [
        c for c in display_columns
        if c in filtered_df.columns
    ]

    st.dataframe(

        filtered_df[available_columns],

        use_container_width=True,

        height=350

    )
    
    
    # ============================================================
# CONTENT EXPLORER TAB
# ============================================================

with explorer_tab:

    st.subheader("🔍 Content Explorer")

    st.markdown(
        "Browse and search digital mentions using filters."
    )

    st.divider()

    # --------------------------------------------------------
    # Search Statistics
    # --------------------------------------------------------

    left, right = st.columns([1,3])

    with left:

        st.metric(
            "Showing",
            len(filtered_df)
        )

    with right:

        csv = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Filtered Data",
            data=csv,
            file_name="filtered_mentions.csv",
            mime="text/csv"
        )

    st.divider()

    # --------------------------------------------------------
    # Article Table
    # --------------------------------------------------------

    display_columns = [

        "Date",
        "Source Name",
        "Title",
        "Driver",
        "Sub driver",
        "Sentiment"

    ]

    available_columns = [

        c for c in display_columns

        if c in filtered_df.columns

    ]

    st.dataframe(

        filtered_df[available_columns],

        width="stretch",

        height=350

    )

    st.divider()

    # --------------------------------------------------------
    # Select Article
    # --------------------------------------------------------

    if len(filtered_df) > 0:

        article_titles = (

            filtered_df["Title"]

            .fillna("Untitled Article")

            .tolist()

        )

        selected_title = st.selectbox(

            "Select an Article",

            article_titles

        )

        selected_row = (

            filtered_df

            [

                filtered_df["Title"]

                == selected_title

            ]

            .iloc[0]

        )

        st.divider()

        # ----------------------------------------------------
        # Article Details
        # ----------------------------------------------------

        st.subheader("📰 Article Details")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("### Metadata")

            st.write("**Date:**", selected_row.get("Date", "N/A"))

            st.write(
                "**Source:**",
                selected_row.get("Source Name", "N/A")
            )

            st.write(
                "**Sentiment:**",
                selected_row.get("Sentiment", "N/A")
            )

            st.write(
                "**Driver:**",
                selected_row.get("Driver", "N/A")
            )

            st.write(
                "**Sub Driver:**",
                selected_row.get("Sub driver", "N/A")
            )

            reach = selected_row.get("Reach", None)

            if pd.notna(reach):

                st.write("**Reach:**", reach)

        with c2:

            st.markdown("### Original Title")

            st.info(

                selected_row.get(

                    "Title",

                    "No Title"

                )

            )

            if pd.notna(

                selected_row.get("URL", None)

            ):

                st.markdown(

                    f"🔗 [Open Original Article]({selected_row['URL']})"

                )

        st.divider()

        # ----------------------------------------------------
        # Original Content
        # ----------------------------------------------------

        st.subheader("📄 Original Content")

        st.write(

            selected_row.get(

                "combined_text",

                "No content available."

            )

        )

    else:

        st.warning(

            "No records match the selected filters."

        )
        
        
        
        # ============================================================
# AI INSIGHTS TAB
# ============================================================

with insights_tab:

    st.subheader("🧠 AI Reputation Insights")

    st.markdown(
        "Automatically generated insights based on the classified digital mentions."
    )

    st.divider()

    # --------------------------------------------------------
    # Positive & Negative Driver Analysis
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ✅ Positive Reputation Drivers")

        positive_driver = (
            filtered_df[
                filtered_df["Sentiment"] == "Positive"
            ]["Driver"]
            .value_counts()
            .reset_index()
        )

        positive_driver.columns = [
            "Driver",
            "Mentions"
        ]

        if len(positive_driver):

            fig = px.bar(
                positive_driver,
                x="Driver",
                y="Mentions",
                text="Mentions",
                title="Positive Reputation Drivers"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info("No positive mentions found.")

    with col2:

        st.markdown("### ❌ Negative Reputation Drivers")

        negative_driver = (
            filtered_df[
                filtered_df["Sentiment"] == "Negative"
            ]["Driver"]
            .value_counts()
            .reset_index()
        )

        negative_driver.columns = [
            "Driver",
            "Mentions"
        ]

        if len(negative_driver):

            fig = px.bar(
                negative_driver,
                x="Driver",
                y="Mentions",
                text="Mentions",
                title="Negative Reputation Drivers"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info("No negative mentions found.")

    st.divider()

    # --------------------------------------------------------
    # Key Findings
    # --------------------------------------------------------

    st.subheader("📌 Key Findings")

    top_driver = (
        filtered_df["Driver"]
        .value_counts()
        .idxmax()
    )

    top_driver_count = (
        filtered_df["Driver"]
        .value_counts()
        .max()
    )

    top_subdriver = (
        filtered_df["Sub driver"]
        .value_counts()
        .idxmax()
    )

    st.success(
        f"""
• **Total Mentions:** {len(filtered_df)}

• **Dominant Reputation Driver:** {top_driver} ({top_driver_count} mentions)

• **Most Frequent Sub-driver:** {top_subdriver}

• **Positive Mentions:** {positive}

• **Neutral Mentions:** {neutral}

• **Negative Mentions:** {negative}
"""
    )

    st.divider()

    # --------------------------------------------------------
    # Executive Summary
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    st.subheader("💡 Recommendations")

    recommendations = [

        "Increase thought leadership articles from senior leadership.",

        "Promote positive customer success stories across digital channels.",

        "Strengthen digital engagement around new investment products.",

        "Improve communication around customer complaints and resolutions.",

        "Increase visibility of CSR and responsible business initiatives."

    ]

    for rec in recommendations:

        st.markdown(f"✅ {rec}")

    st.divider()

    # --------------------------------------------------------
    # Read Insights Report
    # --------------------------------------------------------

    st.subheader("📄 Generated Insights Report")

    try:

        with open(
            "output/reports/insights.txt",
            "r",
            encoding="utf-8"
        ) as f:

            report = f.read()

        st.text_area(
            "Insights Report",
            report,
            height=350
        )

    except FileNotFoundError:

        st.warning(
            "Run insights.py to generate the report."
        )

    st.divider()

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    st.markdown(
        """
        ---
        **AI & Data Solutions Specialist Assignment**

        Built using **Python • Pandas • Mistral AI • Plotly • Streamlit**
        """
    )