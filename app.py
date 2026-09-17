"""
Employee Satisfaction Analytics Dashboard
Nikita Singh | MBA (HR) | Symbiosis International (Deemed University)

Run with:  streamlit run app.py
"""

import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------
# PAGE CONFIG  (must be the first Streamlit call)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Employee Satisfaction Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = "employee_data(1).csv"
FEEDBACK_FILE = "feedback.csv"

DEPARTMENTS = [
    "Human Resources", "Finance", "Marketing", "Operations",
    "Information Technology", "Sales", "Customer Support",
]

# Palette
FOREST = "#1B4332"
MOSS = "#2D6A4F"
FERN = "#52B788"
SAGE = "#95D5B2"
MIST = "#E9F5EC"
AMBER = "#C08A2E"
CLAY = "#B3543F"

GREEN_SCALE = [MIST, SAGE, FERN, MOSS, FOREST]

# ----------------------------------------------------------------------
# STYLING
# ----------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600&display=swap');

/* ---------- Background: layered green light + fine paper weave ---------- */
.stApp {
    background-color: #F7FBF8;
    background-image:
        radial-gradient(900px 500px at 12% -5%, rgba(82,183,136,.20), transparent 60%),
        radial-gradient(700px 500px at 95% 8%, rgba(27,67,50,.14), transparent 55%),
        radial-gradient(800px 600px at 50% 110%, rgba(149,213,178,.22), transparent 60%),
        url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'><path d='M0 20h40M20 0v40' stroke='%231B4332' stroke-opacity='0.05' stroke-width='1'/></svg>");
    background-attachment: fixed;
}

html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #1B4332 0%, #2D6A4F 55%, #40916C 100%);
}
section[data-testid="stSidebar"] * { color: #EAF6EE !important; }
section[data-testid="stSidebar"] .stRadio label { font-size: 15px; }
.side-brand {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 23px; line-height: 1.25; font-weight: 700;
    padding: 6px 0 2px 0;
}
.side-sub { font-size: 12.5px; opacity: .78; letter-spacing: .01em; margin-bottom: 14px; }

/* ---------- Layout ---------- */
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1280px; }

/* ---------- Hero ---------- */
.hero {
    background: linear-gradient(120deg, #1B4332 0%, #2D6A4F 58%, #40916C 100%);
    border-radius: 26px;
    padding: 46px 48px 40px 48px;
    color: #F2FAF5;
    box-shadow: 0 22px 48px rgba(27,67,50,.28);
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "";
    position: absolute; right: -70px; top: -90px;
    width: 320px; height: 320px; border-radius: 50%;
    background: radial-gradient(circle, rgba(149,213,178,.38), transparent 68%);
}
.hero h1 {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 45px; line-height: 1.12; font-weight: 700;
    margin: 0 0 12px 0; letter-spacing: -.5px;
}
.hero p { font-size: 17px; max-width: 62ch; opacity: .92; margin: 0; }
.hero-rule { width: 64px; height: 3px; background: #95D5B2; border-radius: 3px; margin: 18px 0 20px 0; }

/* ---------- Section heading ---------- */
.section-head {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 27px; color: #1B4332; font-weight: 700;
    margin: 34px 0 6px 0;
}
.section-note { color: #5C7268; font-size: 14.5px; margin-bottom: 16px; }

/* ---------- Metric cards ---------- */
[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 20px 22px;
    border-radius: 16px;
    border-top: 4px solid #2D6A4F;
    box-shadow: 0 10px 26px rgba(27,67,50,.09);
}
[data-testid="stMetricValue"] {
    font-family: 'Fraunces', Georgia, serif;
    color: #1B4332; font-size: 34px;
}
[data-testid="stMetricLabel"] p { color: #5C7268; font-size: 13.5px; }

/* ---------- Panels ---------- */
.panel {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 24px 26px;
    box-shadow: 0 10px 26px rgba(27,67,50,.08);
    border-left: 5px solid #52B788;
}
.panel h4 {
    font-family: 'Fraunces', Georgia, serif;
    color: #1B4332; margin: 0 0 10px 0; font-size: 20px;
}
.panel ul { margin: 0; padding-left: 18px; color: #33443C; line-height: 1.75; }

/* ---------- Buttons ---------- */
.stButton > button {
    background: #2D6A4F; color: #FFFFFF; border: none;
    border-radius: 12px; height: 48px; font-size: 15px; font-weight: 500;
    transition: background .2s ease;
}
.stButton > button:hover { background: #40916C; color: #FFFFFF; }
.stButton > button:focus-visible { outline: 3px solid #95D5B2; outline-offset: 2px; }

/* ---------- Tabs / tables / misc ---------- */
.stTabs [data-baseweb="tab"] { font-size: 15px; }
.stTabs [aria-selected="true"] { color: #1B4332 !important; }
[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }
div[data-baseweb="notification"] { border-radius: 14px; }
hr { border: 0; height: 1px; background: #D6E7DC; }
.footer { text-align: center; color: #6B8077; font-size: 13.5px; padding-top: 26px; }

@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------
# DATA
# ----------------------------------------------------------------------
def sample_data(n=120):
    """Fallback dataset so the app always runs, even without the CSV."""
    import random

    random.seed(7)
    first = ["Aarav", "Diya", "Kabir", "Meera", "Rohan", "Ananya", "Vikram", "Sneha",
             "Arjun", "Priya", "Nikhil", "Tara", "Rahul", "Ishita", "Karan", "Neha"]
    last = ["Sharma", "Patel", "Iyer", "Nair", "Desai", "Joshi", "Mehta", "Rao",
            "Kulkarni", "Banerjee", "Gupta", "Reddy"]
    rows = []
    for i in range(1, n + 1):
        rating = random.choices([1, 2, 3, 4, 5], weights=[4, 9, 25, 38, 24])[0]
        rows.append({
            "EmpID": f"EMP{i:03d}",
            "Name": f"{random.choice(first)} {random.choice(last)}",
            "Department": random.choice(DEPARTMENTS),
            "Experience": random.randint(1, 18),
            "WorkLifeBalance": max(1, min(5, rating + random.randint(-1, 1))),
            "Recognition": max(1, min(5, rating + random.randint(-1, 1))),
            "CareerGrowth": max(1, min(5, rating + random.randint(-1, 1))),
            "Rating": rating,
            "Feedback": "",
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Source": "HR Survey",
        })
    return pd.DataFrame(rows)


def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        placeholder = False
    else:
        df = sample_data()
        placeholder = True

    for col, default in [("Department", "Not specified"), ("Experience", 0),
                         ("WorkLifeBalance", None), ("Recognition", None),
                         ("CareerGrowth", None), ("Feedback", ""),
                         ("Source", "HR Survey")]:
        if col not in df.columns:
            df[col] = default if default is not None else df.get("Rating", 3)
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    return df.dropna(subset=["Rating"]), placeholder


def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        return pd.read_csv(FEEDBACK_FILE)
    return pd.DataFrame(columns=[
        "EmpID", "Name", "Department", "Experience", "WorkLifeBalance",
        "Recognition", "CareerGrowth", "Rating", "Feedback", "Date", "Source"])


def save_feedback(row):
    fb = load_feedback()
    fb = pd.concat([fb, pd.DataFrame([row])], ignore_index=True)
    fb.to_csv(FEEDBACK_FILE, index=False)


def band(r):
    if r >= 4:
        return "Positive"
    if r == 3:
        return "Neutral"
    return "Negative"


def chart_layout(fig, height=380):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=13, color="#33443C"),
        title_font=dict(family="Fraunces, Georgia, serif", size=19, color=FOREST),
        legend=dict(orientation="h", y=-0.15),
    )
    fig.update_xaxes(gridcolor="#E3EEE7", zeroline=False)
    fig.update_yaxes(gridcolor="#E3EEE7", zeroline=False)
    return fig


# ----------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------
st.sidebar.markdown(
    "<div class='side-brand'>Employee Satisfaction<br>Analytics</div>"
    "<div class='side-sub'>MBA (HR) Project · Nikita Singh</div>",
    unsafe_allow_html=True,
)
page = st.sidebar.radio(
    "Go to",
    ["Home", "Share feedback", "Dashboard", "Employee data", "Recommendations"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
include_new = st.sidebar.checkbox("Include newly submitted feedback", value=True)

data, using_sample = load_data()
feedback = load_feedback()

if include_new and not feedback.empty:
    data = pd.concat([data, feedback], ignore_index=True)

data["Band"] = data["Rating"].apply(band)

st.sidebar.caption(f"{len(data)} responses loaded")
if using_sample:
    st.sidebar.warning("employee_data.csv not found — showing generated sample data.")


# ======================================================================
# HOME
# ======================================================================
if page == "Home":
    st.markdown(
        """
<div class="hero">
  <h1>What your people are actually telling you</h1>
  <div class="hero-rule"></div>
  <p>This dashboard turns raw employee feedback into the numbers HR can act on —
  satisfaction levels, department-wise patterns, and where engagement is slipping
  before it shows up in attrition.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    total = len(data)
    pos = (data["Band"] == "Positive").sum()
    neu = (data["Band"] == "Neutral").sum()
    neg = (data["Band"] == "Negative").sum()

    st.markdown("<div class='section-head'>Where things stand</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='section-note'>Based on {total} responses across "
        f"{data['Department'].nunique()} departments.</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Employees covered", total)
    c2.metric("Average rating", f"{data['Rating'].mean():.2f} / 5")
    c3.metric("Satisfied", f"{pos}", f"{pos/total*100:.0f}% of staff")
    c4.metric("At risk", f"{neg}", f"-{neg/total*100:.0f}% of staff", delta_color="inverse")

    left, right = st.columns([3, 2], gap="large")

    with left:
        dept = (data.groupby("Department")["Rating"].mean()
                .sort_values().reset_index())
        fig = px.bar(
            dept, x="Rating", y="Department", orientation="h",
            color="Rating", color_continuous_scale=GREEN_SCALE,
            range_x=[0, 5], title="Average satisfaction by department",
            text=dept["Rating"].round(2),
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(chart_layout(fig, 420), use_container_width=True)

    with right:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(data["Rating"].mean(), 2),
            number={"font": {"size": 46, "color": FOREST}},
            gauge={
                "axis": {"range": [0, 5], "tickcolor": "#5C7268"},
                "bar": {"color": MOSS, "thickness": 0.28},
                "steps": [
                    {"range": [0, 2.5], "color": "#F3DCD6"},
                    {"range": [2.5, 3.5], "color": "#F6EBD5"},
                    {"range": [3.5, 5], "color": MIST},
                ],
                "threshold": {"line": {"color": CLAY, "width": 3}, "value": 3.5},
            },
            title={"text": "Overall satisfaction index"},
        ))
        st.plotly_chart(chart_layout(fig, 420), use_container_width=True)

    st.markdown(
        f"""
<div class="panel">
  <h4>Reading this quickly</h4>
  <ul>
    <li>{pos} employees rate their experience 4 or 5 — this is the group to learn from.</li>
    <li>{neu} sit at a neutral 3. They are the swing group; small fixes move them up.</li>
    <li>{neg} rate 2 or below and need direct manager conversations.</li>
  </ul>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='footer'>Built by Nikita Singh · MBA (HR) · Symbiosis International (Deemed University)</div>",
                unsafe_allow_html=True)


# ======================================================================
# FEEDBACK FORM
# ======================================================================
elif page == "Share feedback":
    st.markdown("<div class='section-head'>Share your feedback</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-note'>Takes about a minute. Responses are added to the "
        "dashboard as soon as you submit.</div>",
        unsafe_allow_html=True,
    )

    with st.form("feedback_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Your name", placeholder="Leave blank to stay anonymous")
        dept = c2.selectbox("Department", DEPARTMENTS)

        c3, c4 = st.columns(2)
        emp_id = c3.text_input("Employee ID", placeholder="EMP121")
        exp = c4.number_input("Years with the company", 0, 40, 2)

        st.markdown("**How would you rate each of these?**")
        d1, d2, d3 = st.columns(3)
        wlb = d1.slider("Work-life balance", 1, 5, 3)
        rec = d2.slider("Recognition", 1, 5, 3)
        grw = d3.slider("Career growth", 1, 5, 3)

        overall = st.slider("Overall satisfaction at work", 1, 5, 3)
        comment = st.text_area(
            "Anything you'd like HR to know?",
            placeholder="What's working well, and what would you change?",
            height=120,
        )
        submitted = st.form_submit_button("Submit feedback", use_container_width=True)

    if submitted:
        save_feedback({
            "EmpID": emp_id.strip() or f"EMP{len(load_feedback()) + 121:03d}",
            "Name": name.strip() or "Anonymous",
            "Department": dept,
            "Experience": exp,
            "WorkLifeBalance": wlb,
            "Recognition": rec,
            "CareerGrowth": grw,
            "Rating": overall,
            "Feedback": comment.strip(),
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Source": "Employee submission",
        })
        st.success("Feedback recorded. Thank you — it's now part of the dashboard.")
        st.balloons()

    fb = load_feedback()
    st.markdown("<div class='section-head'>Recent submissions</div>", unsafe_allow_html=True)
    if fb.empty:
        st.info("No feedback submitted yet. The first response will appear here.")
    else:
        st.dataframe(
            fb[["Date", "Name", "Department", "Rating", "Feedback"]].tail(10)[::-1],
            use_container_width=True, hide_index=True,
        )
        st.download_button("Download all feedback (CSV)",
                           fb.to_csv(index=False).encode(),
                           "feedback_export.csv", "text/csv")


# ======================================================================
# DASHBOARD
# ======================================================================
elif page == "Dashboard":
    st.markdown("<div class='section-head'>Satisfaction dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>Hover any chart for exact values.</div>",
                unsafe_allow_html=True)

    depts = st.multiselect("Filter departments", sorted(data["Department"].unique()),
                           default=sorted(data["Department"].unique()))
    view = data[data["Department"].isin(depts)] if depts else data

    if view.empty:
        st.warning("No responses match this filter. Add a department to continue.")
        st.stop()

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Responses", len(view))
    m2.metric("Average rating", f"{view['Rating'].mean():.2f}")
    m3.metric("Positive", (view["Band"] == "Positive").sum())
    m4.metric("Neutral", (view["Band"] == "Neutral").sum())
    m5.metric("Negative", (view["Band"] == "Negative").sum())

    tab1, tab2, tab3 = st.tabs(["Overview", "Departments", "What drives it"])

    with tab1:
        a, b = st.columns(2, gap="large")
        with a:
            counts = view["Band"].value_counts().reindex(
                ["Positive", "Neutral", "Negative"]).fillna(0)
            fig = go.Figure(go.Pie(
                labels=counts.index, values=counts.values, hole=.58,
                marker=dict(colors=[MOSS, SAGE, CLAY], line=dict(color="white", width=3)),
                textinfo="label+percent", textfont=dict(size=14),
            ))
            fig.update_layout(title="Satisfaction split", showlegend=False)
            fig.add_annotation(text=f"{view['Rating'].mean():.2f}<br><span style='font-size:12px'>avg</span>",
                               showarrow=False, font=dict(size=28, color=FOREST, family="Fraunces, Georgia, serif"))
            st.plotly_chart(chart_layout(fig), use_container_width=True)
        with b:
            dist = view["Rating"].value_counts().sort_index().reset_index()
            dist.columns = ["Rating", "Employees"]
            fig = px.bar(dist, x="Rating", y="Employees", text="Employees",
                         color="Rating", color_continuous_scale=GREEN_SCALE,
                         title="How ratings are spread")
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(coloraxis_showscale=False, bargap=.35)
            st.plotly_chart(chart_layout(fig), use_container_width=True)

    with tab2:
        summary = (view.groupby("Department")
                   .agg(Responses=("Rating", "size"), Average=("Rating", "mean"))
                   .reset_index().sort_values("Average", ascending=False))
        summary["Average"] = summary["Average"].round(2)

        fig = px.bar(view.groupby(["Department", "Band"]).size().reset_index(name="Count"),
                     x="Department", y="Count", color="Band",
                     color_discrete_map={"Positive": MOSS, "Neutral": SAGE, "Negative": CLAY},
                     title="Sentiment mix within each department")
        fig.update_layout(barmode="stack", xaxis_tickangle=-20)
        st.plotly_chart(chart_layout(fig, 430), use_container_width=True)
        st.dataframe(summary, use_container_width=True, hide_index=True)

    with tab3:
        drivers = ["WorkLifeBalance", "Recognition", "CareerGrowth"]
        available = [d for d in drivers if d in view.columns and view[d].notna().any()]
        if available:
            melt = (view[["Department"] + available]
                    .melt("Department", var_name="Driver", value_name="Score")
                    .dropna())
            melt["Driver"] = melt["Driver"].replace({
                "WorkLifeBalance": "Work-life balance",
                "CareerGrowth": "Career growth"})
            pivot = melt.pivot_table(index="Department", columns="Driver",
                                     values="Score", aggfunc="mean").round(2)
            fig = px.imshow(pivot, color_continuous_scale=GREEN_SCALE, text_auto=True,
                            aspect="auto", zmin=1, zmax=5,
                            title="Average driver scores by department")
            st.plotly_chart(chart_layout(fig, 420), use_container_width=True)

            weakest = melt.groupby("Driver")["Score"].mean().idxmin()
            st.info(f"Lowest-scoring driver overall: **{weakest}**. "
                    "Start policy changes here for the biggest lift.")
        else:
            st.info("Add WorkLifeBalance, Recognition and CareerGrowth columns to your "
                    "CSV to unlock this view.")

        if "Experience" in view.columns:
            fig = px.scatter(view, x="Experience", y="Rating", color="Department",
                             size=view["Rating"] * 2, opacity=.75,
                             title="Does experience change how people feel?")
            st.plotly_chart(chart_layout(fig, 420), use_container_width=True)


# ======================================================================
# EMPLOYEE DATA
# ======================================================================
elif page == "Employee data":
    st.markdown("<div class='section-head'>Employee records</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-note'>{len(data)} rows.</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    search = c1.text_input("Search by name, ID or department")
    band_pick = c2.selectbox("Sentiment", ["All", "Positive", "Neutral", "Negative"])

    view = data.copy()
    if search:
        mask = view.astype(str).apply(
            lambda r: search.lower() in " ".join(r).lower(), axis=1)
        view = view[mask]
    if band_pick != "All":
        view = view[view["Band"] == band_pick]

    if view.empty:
        st.warning("Nothing matches that search. Clear the filters to see all records.")
    else:
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.download_button("Download this view (CSV)",
                           view.to_csv(index=False).encode(),
                           "employee_data_filtered.csv", "text/csv")

    comments = data[data["Feedback"].astype(str).str.strip().ne("")]
    if not comments.empty:
        st.markdown("<div class='section-head'>In their words</div>", unsafe_allow_html=True)
        for _, row in comments.tail(6)[::-1].iterrows():
            st.markdown(
                f"<div class='panel' style='margin-bottom:12px'>"
                f"<b>{row['Department']}</b> · rated {int(row['Rating'])}/5<br>"
                f"<span style='color:#33443C'>{row['Feedback']}</span></div>",
                unsafe_allow_html=True)


# ======================================================================
# RECOMMENDATIONS
# ======================================================================
elif page == "Recommendations":
    st.markdown("<div class='section-head'>What HR should do next</div>", unsafe_allow_html=True)
    avg = data["Rating"].mean()
    neg_share = (data["Band"] == "Negative").mean() * 100

    if avg >= 4:
        st.success(f"Satisfaction is strong at {avg:.2f}/5. Focus on protecting it.")
    elif avg >= 3:
        st.warning(f"Satisfaction is moderate at {avg:.2f}/5. There is clear room to improve.")
    else:
        st.error(f"Satisfaction is low at {avg:.2f}/5. Treat this as urgent.")

    dept_avg = data.groupby("Department")["Rating"].mean().sort_values()
    worst, best = dept_avg.index[0], dept_avg.index[-1]

    st.markdown(
        f"""
<div class="panel">
  <h4>Priority actions</h4>
  <ul>
    <li><b>{worst}</b> reports the lowest satisfaction ({dept_avg.iloc[0]:.2f}/5).
        Run listening sessions there first.</li>
    <li><b>{best}</b> is highest ({dept_avg.iloc[-1]:.2f}/5) — document what its managers
        do differently and carry it across.</li>
    <li>{neg_share:.0f}% of employees rate 2 or below. Schedule one-to-ones with that group
        within the month.</li>
    <li>Repeat this survey quarterly so trends, not single scores, guide decisions.</li>
  </ul>
</div>
""",
        unsafe_allow_html=True,
    )

    drivers = {"Work-life balance": "WorkLifeBalance", "Recognition": "Recognition",
               "Career growth": "CareerGrowth"}
    scores = {k: data[v].mean() for k, v in drivers.items()
              if v in data.columns and data[v].notna().any()}
    if scores:
        fig = px.bar(x=list(scores.keys()), y=[round(v, 2) for v in scores.values()],
                     text=[f"{v:.2f}" for v in scores.values()],
                     color=list(scores.values()), color_continuous_scale=GREEN_SCALE,
                     range_y=[0, 5], title="Which driver needs attention")
        fig.update_traces(textposition="outside")
        fig.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="Average score")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.markdown("<div class='footer'>Built by Nikita Singh · MBA (HR) · Symbiosis International (Deemed University)</div>",
                unsafe_allow_html=True)
