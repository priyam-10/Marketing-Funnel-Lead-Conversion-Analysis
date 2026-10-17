import pandas as pd
import plotly.graph_objects as go
import streamlit as st

REPO_URL = "https://github.com/priyam-10/Marketing-Funnel-Lead-Conversion-Analysis"
REPORT_URL = REPO_URL + "/blob/main/Marketing_Funnel_Lead_Conversion_Report.pdf"
DATA_URL = ("https://raw.githubusercontent.com/priyam-10/Marketing-Funnel-Lead-Conversion-Analysis/"
            "main/data/bank-full.csv")

# Theme: midnight slate page, slate cards, coral + sky + mint accents, light text
BG, CARD, LINE, INK, MUTED = "#0e1621", "#172333", "#26364a", "#f1f5f9", "#a9b6c6"
CORAL, SKY, MINT, GOLD = "#ff6b5b", "#4cc3ff", "#3ddc97", "#ffc857"

st.set_page_config(page_title="Marketing Funnel & Lead Conversion Dashboard", page_icon="🎯",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown(f"""
<style>
.stApp {{ background:{BG}; }}
.block-container {{ padding:1.2rem 2rem 2rem; max-width:1500px; }}
header[data-testid="stHeader"] {{ background:transparent; }}
section[data-testid="stSidebar"] {{ display:none; }}
.stApp, .stApp p, .stApp label, .stApp span, .stApp li {{ color:{INK}; }}

.hero {{ display:grid; grid-template-columns: 1fr auto; gap:16px; align-items:center;
         background:linear-gradient(120deg,{CARD} 0%, #1d2d42 100%); border:1px solid {LINE};
         border-left:6px solid {CORAL}; border-radius:16px; padding:22px 26px; margin-bottom:16px; }}
.hero h1 {{ color:{INK} !important; font-size:34px; font-weight:800; margin:0; padding:0; }}
.hero h1 b {{ color:{CORAL}; }}
.hero p {{ color:{MUTED} !important; margin:6px 0 0; font-size:15px; }}
.btns a {{ display:block; text-align:center; margin:6px 0; padding:10px 18px; border-radius:10px;
          font-weight:700; text-decoration:none; font-size:14px; }}
.btns a.rep {{ background:{CORAL}; color:#0e1621 !important; }}
.btns a.git {{ background:transparent; color:{SKY} !important; border:2px solid {SKY}; }}

.stat {{ background:{CARD}; border:1px solid {LINE}; border-radius:14px; padding:16px 18px; height:100%; }}
.stat .lb {{ color:{MUTED} !important; font-size:13px; font-weight:600; }}
.stat .vl {{ color:var(--c) !important; font-size:32px; font-weight:800; line-height:1.2; }}
.stat .sm {{ color:{MUTED} !important; font-size:12px; }}

.insight {{ background:{CARD}; border:1px solid {LINE}; border-radius:14px; padding:16px 20px; }}
.insight h4 {{ color:{GOLD} !important; margin:0 0 8px; }}
.insight li {{ color:{INK} !important; margin-bottom:6px; }}

/* Filter expander */
[data-testid="stExpander"] details {{ background:{CARD}; border:1px solid {LINE}; border-radius:12px; }}
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary * {{ color:{INK} !important; }}

/* Dropdowns: light boxes with dark text, never black-on-black */
[data-testid="stSelectbox"] [data-testid="stWidgetLabel"], [data-testid="stSelectbox"] [data-testid="stWidgetLabel"] * {{
  color:{SKY} !important; -webkit-text-fill-color:{SKY} !important; font-weight:700; background:transparent !important; }}
[data-testid="stSelectbox"] div:not([data-testid="stWidgetLabel"]):not([data-testid="stWidgetLabel"] *) {{
  background-color:#f1f5f9 !important; color:#0e1621 !important; }}
[data-testid="stSelectbox"] > div > div:last-child,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{ border:1px solid {LINE} !important; border-radius:8px !important; }}
[data-testid="stSelectbox"] div:not([data-testid="stWidgetLabel"] *), [data-testid="stSelectbox"] span:not([data-testid="stWidgetLabel"] *),
[data-testid="stSelectbox"] input {{
  color:#0e1621 !important; -webkit-text-fill-color:#0e1621 !important; opacity:1 !important; }}
[data-testid="stSelectbox"] svg {{ fill:#0e1621 !important; color:#0e1621 !important; }}
div[data-baseweb="popover"], div[data-baseweb="popover"] > div, div[data-baseweb="menu"],
ul[role="listbox"], [data-testid="stSelectboxVirtualDropdown"] {{ background-color:#f1f5f9 !important; }}
[role="option"], [role="option"] * {{ background-color:#f1f5f9 !important; color:#0e1621 !important; }}
[role="option"]:hover, [role="option"]:hover *, [role="option"][aria-selected="true"],
[role="option"][aria-selected="true"] * {{ background-color:#ffd9d4 !important; }}

/* Section switcher (radio as pills) */
div[role="radiogroup"] {{ gap:8px; flex-wrap:wrap; }}
div[role="radiogroup"] label {{ background:{CARD}; border:1px solid {LINE}; border-radius:999px; padding:6px 16px !important; }}
div[role="radiogroup"] label p {{ color:{INK} !important; font-weight:600; }}
div[role="radiogroup"] label:has(input:checked) {{ background:{SKY}; border-color:{SKY}; }}
div[role="radiogroup"] label:has(input:checked) p {{ color:#0e1621 !important; }}

div[data-testid="stPlotlyChart"] {{ background:{CARD}; border:1px solid {LINE}; border-radius:14px; padding:8px; }}
.foot {{ text-align:center; color:{MUTED} !important; margin-top:18px; }}
.foot a {{ color:{SKY} !important; font-weight:700; }}
</style>
""", unsafe_allow_html=True)

MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


@st.cache_data(ttl=3600, show_spinner="Loading campaign data...")
def load():
    df = pd.read_csv(DATA_URL, sep=";")
    df["Converted"] = (df["y"] == "yes").astype(int)
    df["Age Group"] = pd.cut(df["age"], [0, 25, 35, 45, 55, 65, 120],
                             labels=["18-25", "26-35", "36-45", "46-55", "56-65", "65+"])
    df["Balance Group"] = pd.cut(df["balance"], [-1e9, 0, 1000, 5000, 1e9],
                                 labels=["Negative/Zero", "Low (1-1K)", "Medium (1K-5K)", "High (5K+)"])
    df["Month"] = pd.Categorical(df["month"], MONTHS, ordered=True)
    return df


df = load()

# ---------- Hero ----------
st.markdown(f"""
<div class="hero">
  <div><h1>🎯 Marketing Funnel &amp; <b>Lead Conversion</b> Dashboard</h1>
  <p>Bank telemarketing campaign · who we reached, who engaged, and who subscribed to a term deposit</p></div>
  <div class="btns">
    <a class="rep" href="{REPORT_URL}" target="_blank">📄 Open Full Report</a>
    <a class="git" href="{REPO_URL}" target="_blank">GitHub Repository</a>
  </div>
</div>""", unsafe_allow_html=True)

# ---------- Filters (collapsible) ----------
d = df.copy()
with st.expander("🔎  Filter leads", expanded=False):
    cols = st.columns(6)
    for c, (col, label) in zip(cols, [("job", "Job"), ("marital", "Marital Status"), ("education", "Education"),
                                      ("contact", "Contact Method"), ("housing", "Housing Loan"), ("loan", "Personal Loan")]):
        choice = c.selectbox(label, ["All"] + sorted(df[col].unique().tolist()), key=col)
        if choice != "All":
            d = d[d[col] == choice]

if d.empty:
    st.warning("No leads match these filters.")
    st.stop()

total = len(d)
contacted = int((d["duration"] >= 60).sum())
engaged = int((d["duration"] >= 180).sum())
converted = int(d["Converted"].sum())
rate = converted / total * 100

# ---------- Funnel + stats ----------
left, right = st.columns([1.25, 1])
with left:
    fig = go.Figure(go.Funnel(
        y=["Total Leads", "Talked 1+ min", "Talked 3+ min", "Subscribed"],
        x=[total, contacted, engaged, converted], textinfo="value+percent initial",
        textfont=dict(color="#0e1621", size=15),
        marker=dict(color=[SKY, MINT, GOLD, CORAL]), connector=dict(fillcolor=LINE)))
    fig.update_layout(height=380, paper_bgcolor=CARD, plot_bgcolor=CARD, font=dict(color=INK, size=14),
                      margin=dict(l=130, r=20, t=55, b=10),
                      title=dict(text="<b>Lead Conversion Funnel</b>", x=0.02, font=dict(color=INK, size=18)))
    fig.update_yaxes(tickfont=dict(color=INK, size=14), automargin=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, theme=None)
with right:
    stats = [("Total Leads", f"{total:,}", SKY, "people in the campaign"),
             ("Subscribed", f"{converted:,}", CORAL, "said yes to a term deposit"),
             ("Conversion Rate", f"{rate:.2f}%", MINT, "subscribed ÷ total leads"),
             ("Avg Call Duration", f"{d['duration'].mean() / 60:.1f} min", GOLD, "per contact"),
             ("Avg Contacts / Lead", f"{d['campaign'].mean():.2f}", SKY, "calls this campaign"),
             ("Avg Age", f"{d['age'].mean():.1f}", MINT, "years")]
    for i in range(0, 6, 2):
        a, b = st.columns(2)
        for c, (lb, vl, col, sm) in zip((a, b), stats[i:i + 2]):
            c.markdown(f'<div class="stat" style="--c:{col}"><div class="lb">{lb}</div>'
                       f'<div class="vl">{vl}</div><div class="sm">{sm}</div></div>', unsafe_allow_html=True)
        st.write("")


# ---------- Chart helpers ----------
def conv(col):
    return (d.groupby(col, observed=True)["Converted"].mean() * 100).round(2)


def style(fig, title, h=380):
    fig.update_layout(height=h, paper_bgcolor=CARD, plot_bgcolor=CARD, showlegend=False,
                      title=dict(text=f"<b>{title}</b>", x=0.02, font=dict(color=INK, size=17)),
                      font=dict(color=INK, size=13), margin=dict(l=10, r=50, t=60, b=10))
    fig.update_xaxes(showgrid=False, zeroline=False, title=None, tickfont=dict(color=MUTED), automargin=True)
    fig.update_yaxes(gridcolor=LINE, zeroline=False, title=None, tickfont=dict(color=MUTED), automargin=True)
    return fig


def bars(s, title, color, horizontal=False, h=380):
    txt = [f"{v:.1f}%" for v in s.values]
    if horizontal:
        s = s.sort_values()
        txt = [f"{v:.1f}%" for v in s.values]
        fig = go.Figure(go.Bar(x=s.values, y=[str(i).title() for i in s.index], orientation="h",
                               marker_color=color, text=txt, textposition="outside",
                               textfont=dict(color=INK), cliponaxis=False))
        fig.update_xaxes(visible=False, range=[0, s.max() * 1.2])
    else:
        fig = go.Figure(go.Bar(x=[str(i).title() for i in s.index], y=s.values, marker_color=color, width=0.6,
                               text=txt, textposition="outside", textfont=dict(color=INK), cliponaxis=False))
        fig.update_yaxes(visible=False, range=[0, s.max() * 1.25])
    return style(fig, title, h)


cfg = {"displayModeBar": False}
show = lambda c, f: c.plotly_chart(f, use_container_width=True, config=cfg, theme=None)

st.write("")
section = st.radio("Section", ["👥 Who converts", "📞 Campaign & channel", "📅 Timing", "💡 Key insights"],
                   horizontal=True, label_visibility="collapsed")

if section == "👥 Who converts":
    c1, c2 = st.columns(2)
    show(c1, bars(conv("job"), "Conversion Rate by Job", SKY, horizontal=True, h=460))
    show(c2, bars(conv("Age Group"), "Conversion Rate by Age Group", CORAL, h=460))
    c1, c2, c3 = st.columns(3)
    show(c1, bars(conv("education"), "By Education Level", MINT))
    show(c2, bars(conv("marital"), "By Marital Status", GOLD))
    show(c3, bars(conv("Balance Group"), "By Account Balance", SKY))

elif section == "📞 Campaign & channel":
    c1, c2 = st.columns(2)
    show(c1, bars(conv("poutcome"), "Conversion by Previous Campaign Outcome", CORAL))
    ct = d.groupby(["contact", "y"]).size().unstack(fill_value=0)
    fig = go.Figure([go.Bar(x=ct.index.str.title(), y=ct.get("no", 0), name="Not subscribed", marker_color=SKY),
                     go.Bar(x=ct.index.str.title(), y=ct.get("yes", 0), name="Subscribed", marker_color=CORAL)])
    fig = style(fig, "Subscription Outcome by Contact Method")
    fig.update_layout(barmode="stack", showlegend=True,
                      legend=dict(orientation="h", y=1.1, x=1, xanchor="right", font=dict(color=INK)))
    show(c2, fig)
    camp = d.assign(Calls=d["campaign"].clip(upper=10).astype(str).replace("10", "10+"))
    order = [str(i) for i in range(1, 10)] + ["10+"]
    s = (camp.groupby("Calls")["Converted"].mean() * 100).reindex(order).dropna()
    fig = go.Figure(go.Scatter(x=s.index, y=s.values, mode="lines+markers+text", line=dict(color=MINT, width=3),
                               marker=dict(size=9), text=[f"{v:.1f}%" for v in s.values],
                               textposition="top center", textfont=dict(color=INK), fill="tozeroy",
                               fillcolor="rgba(61,220,151,0.15)"))
    fig.update_yaxes(visible=False, range=[0, s.max() * 1.3])
    fig.update_xaxes(title="Number of calls in this campaign", title_font=dict(color=MUTED))
    show(st, style(fig, "Conversion Rate vs Number of Calls"))

elif section == "📅 Timing":
    m = d.groupby("Month", observed=True).agg(Leads=("Converted", "size"), Rate=("Converted", "mean"))
    fig = go.Figure()
    fig.add_trace(go.Bar(x=m.index.str.title(), y=m["Leads"], name="Leads contacted", marker_color=LINE,
                         marker_line_color=SKY, marker_line_width=1.5, yaxis="y"))
    fig.add_trace(go.Scatter(x=m.index.str.title(), y=m["Rate"] * 100, name="Conversion rate %", mode="lines+markers+text",
                             line=dict(color=CORAL, width=3), marker=dict(size=9),
                             text=[f"{v * 100:.1f}%" for v in m["Rate"]], textposition="top center",
                             textfont=dict(color=INK), yaxis="y2"))
    fig = style(fig, "Leads vs Conversion Rate by Month", 440)
    fig.update_layout(showlegend=True, legend=dict(orientation="h", y=1.1, x=1, xanchor="right", font=dict(color=INK)),
                      yaxis2=dict(overlaying="y", side="right", showgrid=False, visible=False,
                                  range=[0, m["Rate"].max() * 130]))
    show(st, fig)
    c1, c2 = st.columns(2)
    dur = d.assign(Call=pd.cut(d["duration"], [-1, 120, 300, 600, 1e9],
                               labels=["< 2 min", "2-5 min", "5-10 min", "10+ min"]))
    show(c1, bars((dur.groupby("Call", observed=True)["Converted"].mean() * 100), "Conversion by Call Length", GOLD))
    pie = d["y"].value_counts().reindex(["no", "yes"]).fillna(0)
    fig = go.Figure(go.Pie(labels=["Not subscribed", "Subscribed"], values=pie.values, hole=0.62,
                           marker=dict(colors=[SKY, CORAL]), textinfo="percent",
                           textfont=dict(color="#0e1621", size=14), sort=False))
    fig.add_annotation(text=f"<b>{rate:.1f}%</b><br>converted", showarrow=False, font=dict(color=INK, size=18))
    fig = style(fig, "Customer Subscription Distribution")
    fig.update_layout(showlegend=True, legend=dict(font=dict(color=INK)))
    show(c2, fig)

else:
    best_job = conv("job").idxmax()
    best_age = conv("Age Group").idxmax()
    best_month = conv("Month").idxmax()
    po = conv("poutcome")
    st.markdown(f"""
<div class="insight"><h4>What the data says (updates with your filters)</h4><ul>
<li>Overall, <b>{rate:.2f}%</b> of {total:,} leads subscribed.</li>
<li>Best job group: <b>{str(best_job).title()}</b> ({conv('job').max():.1f}% conversion).</li>
<li>Best age group: <b>{best_age}</b> ({conv('Age Group').max():.1f}%).</li>
<li>Best month: <b>{str(best_month).title()}</b> ({conv('Month').max():.1f}%).</li>
<li>Leads whose previous campaign was a <b>success</b> convert at <b>{po.get('success', 0):.1f}%</b> vs
    <b>{po.get('unknown', 0):.1f}%</b> for new leads.</li>
<li>Longer calls convert far better — engagement is the strongest signal of a sale.</li>
</ul><p>Read the full analysis and recommendations in the
<a href="{REPORT_URL}" target="_blank" style="color:{CORAL};font-weight:700">project report (PDF)</a>.</p></div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="foot">Data: Bank Marketing (UCI) · <a href="{REPORT_URL}" target="_blank">Full report (PDF)</a>'
            f' · <a href="{REPO_URL}" target="_blank">GitHub repository</a></div>', unsafe_allow_html=True)
