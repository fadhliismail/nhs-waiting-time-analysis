import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="NHS A&E Performance 2019–2025",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    national = pd.read_csv("data/processed/dashboard_national.csv", parse_dates=["period"])
    trust = pd.read_csv("data/processed/dashboard_trust.csv", parse_dates=["quarter_start_date"])
    trust["region_short"] = trust["region_short"].str.strip()
    return national, trust

national, trust = load_data()

st.sidebar.title("NHS A&E Dashboard")
page = st.sidebar.radio(
    "",
    ["About & Key Findings", "National Overview", "Trust Performance", "Seasonal Patterns", "Local Focus"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Source: NHS England A&E Attendances and Emergency Admissions, April 2019 – April 2026")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "Built by **Fadhli Ismail**  \n"
    "[GitHub](https://github.com/fadhliismail/nhs-waiting-time-analysis)"
)


if page == "About & Key Findings":
    st.title("NHS A&E Waiting Times — England 2019 to 2025")
    st.markdown(
        """
        This dashboard looks at six years of NHS A&E performance data, from the pre-pandemic
        baseline in 2019-20, through COVID, to today. The main metric throughout
        is the **4-hour standard**: the NHS target that 95% of patients attending a major A&E should be seen,
        treated, and either admitted or discharged within four hours of arrival.

        It covers **England's ~136 Type 1 (major) A&E departments**, using NHS England's
        monthly national time series and quarterly trust-level returns. I downloaded the raw files,
        cleaned and processed them in Python, and built this dashboard from the results.

        Use the sidebar to navigate. Each page looks at a different angle of the same story.
        """
    )

    st.markdown("---")
    st.subheader("Five things the data shows")

    col1, col2 = st.columns(2)

    with col1:
        st.error(
            "**1. Not one trust met the 95% target in 2024-25**\n\n"
            "In the financial year 2024-25, no Type 1 A&E department in England achieved the 95% standard "
            "for a full year. 96% of trusts performed below 75%, the threshold that triggers formal concern. "
            "This isn't a few struggling hospitals dragging down an otherwise healthy system. "
            "The whole distribution has shifted."
        )
        st.warning(
            "**2. Demand recovered. Performance didn't.**\n\n"
            "Type 1 attendances are only 6% above pre-pandemic levels by 2024-25. "
            "The 4-hour performance rate has fallen from 75% to 59% over the same period. "
            "Rising patient numbers alone don't explain the collapse. Something else changed."
        )
        st.error(
            "**3. 12-hour trolley waits rose 43-fold**\n\n"
            "In 2019-20, 12,435 patients waited more than 12 hours in A&E after a doctor had already "
            "decided they needed to be admitted to a ward. By 2024-25 that figure was 532,451. "
            "These patients weren't waiting to be seen. They were waiting for a bed. "
            "The bottleneck is the back door, not the front."
        )

    with col2:
        st.warning(
            "**4. The worst year was 2021-22**\n\n"
            "Performance dropped 15.3 percentage points in a single year as post-lockdown attendance "
            "rebounded faster than NHS capacity could respond. The system has never recovered to "
            "its pre-pandemic level. Each subsequent year has seen only marginal improvement."
        )
        st.info(
            "**5. The seasonal crisis is now year-round**\n\n"
            "A&E has always been harder in winter. But the summer–winter performance gap has "
            "narrowed from 7.8 percentage points to 4.3, and not because winters got better. "
            "Summer performance collapsed to near-winter levels. "
            "The system is under pressure every month of the year now."
        )

    st.markdown("---")
    st.subheader("About the data")
    st.markdown(
        """
        | Dataset | Coverage | Rows |
        |---------|----------|------|
        | National monthly time series | April 2019 – April 2026 | 85 months |
        | Quarterly by-provider | 2019-20 Q1 – 2024-25 Q4 | 5,062 trust-quarters |

        **Type 1 only.** The 4-hour standard applies to major A&E departments (Type 1).
        Type 2 (single-specialty units) and Type 3 (urgent treatment centres) are excluded because mixing them in
        would make the performance numbers meaningless. A minor injuries unit isn't comparable to a full A&E.

        **Percentages** are stored as decimals in the raw data (0.0–1.0) and converted here.

        Source: [NHS England A&E Attendances and Emergency Admissions](https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/)
        """
    )

    st.markdown("---")
    st.subheader("Further work")
    st.markdown(
        """
        A few things I'd like to add if I pick this up again:

        - **Workforce data.** NHS England publishes quarterly staffing figures by trust, covering headcount and
          full-time equivalent broken down by staff group (nurses, doctors, support staff). Joining that
          to the trust performance data on ODS code and quarter would let you test whether understaffing
          is correlated with worse 4-hour performance. It's a separate download and a fair bit of extra
          cleaning, but it'd make the analysis a lot more explanatory.

        - **Delayed discharge data.** NHS England also publishes monthly delayed transfer of care figures.
          Linking those to the 12-hour trolley wait trend would help quantify how much of the back-door
          problem is driven by social care delays specifically, which is directly relevant for a local
          authority audience.

        - **Longer time horizon.** The A&E time series goes back to 2010. Including the pre-2019 data
          would show the full decline from the last time the 95% target was consistently met (around 2014)
          and give more context to the COVID impact.
        """
    )


elif page == "National Overview":
    st.title("National Overview")

    st.markdown(
        """
        This page asks the most basic question: **what happened to NHS A&E performance over the last six years,
        and why?**

        The short answer is that attendances recovered to near pre-pandemic levels by 2021-22, but performance
        kept falling. That gap makes it hard to blame rising demand. Something else changed. The third chart
        below (12-hour Decision-to-Admit waits) points to what's actually driving it: patients stuck in A&E
        waiting for a hospital bed after they've already been assessed and told they need one. That's a
        capacity and discharge problem, not really an A&E problem.
        """
    )

    era_options = ["All"] + sorted(national["era"].dropna().unique().tolist())
    era_filter = st.selectbox("Filter by era", era_options)

    nat = national.copy()
    if era_filter != "All":
        nat = nat[nat["era"] == era_filter]

    # Scorecards
    latest = national.sort_values("period").iloc[-1]
    prev = national.sort_values("period").iloc[-2]
    yr_2024 = national[national["financial_year"] == "2024-25"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Type 1 Attendances (latest month)",
        f"{latest['type1_attendances']:,.0f}",
        delta=f"{latest['type1_attendances'] - prev['type1_attendances']:+,.0f} vs prev month"
    )
    col2.metric(
        "% Seen Within 4hrs (latest month)",
        f"{latest['pct_4hr_type1_pct']:.1f}%",
        delta=f"{latest['pct_4hr_type1_pct'] - prev['pct_4hr_type1_pct']:+.1f}pp vs prev month"
    )
    col3.metric(
        "2024-25 Avg Performance",
        f"{yr_2024['pct_4hr_type1_pct'].mean():.1f}%",
        delta=f"{yr_2024['pct_4hr_type1_pct'].mean() - 95:.1f}pp vs 95% target",
        delta_color="inverse"
    )
    col4.metric(
        "Months at 95% Target (2024-25)",
        f"{int(yr_2024['at_target'].sum())} / 12",
        delta_color="off"
    )

    st.markdown("---")

    # Attendances line chart
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=nat["period"], y=nat["type1_attendances"],
        mode="lines", name="Type 1 attendances",
        line=dict(color="#005EB8", width=2),
        hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra></extra>"
    ))
    fig1.add_vrect(
        x0="2020-03-01", x1="2021-06-01",
        fillcolor="orange", opacity=0.12, line_width=0,
        annotation_text="COVID-19", annotation_position="top left"
    )
    fig1.update_layout(
        title="Monthly Type 1 A&E Attendances — England",
        plot_bgcolor="white", hovermode="x unified",
        xaxis_title="", yaxis_title="Attendances"
    )
    fig1.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    fig1.update_xaxes(showgrid=False)
    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        "Attendances dropped roughly 50% in April 2020 as people stayed away during the first lockdown. "
        "They came back to pre-pandemic levels by 2021-22 and have kept rising since. "
        "By 2024-25, Type 1 attendance is about 6% above the 2019-20 baseline. Not nothing, but nowhere "
        "near enough to explain the performance collapse you'll see in the next chart."
    )

    st.markdown("---")

    # Performance line chart
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=nat["period"], y=nat["pct_4hr_type1_pct"],
        mode="lines", name="% seen within 4hrs",
        line=dict(color="#d73027", width=2),
        hovertemplate="%{x|%b %Y}: %{y:.1f}%<extra></extra>"
    ))
    fig2.add_hline(
        y=95, line_dash="dash", line_color="#1a9850", line_width=1.5,
        annotation_text="95% target", annotation_font_color="#1a9850"
    )
    fig2.add_vrect(
        x0="2020-03-01", x1="2021-06-01",
        fillcolor="orange", opacity=0.12, line_width=0,
        annotation_text="COVID-19", annotation_position="top left"
    )
    fig2.update_layout(
        title="% of Type 1 Patients Seen Within 4 Hours — England",
        plot_bgcolor="white", hovermode="x unified",
        xaxis_title="", yaxis_title="% seen within 4 hours",
        yaxis=dict(range=[50, 100], ticksuffix="%")
    )
    fig2.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    fig2.update_xaxes(showgrid=False)
    st.plotly_chart(fig2, use_container_width=True)
    st.warning(
        "Performance was already well below the 95% target before COVID. England hasn't consistently "
        "hit it since around 2014. But the post-pandemic collapse is on a different scale. "
        "The sharpest single drop was 2021-22: 15 percentage points in one year as attendance rebounded "
        "faster than the system could cope. It hasn't recovered since."
    )

    st.markdown("---")

    # 12-hour trolley wait chart
    st.markdown("#### 12-Hour Decision-to-Admit Waits")
    st.markdown(
        """
        This metric measures something very specific: patients who've **already been assessed by a doctor
        and told they need a hospital bed** but are still waiting in A&E more than 12 hours later because
        no bed is free. The clinical work is done. The A&E has done its job. The wait is happening
        because the rest of the hospital can't take them.

        This is often called the **back-door problem**: patients who can't be discharged from wards
        (often because social care arrangements aren't in place) block beds, which blocks admissions from A&E,
        which blocks new patients coming through the front door. It's a chain reaction that starts outside A&E.
        """
    )
    fig_trolley = go.Figure()
    fig_trolley.add_trace(go.Scatter(
        x=nat["period"], y=nat["dtoa_over_12hr"],
        mode="lines", name="12-hr DTA waits",
        line=dict(color="#7b2d8b", width=2),
        fill="tozeroy", fillcolor="rgba(123,45,139,0.1)",
        hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra></extra>"
    ))
    fig_trolley.add_vrect(
        x0="2020-03-01", x1="2021-06-01",
        fillcolor="orange", opacity=0.12, line_width=0,
        annotation_text="COVID-19", annotation_position="top left"
    )
    fig_trolley.update_layout(
        title="Monthly Patients Waiting 12+ Hours After Decision to Admit — England",
        plot_bgcolor="white", hovermode="x unified",
        xaxis_title="", yaxis_title="Patients per month"
    )
    fig_trolley.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    fig_trolley.update_xaxes(showgrid=False)
    st.plotly_chart(fig_trolley, use_container_width=True)

    val_2019 = national[national["financial_year"] == "2019-20"]["dtoa_over_12hr"].sum()
    val_2024 = national[national["financial_year"] == "2024-25"]["dtoa_over_12hr"].sum()
    st.error(
        f"**{val_2019:,.0f}** patients waited 12+ hours after a decision to admit in 2019-20.  \n"
        f"**{val_2024:,.0f}** in 2024-25.  \n"
        f"That's a **{val_2024/val_2019:.0f}x increase** in six years, which works out at roughly "
        f"**{val_2024/365:,.0f} patients every single day**. "
        "This is the single most important number in the dataset: it isolates the cause of the crisis "
        "in the part of the system beyond A&E itself."
    )


elif page == "Trust Performance":
    st.title("Trust Performance")

    st.markdown(
        """
        The national average hides a lot. This page breaks things down to individual trust level,
        roughly 136 major A&E departments across England.

        The main questions: **how spread out is performance, and is the whole distribution shifting or
        just a few outliers pulling the average down?** The league table shows the worst performers in
        a given year. The scatter tests whether bigger, busier trusts are systematically worse
        (short answer: not really, volume doesn't predict performance cleanly).
        The stacked bar at the bottom shows how the whole distribution has moved over six years.
        """
    )

    col1, col2, col3 = st.columns(3)
    fy_options = sorted(trust["financial_year"].unique().tolist(), reverse=True)
    selected_fy = col1.selectbox("Financial Year", fy_options)

    region_options = ["All"] + sorted(trust["region_short"].dropna().unique().tolist())
    selected_region = col2.selectbox("Region", region_options)

    band_order = ["1. >= 95% (target)", "2. 85-94%", "3. 75-84%", "4. < 75% (severe)"]
    band_options = ["All"] + band_order
    selected_band = col3.selectbox("Performance Band", band_options)

    t = trust[trust["financial_year"] == selected_fy].copy()
    if selected_region != "All":
        t = t[t["region_short"] == selected_region]
    if selected_band != "All":
        t = t[t["performance_band"] == selected_band]

    st.markdown("---")

    # league table, bottom 30
    league = (
        t.groupby(["code", "name"])["pct_4hr_type1_pct"]
        .mean().reset_index().dropna()
        .sort_values("pct_4hr_type1_pct")
        .head(30)
    )
    fig3 = px.bar(
        league, x="pct_4hr_type1_pct", y="name",
        orientation="h",
        title=f"Bottom 30 Trusts by Type 1 Performance — {selected_fy}",
        labels={"pct_4hr_type1_pct": "% seen within 4hrs", "name": ""},
        color="pct_4hr_type1_pct",
        color_continuous_scale=["#d73027", "#fee08b", "#1a9850"],
        range_color=[50, 95]
    )
    fig3.add_vline(
        x=95, line_dash="dash", line_color="#1a9850",
        annotation_text="95% target", annotation_font_color="#1a9850"
    )
    fig3.update_layout(plot_bgcolor="white", coloraxis_showscale=False, height=700)
    fig3.update_xaxes(showgrid=True, gridcolor="#e0e0e0", ticksuffix="%")
    fig3.update_yaxes(showgrid=False)
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "Sorted worst-first. Hover over any bar to see the trust name and exact figure. "
        "In 2024-25, the worst-performing trusts are seeing fewer than one in three patients "
        "within the 4-hour standard. The target is 19 in 20."
    )

    st.markdown("---")
    col_left, col_right = st.columns(2)

    # Scatter: volume vs performance
    trust_agg = (
        t.groupby(["code", "name", "region_short"])
        .agg(total_type1=("type1_attendances", "sum"), avg_perf=("pct_4hr_type1_pct", "mean"))
        .reset_index().dropna()
    )
    fig4 = px.scatter(
        trust_agg, x="total_type1", y="avg_perf",
        color="region_short", hover_name="name",
        title="Trust Volume vs Performance",
        labels={
            "total_type1": "Type 1 attendances",
            "avg_perf": "Avg % seen within 4hrs",
            "region_short": "Region"
        }
    )
    fig4.add_hline(y=95, line_dash="dash", line_color="#1a9850")
    fig4.update_layout(plot_bgcolor="white", yaxis=dict(ticksuffix="%"))
    fig4.update_xaxes(showgrid=True, gridcolor="#e0e0e0")
    fig4.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    col_left.plotly_chart(fig4, use_container_width=True)
    col_left.caption(
        "If volume were the main driver, you'd expect a clear downward slope with bigger trusts doing worse. "
        "The scatter is all over the place, which suggests it's more complicated than just patient numbers. "
        "Hover over any dot to see which trust it is."
    )

    # Donut: performance band
    band_colors = {
        "1. >= 95% (target)": "#1a9850",
        "2. 85-94%": "#fee08b",
        "3. 75-84%": "#fc8d59",
        "4. < 75% (severe)": "#d73027"
    }
    band_counts = (
        t["performance_band"]
        .value_counts()
        .reset_index()
    )
    band_counts.columns = ["performance_band", "count"]
    fig5 = px.pie(
        band_counts[band_counts["performance_band"].isin(band_order)],
        names="performance_band", values="count",
        title="Trusts by Performance Band",
        color="performance_band",
        color_discrete_map=band_colors,
        hole=0.4,
        category_orders={"performance_band": band_order}
    )
    col_right.plotly_chart(fig5, use_container_width=True)
    col_right.caption(
        "In 2019-20 roughly a third of trusts were meeting the 95% target. "
        "By 2024-25 the green segment has disappeared entirely. "
        "Change the year filter above to watch the distribution shift."
    )

    st.markdown("---")

    # performance band trend
    st.markdown(
        "The chart below shows how that distribution has shifted **across all six years**. "
        "Each bar adds up to 100% of trusts. Watch the green (at target) shrink and the red (severe) grow."
    )
    band_trend = (
        trust[trust["performance_band"].notna()]
        .groupby(["financial_year", "performance_band"])
        .size().reset_index(name="count")
    )
    totals = band_trend.groupby("financial_year")["count"].sum().reset_index(name="total")
    band_trend = band_trend.merge(totals, on="financial_year")
    band_trend["pct"] = (band_trend["count"] / band_trend["total"] * 100).round(1)
    band_trend = band_trend[band_trend["performance_band"].isin(band_order)]

    fig_band = px.bar(
        band_trend,
        x="financial_year", y="pct",
        color="performance_band",
        title="Share of NHS Trusts by Performance Band — 2019-20 to 2024-25",
        labels={"pct": "% of trusts", "financial_year": "", "performance_band": ""},
        category_orders={"performance_band": band_order},
        color_discrete_map=band_colors,
        barmode="stack",
        text_auto=".0f"
    )
    fig_band.update_layout(
        plot_bgcolor="white",
        yaxis=dict(ticksuffix="%", range=[0, 105]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    fig_band.update_traces(texttemplate="%{y:.0f}%", textposition="inside")
    fig_band.update_xaxes(showgrid=False)
    fig_band.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    st.plotly_chart(fig_band, use_container_width=True)
    st.warning(
        "This is what makes it clear it isn't just a handful of struggling trusts. "
        "In 2019-20, roughly 30% of trusts were meeting the target. By 2024-25 that's zero. "
        "The whole system shifted. It's structural, not a few bad apples."
    )


elif page == "Seasonal Patterns":
    st.title("Seasonal Patterns")

    st.markdown(
        """
        A&E has always been harder in winter, with more respiratory illness, more falls, and more frailty
        episodes all arriving at once. A seasonal dip is expected and well-documented.

        But the data shows something more troubling: **the summer recovery is disappearing**. The gap
        between the best and worst months has narrowed from 7.8 percentage points to 4.3, and not because
        winters got better. Summer performance collapsed towards winter levels.
        The system is now under pressure year-round, not just in the cold months.

        I've excluded the COVID year (2020-21) from the monthly average because suppressed attendances
        during lockdown distort the seasonal pattern too much to be useful here.
        """
    )

    col_a, col_b = st.columns(2)
    fy_options = sorted(national["financial_year"].unique().tolist())
    selected_years = col_a.multiselect(
        "Financial years to show (year-on-year chart)",
        fy_options, default=fy_options
    )
    season_options = ["All"] + sorted(national["season"].dropna().unique().tolist())
    selected_season = col_b.selectbox("Season (monthly chart)", season_options)

    st.markdown("---")

    # Monthly average bar
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    non_covid = national[national["financial_year"] != "2020-21"]
    if selected_season != "All":
        non_covid = non_covid[non_covid["season"] == selected_season]
    monthly_avg = (
        non_covid.groupby("month_name")["pct_4hr_type1_pct"]
        .mean().reindex(month_order).reset_index()
    )
    fig6 = px.bar(
        monthly_avg, x="month_name", y="pct_4hr_type1_pct",
        title="Average Type 1 Performance by Month (COVID year 2020-21 excluded)",
        labels={"pct_4hr_type1_pct": "Avg % seen within 4hrs", "month_name": ""},
        color="pct_4hr_type1_pct",
        color_continuous_scale=["#d73027", "#fee08b", "#1a9850"],
        range_color=[70, 88],
        text_auto=".1f"
    )
    fig6.add_hline(
        y=95, line_dash="dash", line_color="#1a9850",
        annotation_text="95% target", annotation_font_color="#1a9850"
    )
    fig6.update_layout(
        plot_bgcolor="white",
        yaxis=dict(range=[60, 100], ticksuffix="%"),
        coloraxis_showscale=False
    )
    fig6.update_traces(textposition="outside")
    fig6.update_xaxes(showgrid=False)
    fig6.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    st.plotly_chart(fig6, use_container_width=True)
    st.caption(
        "Winter months (Dec to Feb) consistently show the lowest performance, with more patients, "
        "sicker patients, and more admissions needed. But even the best summer months are nowhere near "
        "the 95% target. The seasonal dip explains some of the variation, but not the overall level."
    )

    st.markdown("---")

    # Year-on-year line
    if selected_years:
        yoy = national[national["financial_year"].isin(selected_years)]
        fig7 = px.line(
            yoy, x="fy_month_pos", y="pct_4hr_type1_pct",
            color="financial_year",
            title="Monthly Performance by Financial Year (Apr → Mar)",
            labels={
                "pct_4hr_type1_pct": "% seen within 4hrs",
                "fy_month_pos": "Month in financial year",
                "financial_year": "Year"
            }
        )
        fig7.add_hline(
            y=95, line_dash="dash", line_color="#1a9850",
            annotation_text="95% target", annotation_font_color="#1a9850"
        )
        fig7.update_layout(
            plot_bgcolor="white",
            yaxis=dict(ticksuffix="%"),
            hovermode="x unified"
        )
        fig7.update_xaxes(
            showgrid=False,
            tickvals=list(range(1, 13)),
            ticktext=["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
        )
        fig7.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
        st.plotly_chart(fig7, use_container_width=True)
        st.caption(
            "Each line is one financial year (April to March). The 2019-20 line sits at the top, "
            "that's the pre-pandemic baseline. Each year after sits lower. "
            "Use the multiselect above to isolate specific years for comparison. "
            "Try comparing 2019-20 against 2024-25 to see the full extent of the shift."
        )


elif page == "Local Focus":
    st.title("Local Focus — North West Anglia NHS FT")

    st.markdown(
        """
        North West Anglia NHS Foundation Trust runs **Hinchingbrooke Hospital** in Huntingdon,
        Cambridgeshire, the main acute hospital for much of Huntingdonshire. Its ODS code is **RGN**.

        This page asks: how does the local trust compare to the national picture and its East of England
        peers? Being near the national average might sound fine, but in 2024-25 the national average is
        59%, which is 36 percentage points below the target. Average now means failing by a long way.

        There's also a direct connection to local authority work worth flagging.
        Delayed hospital discharges (patients ready to leave a ward but waiting on social care
        arrangements) are one of the main drivers of the back-door bottleneck. Adult social care
        in Huntingdonshire is commissioned by Cambridgeshire County Council in partnership with
        district councils. How quickly home care can be arranged locally feeds directly into
        Hinchingbrooke's A&E performance numbers.
        """
    )

    rgn = trust[trust["code"] == "RGN"].copy()
    nat_quarterly = (
        trust.groupby("quarter_start_date")["pct_4hr_type1_pct"]
        .mean().reset_index()
        .rename(columns={"pct_4hr_type1_pct": "national_avg"})
    )

    rgn_2024 = rgn[rgn["financial_year"] == "2024-25"]["pct_4hr_type1_pct"].mean()
    nat_2024 = trust[trust["financial_year"] == "2024-25"]["pct_4hr_type1_pct"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("RGN 2024-25 Avg", f"{rgn_2024:.1f}%")
    col2.metric("National Avg 2024-25", f"{nat_2024:.1f}%")
    col3.metric("Gap vs National", f"{rgn_2024 - nat_2024:+.1f}pp")

    st.info(
        f"RGN sits close to the national median, roughly the 50th percentile among Type 1 trusts. "
        f"That means it's neither an outlier nor a star performer. "
        f"At {rgn_2024:.1f}%, it's {95 - rgn_2024:.1f} percentage points below the 95% target. "
        "Being average in 2024-25 means failing the standard by more than a third."
    )

    st.markdown("---")

    # RGN vs national trend
    fig8 = go.Figure()
    fig8.add_trace(go.Scatter(
        x=rgn["quarter_start_date"], y=rgn["pct_4hr_type1_pct"],
        mode="lines+markers", name="RGN (Hinchingbrooke)",
        line=dict(color="#005EB8", width=2),
        hovertemplate="%{x|%b %Y}: %{y:.1f}%<extra>RGN</extra>"
    ))
    fig8.add_trace(go.Scatter(
        x=nat_quarterly["quarter_start_date"], y=nat_quarterly["national_avg"],
        mode="lines", name="National average",
        line=dict(color="#888888", width=1.5, dash="dot"),
        hovertemplate="%{x|%b %Y}: %{y:.1f}%<extra>National avg</extra>"
    ))
    fig8.add_hline(
        y=95, line_dash="dash", line_color="#1a9850", line_width=1.5,
        annotation_text="95% target", annotation_font_color="#1a9850"
    )
    fig8.update_layout(
        title="Hinchingbrooke Type 1 Performance vs National Average (2019–2025)",
        plot_bgcolor="white", hovermode="x unified",
        yaxis=dict(ticksuffix="%"), xaxis_title=""
    )
    fig8.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    fig8.update_xaxes(showgrid=False)
    st.plotly_chart(fig8, use_container_width=True)
    st.caption(
        "RGN has tracked pretty closely with the national average throughout, "
        "falling at similar times and by similar amounts. There's no point where the local trust "
        "bucked the national trend for any sustained period. That tells you this is a system-wide problem "
        "showing up locally, not something specific to Hinchingbrooke."
    )

    st.markdown("---")

    # East of England peers
    st.markdown("#### East of England peer comparison (2024-25)")
    st.markdown(
        "How does Hinchingbrooke sit among the other major A&E trusts in its NHS England region? "
        "RGN is highlighted in dark blue. Sorted worst-first."
    )
    eoe = (
        trust[
            trust["region_short"].str.contains("East Of England", na=False) &
            (trust["financial_year"] == "2024-25")
        ]
        .groupby(["code", "name", "is_local_trust"])["pct_4hr_type1_pct"]
        .mean().reset_index().dropna()
        .sort_values("pct_4hr_type1_pct")
    )
    fig9 = px.bar(
        eoe, x="pct_4hr_type1_pct", y="name",
        orientation="h",
        title="East of England Trusts — Type 1 Performance 2024-25",
        labels={"pct_4hr_type1_pct": "Avg % seen within 4hrs", "name": ""},
        color="is_local_trust",
        color_discrete_map={1: "#005EB8", 0: "#aec7e8"}
    )
    fig9.add_vline(
        x=95, line_dash="dash", line_color="#1a9850",
        annotation_text="95% target", annotation_font_color="#1a9850"
    )
    fig9.update_layout(plot_bgcolor="white", showlegend=False, xaxis=dict(ticksuffix="%"))
    fig9.update_xaxes(showgrid=True, gridcolor="#e0e0e0")
    fig9.update_yaxes(showgrid=False)
    st.plotly_chart(fig9, use_container_width=True)
    st.caption(
        "No trust in the East of England region met the 95% target in 2024-25, which is consistent with "
        "the national picture. RGN sits in the middle of the regional pack. "
        "The variation within the region shows that local factors do matter, even within a system-wide crisis."
    )
