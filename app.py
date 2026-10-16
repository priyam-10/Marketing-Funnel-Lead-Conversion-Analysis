
from pathlib import Path
from io import BytesIO
import base64

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="MarketPulse | Lead Conversion Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "bank-full.csv"
REPORT_FILE = ROOT / "Marketing_Funnel_Lead_Conversion_Report.pdf"
IMAGES_DIR = ROOT / "images"

GITHUB_URL = (
    "https://github.com/priyam-10/"
    "Marketing-Funnel-Lead-Conversion-Analysis"
)
REPORT_URL = (
    GITHUB_URL + "/blob/main/Marketing_Funnel_Lead_Conversion_Report.pdf"
)

NAVY = "#172B4D"
BLUE = "#3563E9"
TEAL = "#078C83"
GREEN = "#16845B"
AMBER = "#B86B08"
RED = "#C2414B"
MUTED = "#62718A"
BORDER = "#E0E7F0"
PALETTE = [BLUE, TEAL, "#8065D8", AMBER, GREEN, "#D85B73"]

# =========================================================
# VISUAL DESIGN
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --page: #F3F6FB;
    --ink: #172B4D;
    --muted: #62718A;
    --panel: #FFFFFF;
    --line: #E0E7F0;
    --blue: #3563E9;
}
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: var(--page);
    color: var(--ink);
}
[data-testid="stHeader"] {
    background: rgba(243,246,251,.95);
}
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] * {
    color: var(--ink);
}
.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4, p, label {
    color: var(--ink);
}
.hero {
    background: linear-gradient(115deg, #142644 0%, #23468A 60%, #087F83 100%);
    border-radius: 22px;
    padding: 32px 34px;
    margin-bottom: 24px;
    box-shadow: 0 12px 30px rgba(24,49,90,.13);
}
.hero .eyebrow {
    color: #B9E9EA;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 12px;
}
.hero h1 {
    color: #FFFFFF;
    font-size: clamp(28px, 3vw, 42px);
    font-weight: 800;
    line-height: 1.15;
    margin: 0;
}
.hero p {
    color: #E2ECFC;
    font-size: 14px;
    line-height: 1.8;
    max-width: 850px;
    margin: 12px 0 0 0;
}
.section-title {
    color: var(--ink);
    font-size: 21px;
    font-weight: 800;
    margin: 24px 0 5px;
}
.section-desc {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 15px;
}
.metric-card {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 19px;
    min-height: 134px;
    box-shadow: 0 5px 18px rgba(28,48,82,.035);
}
.metric-label {
    color: #62718A;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .65px;
}
.metric-value {
    color: #172B4D;
    font-size: clamp(25px, 2.2vw, 34px);
    font-weight: 800;
    margin-top: 12px;
    line-height: 1.2;
}
.metric-note {
    color: #087F83;
    font-size: 12px;
    font-weight: 600;
    margin-top: 7px;
}
.insight-card {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-left: 4px solid #3563E9;
    border-radius: 12px;
    padding: 17px 18px;
    margin: 0 0 12px;
}
.insight-card h4 {
    font-size: 14px;
    font-weight: 800;
    color: #172B4D;
    margin: 0 0 7px;
}
.insight-card p {
    font-size: 13px;
    line-height: 1.7;
    color: #52627A;
    margin: 0;
}
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 8px;
    box-shadow: 0 4px 16px rgba(28,48,82,.025);
}
div[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}
.stButton button, .stDownloadButton button,
.stLinkButton a {
    border-radius: 10px;
    font-weight: 700;
}
.stButton button[kind="primary"] {
    background: #3563E9;
    border-color: #3563E9;
}
a { color: #2457D6 !important; font-weight: 600; }
hr { border-color: var(--line); }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA & REPORT
# =========================================================
@st.cache_data(show_spinner=False)
def load_dataset(path, modified_time):
    # Bank Marketing CSV uses semicolons.
    return pd.read_csv(path, sep=";", low_memory=False)


@st.cache_data(show_spinner=False)
def load_report_bytes(path, modified_time):
    return Path(path).read_bytes()


@st.cache_data(show_spinner=False)
def load_image_bytes(path, modified_time):
    return Path(path).read_bytes()


if not DATA_FILE.exists():
    st.error(
        "Your original dataset was not found at "
        "`data/bank-full.csv`. Keep the existing data folder "
        "beside app.py and try again."
    )
    st.link_button("Open your GitHub project", GITHUB_URL)
    st.stop()

df = load_dataset(str(DATA_FILE), DATA_FILE.stat().st_mtime)

df.columns = (
    df.columns.astype(str).str.strip().str.lower()
)

if "y" not in df.columns:
    st.error(
        "Expected the original target column 'y'. "
        f"Columns found: {', '.join(df.columns)}"
    )
    st.stop()

df["converted"] = (
    df["y"].astype(str).str.strip().str.lower()
    .isin(["yes", "1", "true"])
)

for column in [
    "age", "balance", "campaign", "previous",
    "duration", "day", "pdays"
]:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

if "age" in df.columns:
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 25, 35, 45, 55, 120],
        labels=["18–25", "26–35", "36–45", "46–55", "56+"],
        include_lowest=True,
    )

# =========================================================
# REUSABLE HELPERS
# =========================================================
def section(title, description=""):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )
    if description:
        st.markdown(
            f'<div class="section-desc">{description}</div>',
            unsafe_allow_html=True,
        )


def metric(label, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(title, text):
    st.markdown(
        f"""
        <div class="insight-card">
            <h4>{title}</h4>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def conversion_table(data, column):
    result = (
        data.groupby(column, dropna=False, observed=True)
        .agg(
            Customers=("converted", "size"),
            Subscriptions=("converted", "sum"),
        )
        .reset_index()
    )
    result["Conversion Rate (%)"] = (
        100 * result["Subscriptions"]
        / result["Customers"].replace(0, float("nan"))
    )
    return result


def style_chart(fig, height=370):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=22, r=22, t=68, b=28),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter", size=12, color="#34445B"),
        title=dict(
            font=dict(size=16, color=NAVY),
            x=0.02,
            xanchor="left",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#52627A"),
        ),
        hoverlabel=dict(
            bgcolor=NAVY,
            font_color="#FFFFFF",
            font_family="Inter",
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=BORDER,
        tickfont=dict(color=MUTED),
        title_font=dict(color=NAVY),
    )
    fig.update_yaxes(
        gridcolor="#E9EEF5",
        zeroline=False,
        tickfont=dict(color=MUTED),
        title_font=dict(color=NAVY),
    )
    return fig


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 📈 MarketPulse")
    st.caption("LEAD CONVERSION INTELLIGENCE")
    st.divider()

    st.markdown("### Your project")
    st.link_button(
        "↗ Open GitHub repository",
        GITHUB_URL,
        use_container_width=True,
    )

    st.markdown("### Data source")
    st.success("Original dataset connected")
    st.caption("data/bank-full.csv")
    st.caption(f"{len(df):,} source records")

    st.divider()
    st.caption("Python · Pandas · Plotly · Streamlit")
    st.caption("Interactive portfolio dashboard")

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <div class="eyebrow">EXECUTIVE ANALYTICS · BANK MARKETING</div>
    <h1>Marketing Funnel &amp;<br>Lead Conversion Intelligence</h1>
    <p>
        Discover what drives customer subscriptions, compare contact
        methods, evaluate campaign timing, and explore customer segments
        using the original dataset from your GitHub project.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FILTERS
# =========================================================
section(
    "Explore the data",
    "Choose segments to update all metrics, visualizations, and insights.",
)

filter_fields = [
    ("job", "Job category"),
    ("marital", "Marital status"),
    ("education", "Education"),
    ("contact", "Contact method"),
    ("month", "Campaign month"),
    ("poutcome", "Previous outcome"),
    ("housing", "Housing loan"),
    ("loan", "Personal loan"),
]

with st.container(border=True):
    cols = st.columns(4)
    selected_filters = {}

    for i, (column, label) in enumerate(filter_fields):
        if column not in df.columns:
            continue
        options = sorted(df[column].dropna().astype(str).unique())
        with cols[i % 4]:
            selected_filters[column] = st.multiselect(
                label,
                options,
                default=options,
                key=f"select_{column}",
            )

    if "age" in df.columns and df["age"].notna().any():
        min_age = int(df["age"].min())
        max_age = int(df["age"].max())
        if min_age < max_age:
            age_range = st.slider(
                "Age range",
                min_value=min_age,
                max_value=max_age,
                value=(min_age, max_age),
            )
        else:
            age_range = (min_age, max_age)
    else:
        age_range = None

    reset_col, reset_note = st.columns([1, 3])
    with reset_col:
        if st.button("Reset filters", use_container_width=True):
            for column, _ in filter_fields:
                st.session_state.pop(f"select_{column}", None)
            st.rerun()
    with reset_note:
        st.caption("Tip: select one category to investigate a specific segment.")

filtered = df.copy()

for column, selected in selected_filters.items():
    filtered = filtered[
        filtered[column].astype(str).isin(selected)
    ]

if age_range and "age" in filtered.columns:
    filtered = filtered[
        filtered["age"].between(age_range[0], age_range[1])
    ]

# =========================================================
# KPI CARDS
# =========================================================
total = len(filtered)
subscriptions = int(filtered["converted"].sum())
non_converted = total - subscriptions
conversion_rate = subscriptions / total * 100 if total else 0

source_total = len(df)
source_conversions = int(df["converted"].sum())
source_rate = source_conversions / source_total * 100 if source_total else 0

section("Executive snapshot", "A live summary of the currently selected audience.")

k1, k2, k3, k4 = st.columns(4)
with k1:
    metric("CUSTOMERS ANALYZED", f"{total:,}", "Records in current selection")
with k2:
    metric("SUBSCRIPTIONS", f"{subscriptions:,}", "Target outcome = yes")
with k3:
    metric("CONVERSION RATE", f"{conversion_rate:.2f}%", "Subscriptions / customers")
with k4:
    metric("NOT SUBSCRIBED", f"{non_converted:,}", "Potential re-engagement audience")

st.caption(
    f"Full-dataset benchmark: {source_total:,} customers · "
    f"{source_conversions:,} subscriptions · {source_rate:.2f}% conversion."
)

st.divider()

# =========================================================
# DASHBOARD NAVIGATION
# =========================================================
overview_tab, campaign_tab, customer_tab, explorer_tab, report_tab = st.tabs([
    "✦ Executive Overview",
    "↗ Campaign Performance",
    "◎ Customer Intelligence",
    "▤ Data Explorer",
    "▣ Original Report",
])

# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================
with overview_tab:
    section(
        "Conversion performance",
        "Understand the outcome distribution and which channels perform best.",
    )

    left, right = st.columns(2)

    with left:
        pie = go.Figure(go.Pie(
            labels=["Subscribed", "Not subscribed"],
            values=[subscriptions, non_converted],
            hole=0.70,
            sort=False,
            marker=dict(
                colors=[TEAL, "#DCE4F0"],
                line=dict(color="#FFFFFF", width=4),
            ),
            textinfo="percent+label",
            textfont=dict(color=NAVY, size=12),
            hovertemplate="%{label}<br>Customers: %{value:,}<br>%{percent}<extra></extra>",
        ))
        pie.add_annotation(
            text=f"<b>{conversion_rate:.1f}%</b><br><sup>Conversion</sup>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=21, color=NAVY),
        )
        pie.update_layout(title="Subscription outcome mix", showlegend=False)
        st.plotly_chart(
            style_chart(pie, 365),
            use_container_width=True,
        )

    with right:
        if total and "contact" in filtered.columns:
            channels = conversion_table(filtered, "contact")
            channels = channels.sort_values("Conversion Rate (%)")
            fig = px.bar(
                channels,
                x="Conversion Rate (%)",
                y="contact",
                orientation="h",
                text=channels["Conversion Rate (%)"].map(lambda x: f"{x:.2f}%"),
                color="Conversion Rate (%)",
                color_continuous_scale=["#B8C9F5", BLUE, TEAL],
                hover_data=["Customers", "Subscriptions"],
                title="Conversion rate by contact method",
            )
            fig.update_traces(
                textposition="outside",
                cliponaxis=False,
                marker_line_width=0,
            )
            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Conversion rate (%)",
                yaxis_title="",
            )
            st.plotly_chart(
                style_chart(fig, 365),
                use_container_width=True,
            )

    section(
        "Monthly campaign trends",
        "Compare customer volume and subscription rates across the calendar.",
    )

    if total and "month" in filtered.columns:
        month_order = [
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec",
        ]
        monthly = conversion_table(filtered, "month")
        monthly["_order"] = monthly["month"].astype(str).str.lower().map(
            {m: i for i, m in enumerate(month_order)}
        )
        monthly = monthly.sort_values("_order")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly["month"],
            y=monthly["Customers"],
            name="Customers",
            marker_color="#DCE6FA",
            hovertemplate="%{x}<br>Customers: %{y:,}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=monthly["month"],
            y=monthly["Conversion Rate (%)"],
            name="Conversion rate",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color=TEAL, width=3),
            marker=dict(size=8, color=TEAL),
            hovertemplate="%{x}<br>Conversion: %{y:.2f}%<extra></extra>",
        ))
        fig.update_layout(
            title="Customer volume and conversion by month",
            xaxis_title="Campaign month",
            yaxis=dict(title="Customers", gridcolor="#E9EEF5"),
            yaxis2=dict(
                title="Conversion rate (%)",
                overlaying="y",
                side="right",
                showgrid=False,
            ),
        )
        st.plotly_chart(
            style_chart(fig, 405),
            use_container_width=True,
        )

    section("Executive insights", "Generated from the current filtered dataset.")

    if total == 0:
        st.warning("No customers match these filters. Reset or widen your selection.")
    else:
        insight(
            "01 · Conversion benchmark",
            f"{subscriptions:,} out of {total:,} selected customers subscribed, "
            f"resulting in a {conversion_rate:.2f}% conversion rate. "
            f"The full dataset baseline is {source_rate:.2f}%.",
        )

        if "contact" in filtered.columns:
            channel_summary = conversion_table(filtered, "contact")
            channel_summary = channel_summary[
                channel_summary["Customers"] > 0
            ].sort_values("Conversion Rate (%)", ascending=False)

            if not channel_summary.empty:
                best = channel_summary.iloc[0]
                insight(
                    "02 · Highest observed contact conversion",
                    f"{best['contact']} has the highest observed conversion rate "
                    f"at {best['Conversion Rate (%)']:.2f}% across "
                    f"{int(best['Customers']):,} customers in this selection. "
                    "Check volume, costs, and uncertainty before changing budgets.",
                )

        if "month" in filtered.columns:
            month_summary = conversion_table(filtered, "month")
            month_summary = month_summary[
                month_summary["Customers"] > 0
            ].sort_values("Conversion Rate (%)", ascending=False)

            if not month_summary.empty:
                best_month = month_summary.iloc[0]
                insight(
                    "03 · Strongest observed month",
                    f"{best_month['month']} has the highest observed conversion "
                    f"rate at {best_month['Conversion Rate (%)']:.2f}%. "
                    "This is an association in the historical data, not proof "
                    "that timing alone caused the result.",
                )

# =========================================================
# CAMPAIGN PERFORMANCE
# =========================================================
with campaign_tab:
    section(
        "Campaign effectiveness",
        "Review contact frequency and previous campaign outcomes.",
    )

    left, right = st.columns(2)

    with left:
        if total and "campaign" in filtered.columns:
            work = filtered.dropna(subset=["campaign"]).copy()
            work["Contact frequency"] = (
                work["campaign"].clip(upper=10).astype(int)
            )
            frequency = conversion_table(work, "Contact frequency")
            frequency = frequency.sort_values("Contact frequency")

            fig = px.bar(
                frequency,
                x="Contact frequency",
                y="Conversion Rate (%)",
                color="Conversion Rate (%)",
                color_continuous_scale=["#C9D7FA", BLUE, TEAL],
                hover_data=["Customers", "Subscriptions"],
                title="Conversion by number of campaign contacts",
            )
            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Contacts (10 represents 10+)",
            )
            st.plotly_chart(
                style_chart(fig, 380),
                use_container_width=True,
            )

    with right:
        if total and "poutcome" in filtered.columns:
            previous = conversion_table(filtered, "poutcome")
            previous = previous.sort_values("Conversion Rate (%)")

            fig = px.bar(
                previous,
                x="Conversion Rate (%)",
                y="poutcome",
                orientation="h",
                color="Conversion Rate (%)",
                color_continuous_scale=["#C9D7FA", BLUE, TEAL],
                hover_data=["Customers", "Subscriptions"],
                title="Conversion by previous campaign outcome",
            )
            fig.update_layout(
                coloraxis_showscale=False,
                yaxis_title="Previous outcome",
            )
            st.plotly_chart(
                style_chart(fig, 380),
                use_container_width=True,
            )

    if total and "duration" in filtered.columns:
        section(
            "Call duration analysis",
            "Duration is known after a call. It should not be used as if it were a pre-call targeting signal.",
        )
        calls = filtered.dropna(subset=["duration"]).copy()
        calls["Call duration"] = pd.cut(
            calls["duration"],
            bins=[-1, 60, 180, 300, 600, float("inf")],
            labels=["0–60 sec", "61–180 sec", "181–300 sec", "301–600 sec", "600+ sec"],
        )
        duration_summary = conversion_table(calls, "Call duration")

        fig = px.bar(
            duration_summary,
            x="Call duration",
            y="Conversion Rate (%)",
            color="Conversion Rate (%)",
            color_continuous_scale=["#C9D7FA", BLUE, TEAL],
            hover_data=["Customers", "Subscriptions"],
            title="Observed conversion by call-duration band",
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(
            style_chart(fig, 365),
            use_container_width=True,
        )

    if total and "contact" in filtered.columns:
        section("Contact-method scorecard")
        scorecard = conversion_table(filtered, "contact")
        scorecard["Conversion Rate (%)"] = scorecard["Conversion Rate (%)"].round(2)
        scorecard["Customer share (%)"] = (
            scorecard["Customers"] / total * 100
        ).round(2)
        st.dataframe(
            scorecard.sort_values("Conversion Rate (%)", ascending=False),
            use_container_width=True,
            hide_index=True,
        )

# =========================================================
# CUSTOMER INTELLIGENCE
# =========================================================
with customer_tab:
    section(
        "Customer segment intelligence",
        "Find audience groups with stronger or weaker observed subscription rates.",
    )

    segment_options = [
        ("job", "Job category"),
        ("education", "Education level"),
        ("marital", "Marital status"),
        ("age_group", "Age group"),
    ]
    segment_options = [
        item for item in segment_options if item[0] in filtered.columns
    ]

    if total and segment_options:
        segment_key = st.selectbox(
            "Choose a segment",
            [x[0] for x in segment_options],
            format_func=lambda x: dict(segment_options)[x],
        )

        segments = conversion_table(filtered, segment_key)
        segments = segments.sort_values("Conversion Rate (%)")

        fig = px.bar(
            segments,
            x="Conversion Rate (%)",
            y=segment_key,
            orientation="h",
            color="Conversion Rate (%)",
            color_continuous_scale=["#C9D7FA", BLUE, TEAL],
            text=segments["Conversion Rate (%)"].map(lambda x: f"{x:.2f}%"),
            hover_data=["Customers", "Subscriptions"],
            title=f"Conversion by {dict(segment_options)[segment_key].lower()}",
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(
            style_chart(fig, max(380, len(segments) * 34)),
            use_container_width=True,
        )

        st.dataframe(
            segments.sort_values("Conversion Rate (%)", ascending=False).round(2),
            use_container_width=True,
            hide_index=True,
        )

    left, right = st.columns(2)

    with left:
        if total and "balance" in filtered.columns:
            balance = filtered.dropna(subset=["balance"]).copy()
            balance["Balance band"] = pd.cut(
                balance["balance"],
                bins=[-float("inf"), 0, 1000, 5000, 20000, float("inf")],
                labels=["Negative", "0–1,000", "1,000–5,000", "5,000–20,000", "20,000+"],
            )
            balance_summary = conversion_table(balance, "Balance band")

            fig = px.bar(
                balance_summary,
                x="Balance band",
                y="Conversion Rate (%)",
                color="Conversion Rate (%)",
                color_continuous_scale=["#C9D7FA", BLUE, TEAL],
                hover_data=["Customers", "Subscriptions"],
                title="Conversion by account-balance band",
            )
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(
                style_chart(fig, 365),
                use_container_width=True,
            )

    with right:
        if total and "education" in filtered.columns:
            education = conversion_table(filtered, "education")
            fig = px.scatter(
                education,
                x="Customers",
                y="Conversion Rate (%)",
                size="Subscriptions",
                color="education",
                hover_data=["Subscriptions"],
                title="Education: audience size vs conversion",
                color_discrete_sequence=PALETTE,
            )
            st.plotly_chart(
                style_chart(fig, 365),
                use_container_width=True,
            )

    section(
        "Original analysis charts",
        "Browse the PNG visualizations saved in your own repository.",
    )

    image_names = [
        ("overall_conversion.png", "Overall conversion"),
        ("contact_method.png", "Contact method"),
        ("monthly_conversion.png", "Monthly conversion"),
        ("job_conversion.png", "Job category"),
        ("education_conversion.png", "Education level"),
        ("marital_conversion.png", "Marital status"),
        ("age_conversion.png", "Age group"),
        ("balance_conversion.png", "Account balance"),
        ("previous_campaign.png", "Previous campaign"),
    ]

    available_images = [
        (filename, label)
        for filename, label in image_names
        if (IMAGES_DIR / filename).exists()
    ]

    if available_images:
        chosen_image = st.selectbox(
            "Choose a saved visualization",
            [x[0] for x in available_images],
            format_func=lambda x: dict(available_images)[x],
        )
        image_path = IMAGES_DIR / chosen_image
        st.image(
            str(image_path),
            caption=dict(available_images)[chosen_image],
            use_container_width=True,
        )
    else:
        st.info(
            "No saved images found. Keep the original images/ folder "
            "beside app.py to show the project's charts."
        )

# =========================================================
# DATA EXPLORER
# =========================================================
with explorer_tab:
    section(
        "Data explorer",
        "Search the original records and export the selected data.",
    )

    query = st.text_input(
        "Search text columns",
        placeholder="Search job, education, contact, month...",
    )

    display_df = filtered.drop(columns=["converted"], errors="ignore").copy()

    if query.strip():
        text_columns = display_df.select_dtypes(
            include=["object", "string", "category"]
        ).columns.tolist()

        if text_columns:
            mask = display_df[text_columns].astype(str).apply(
                lambda column: column.str.contains(
                    query, case=False, na=False, regex=False
                )
            ).any(axis=1)
            display_df = display_df[mask]

    st.caption(
        f"Showing {len(display_df):,} rows from {len(filtered):,} filtered records."
    )
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=440,
    )

    st.download_button(
        "⬇ Download filtered CSV",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="marketing_funnel_filtered.csv",
        mime="text/csv",
        use_container_width=True,
    )

    section("Dataset quality")
    quality = pd.DataFrame({
        "Check": [
            "Original records",
            "Original columns",
            "Missing cells",
            "Duplicate rows",
        ],
        "Value": [
            f"{len(df):,}",
            f"{len(df.columns) - 1:,}",
            f"{int(df.drop(columns=['converted']).isna().sum().sum()):,}",
            f"{int(df.duplicated(subset=[c for c in df.columns if c != 'converted']).sum()):,}",
        ],
    })
    st.dataframe(quality, use_container_width=True, hide_index=True)

# =========================================================
# ORIGINAL PDF REPORT
# =========================================================
with report_tab:
    section(
        "Project report & documentation",
        "Read or download the original report included in your GitHub project.",
    )

    if REPORT_FILE.exists():
        report_bytes = load_report_bytes(
            str(REPORT_FILE), REPORT_FILE.stat().st_mtime
        )

        st.success("Original project PDF found.")

        st.download_button(
            "⬇ Download original PDF report",
            data=report_bytes,
            file_name=REPORT_FILE.name,
            mime="application/pdf",
            use_container_width=True,
        )

        pdf_base64 = base64.b64encode(report_bytes).decode("utf-8")
        st.markdown(
            f"""
            <iframe
                src="data:application/pdf;base64,{pdf_base64}"
                width="100%"
                height="800"
                style="border:1px solid #E0E7F0;border-radius:14px;"
                title="Original project report">
            </iframe>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning(
            "The report PDF was not found locally. "
            "Open the original repository to access the report."
        )
        st.link_button("Open report in GitHub", REPORT_URL)

    section("Project summary")
    insight(
        "Project objective",
        "Analyze bank marketing campaign conversion, contact effectiveness, "
        "campaign timing, customer demographics, and previous campaign outcomes.",
    )
    insight(
        "Recommended actions",
        "Compare contact methods, investigate the strongest historical months, "
        "test relevant customer segments, and use previous campaign outcomes "
        "to inform re-engagement experiments.",
    )
    insight(
        "Interpretation note",
        "The conversion event is a term-deposit subscription. The dataset does "
        "not represent a website funnel with page views, cart events, and checkout steps.",
    )

# =========================================================
# FOOTER
# =========================================================
st.divider()
footer_left, footer_right = st.columns([3, 1])

with footer_left:
    st.caption("MARKETPULSE · Marketing Funnel & Lead Conversion Analysis")
    st.caption(
        "All KPIs and chart summaries are calculated from your original dataset. "
        "Observed associations do not establish causation."
    )

with footer_right:
    st.markdown(f"[↗ View source code on GitHub]({GITHUB_URL})")
