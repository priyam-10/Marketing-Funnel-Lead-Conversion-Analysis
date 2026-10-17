import pandas as pd
import plotly.graph_objects as go
import streamlit as st

REPO_URL = "https://github.com/priyam-10/Marketing-Funnel-Lead-Conversion-Analysis"
REPORT_URL = REPO_URL + "/blob/main/Marketing_Funnel_Lead_Conversion_Report.pdf"
DATA_URL = ("https://raw.githubusercontent.com/priyam-10/Marketing-Funnel-Lead-Conversion-Analysis/"
            "main/data/bank-full.csv")

# Theme: modern bento — soft mesh background, white glass cards, ink-black type,
# electric lime + tangerine + ocean accents
BG, CARD, LINE, INK, MUTED = "#f3f5f9", "#ffffff", "#e5e8f0", "#0b1220", "#5b6476"
CORAL, SKY, MINT, GOLD = "#ff7a45", "#2f6bff", "#14b8a6", "#b8e62e"

st.set_page_config(page_title="Marketing Funnel & Lead Conversion Dashboard", page_icon="🎯",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
html, body, .stApp, .stApp *:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) {{ font-family:'Plus Jakarta Sans', sans-serif; }}
[data-testid="stIconMaterial"] {{ font-family:'Material Symbols Rounded' !important; }}
.stApp {{ background:
   radial-gradient(900px 500px at 0% 0%, rgba(47,107,255,.14), transparent 60%),
   radial-gradient(800px 500px at 100% 10%, rgba(255,122,69,.14), transparent 60%),
   radial-gradient(900px 600px at 50% 100%, rgba(184,230,46,.18), transparent 60%), {BG}; }}
.block-container {{ padding:1.4rem 2rem 2rem; max-width:1500px; }}
header[data-testid="stHeader"] {{ background:transparent; }}
section[data-testid="stSidebar"] {{ display:none; }}
.stApp p, .stApp label, .stApp span, .stApp li {{ color:{INK}; }}

.hero {{ display:grid; grid-template-columns:1fr auto; gap:18px; align-items:center;
         background:{INK}; border-radius:28px; padding:30px 34px; margin-bottom:18px;
         box-shadow:0 20px 50px -20px rgba(11,18,32,.45); }}
.hero .ttl {{ color:#ffffff !important; font-size:38px; font-weight:800; margin:0; padding:0; letter-spacing:-1px; }}
.hero .ttl b {{ background:{GOLD}; color:{INK}; padding:0 10px; border-radius:10px; }}
.hero p {{ color:#c9d1e0 !important; margin:10px 0 0; font-size:15px; }}
.btns a {{ display:block; text-align:center; margin:7px 0; padding:12px 22px; border-radius:999px;
          font-weight:700; text-decoration:none; font-size:14px; }}
.btns a.rep {{ background:{GOLD}; color:{INK} !important; }}
.btns a.git {{ background:rgba(255,255,255,.08); color:#ffffff !important; border:1px solid rgba(255,255,255,.35); }}

.stat {{ background:rgba(255,255,255,.85); backdrop-filter:blur(10px); border:1px solid {LINE};
        border-radius:22px; padding:18px 20px; height:100%; box-shadow:0 8px 24px -12px rgba(11,18,32,.18); }}
.stat .lb {{ color:{MUTED} !important; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1px; }}
.stat .vl {{ color:{INK} !important; font-size:34px; font-weight:800; line-height:1.2; letter-spacing:-1px; }}
.stat .sm {{ color:{MUTED} !important; font-size:12px; }}
.stat::before {{ content:""; display:block; width:34px; height:6px; border-radius:6px; background:var(--c); margin-bottom:10px; }}

.insight {{ background:{CARD}; border:1px solid {LINE}; border-radius:22px; padding:22px 26px; }}
.insight h4 {{ color:{INK} !important; margin:0 0 10px; }}
.insight li {{ color:{INK} !important; margin-bottom:8px; }}

[data-testid="stExpander"] details {{ background:rgba(255,255,255,.85); border:1px solid {LINE}; border-radius:18px; }}
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary * {{ color:{INK} !important; font-weight:700; }}

/* Dropdowns: white boxes, dark text */
[data-testid="stSelectbox"] [data-testid="stWidgetLabel"], [data-testid="stSelectbox"] [data-testid="stWidgetLabel"] * {{
  color:{MUTED} !important; -webkit-text-fill-color:{MUTED} !important; font-weight:700; background:transparent !important; }}
[data-testid="stSelectbox"] div:not([data-testid="stWidgetLabel"]):not([data-testid="stWidgetLabel"] *) {{
  background-color:#ffffff !important; color:{INK} !important; }}
[data-testid="stSelectbox"] > div > div:last-child,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{ border:1px solid {LINE} !important; border-radius:12px !important; }}
[data-testid="stSelectbox"] div:not([data-testid="stWidgetLabel"] *), [data-testid="stSelectbox"] span:not([data-testid="stWidgetLabel"] *),
[data-testid="stSelectbox"] input {{ color:{INK} !important; -webkit-text-fill-color:{INK} !important; opacity:1 !important; }}
[data-testid="stSelectbox"] svg {{ fill:{INK} !important; color:{INK} !important; }}
div[data-baseweb="popover"], div[data-baseweb="popover"] > div, div[data-baseweb="menu"],
ul[role="listbox"], [data-testid="stSelectboxVirtualDropdown"] {{ background-color:#ffffff !important; }}
[role="option"], [role="option"] * {{ background-color:#ffffff !important; color:{INK} !important; }}
[role="option"]:hover, [role="option"]:hover *, [role="option"][aria-selected="true"],
[role="option"][aria-selected="true"] * {{ background-color:#eef7d0 !important; }}

/* Segmented control */
div[role="radiogroup"] {{ gap:4px; background:#ffffff; border:1px solid {LINE}; border-radius:999px;
                          padding:5px; width:fit-content; flex-wrap:wrap; }}
div[role="radiogroup"] label {{ border-radius:999px; padding:8px 18px !important; margin:0 !important; }}
div[role="radiogroup"] label > div:first-child, div[role="radiogroup"] label input + div {{ display:none !important; }}
div[role="radiogroup"] label p {{ color:{MUTED} !important; font-weight:700; }}
div[role="radiogroup"] label:has(input:checked) {{ background:{INK}; }}
div[role="radiogroup"] label:has(input:checked) p {{ color:#ffffff !important; }}

div[data-testid="stPlotlyChart"] {{ background:{CARD}; border:1px solid {LINE}; border-radius:22px; padding:10px;
                                     box-shadow:0 8px 24px -12px rgba(11,18,32,.18); overflow:hidden; }}
.foot {{ text-align:center; color:{MUTED} !important; margin-top:20px; }}
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
  <div><div class="ttl">Marketing Funnel &amp; <b>Lead Conversion</b></div>
  <p>Bank telemarketing campaign · who we reached, who engaged, and who subscribed to a term deposit</p></div>
  <div class="btns">
    <a class="rep" href="{REPORT_URL}" target="_blank">Open Full Report ↗</a>
    <a class="git" href="{REPO_URL}" target="_blank">GitHub Repository ↗</a>
  </div>
</div>""", unsafe_allow_html=True)

# ---------- Filters (collapsible) ----------
d = df.copy()
with st.expander("Filter leads", expanded=False):
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
        textfont=dict(color="#ffffff", size=15),
        marker=dict(color=[INK, SKY, MINT, CORAL]), connector=dict(fillcolor="#eef1f7")))
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
section = st.radio("Section", ["Who converts", "Campaign & channel", "Timing", "Key insights"],
                   horizontal=True, label_visibility="collapsed")

if section == "Who converts":
    c1, c2 = st.columns(2)
    show(c1, bars(conv("job"), "Conversion Rate by Job", SKY, horizontal=True, h=460))
    show(c2, bars(conv("Age Group"), "Conversion Rate by Age Group", CORAL, h=460))
    c1, c2, c3 = st.columns(3)
    show(c1, bars(conv("education"), "By Education Level", MINT))
    show(c2, bars(conv("marital"), "By Marital Status", INK))
    show(c3, bars(conv("Balance Group"), "By Account Balance", SKY))

elif section == "Campaign & channel":
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
                               fillcolor="rgba(20,184,166,0.15)"))
    fig.update_yaxes(visible=False, range=[0, s.max() * 1.3])
    fig.update_xaxes(title="Number of calls in this campaign", title_font=dict(color=MUTED))
    show(st, style(fig, "Conversion Rate vs Number of Calls"))

elif section == "Timing":
    m = d.groupby("Month", observed=True).agg(Leads=("Converted", "size"), Rate=("Converted", "mean"))
    fig = go.Figure()
    fig.add_trace(go.Bar(x=m.index.str.title(), y=m["Leads"], name="Leads contacted", marker_color="#dfe7ff",
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
    show(c1, bars((dur.groupby("Call", observed=True)["Converted"].mean() * 100), "Conversion by Call Length", SKY))
    pie = d["y"].value_counts().reindex(["no", "yes"]).fillna(0)
    fig = go.Figure(go.Pie(labels=["Not subscribed", "Subscribed"], values=pie.values, hole=0.62,
                           marker=dict(colors=[SKY, CORAL]), textinfo="percent",
                           textfont=dict(color="#ffffff", size=14), sort=False))
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
<a href="{REPORT_URL}" target="_blank" style="color:{SKY};font-weight:700">project report (PDF)</a>.</p></div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="foot">Data: Bank Marketing (UCI) · <a href="{REPORT_URL}" target="_blank">Full report (PDF)</a>'
            f' · <a href="{REPO_URL}" target="_blank">GitHub repository</a></div>', unsafe_allow_html=True)
