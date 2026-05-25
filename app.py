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
    locations = pd.read_csv("data/processed/trust_locations.csv")
    return national, trust, locations

national, trust, trust_locations = load_data()

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

    _yr2024 = national[national["financial_year"] == "2024-25"]
    _yr1920 = national[national["financial_year"] == "2019-20"]
    _val_2019 = _yr1920["dtoa_over_12hr"].sum()
    _val_2024 = _yr2024["dtoa_over_12hr"].sum()
    _trusts_2024 = trust[trust["financial_year"] == "2024-25"]
    _trusts_2024_perfs = _trusts_2024.groupby("code")["pct_4hr_type1_pct"].mean().dropna()
    _at_target = int((_trusts_2024_perfs >= 95).sum())
    _total_trusts = int(len(_trusts_2024_perfs))
    _avg_perf = _yr2024["pct_4hr_type1_pct"].mean()
    _gap_2425_h = (
        _yr2024[_yr2024["season"] == "Summer"]["pct_4hr_type1_pct"].mean()
        - _yr2024[_yr2024["season"] == "Winter"]["pct_4hr_type1_pct"].mean()
    )
    _gap_1920_h = (
        _yr1920[_yr1920["season"] == "Summer"]["pct_4hr_type1_pct"].mean()
        - _yr1920[_yr1920["season"] == "Winter"]["pct_4hr_type1_pct"].mean()
    )

    h1, h2, h3, h4 = st.columns(4)
    h1.metric(
        "2024-25 Type 1 Performance", f"{_avg_perf:.1f}%",
        delta=f"{_avg_perf - 95:.1f}pp vs 95% target", delta_color="normal"
    )
    h2.metric(
        "12-hr Trolley Waits Rise", f"{_val_2024 / _val_2019:.0f}x",
        delta=f"{_val_2019:,.0f} → {_val_2024:,.0f} patients/yr", delta_color="normal"
    )
    h3.metric(
        "Trusts at 95% Target (2024-25)", f"{_at_target} / {_total_trusts}",
        delta_color="normal"
    )
    h4.metric(
        "Seasonal Gap (2024-25)", f"{_gap_2425_h:.1f}pp",
        delta=f"{_gap_2425_h - _gap_1920_h:+.1f}pp since 2019-20 (was {_gap_1920_h:.1f}pp)", delta_color="normal"
    )

    st.markdown("---")

    _bar_html = (
        f'<div style="margin:4px 0 16px 0;">'
        f'<p style="margin:0 0 6px 0; font-size:13px; color:#555; font-weight:600;">Four-hour performance vs 95% target (2024-25)</p>'
        f'<div style="background:#eee; border-radius:4px; height:28px; position:relative;">'
        f'<div style="background:#d73027; width:{_avg_perf:.1f}%; height:100%; border-radius:4px 0 0 4px; display:flex; align-items:center; padding-left:10px;">'
        f'<span style="color:white; font-weight:bold; font-size:13px;">{_avg_perf:.1f}%</span>'
        f'</div>'
        f'<div style="position:absolute; top:-4px; left:95%; width:2px; height:36px; background:#1a9850;"></div>'
        f'<span style="position:absolute; top:6px; left:calc(95% + 5px); color:#1a9850; font-size:12px; font-weight:600;">95% target</span>'
        f'</div>'
        f'<p style="margin:5px 0 0 0; font-size:12px; color:#888;">{95 - _avg_perf:.1f}pp short of target</p>'
        f'</div>'
    )
    _bar_col, _ = st.columns([3, 1])
    with _bar_col:
        st.markdown(_bar_html, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Six years of NHS A&E data — monthly national figures and quarterly trust-level returns for up to 135 NHS trusts with Type 1 A&E departments. Use the sidebar to explore each angle.")

    st.markdown("---")
    st.subheader("Five things the data shows")

    fc1, fc2, fc3, fc4, fc5 = st.columns(5)
    with fc1:
        st.metric("Trusts at 95% target", f"0 / {_total_trusts}")
        st.caption("Not one major A&E met the standard in 2024-25. 96% performed below 75%.")
    with fc2:
        st.metric("Attendance rise since 2019", "+6%")
        st.caption("Demand nearly recovered. Performance fell by 16 percentage points.")
    with fc3:
        st.metric("12-hr trolley waits", "43x")
        st.caption(f"Patients assessed by a doctor but still waiting in A&E for a hospital bed. {_val_2019:,.0f} in 2019-20 → {_val_2024:,.0f} in 2024-25.")
    with fc4:
        st.metric("Worst single-year drop", "−15pp")
        st.caption("2021-22: post-lockdown demand rebounded faster than capacity could respond.")
    with fc5:
        st.metric("Seasonal gap (2024-25)", "4.3pp")
        st.caption("Down from 7.7pp — not because winters improved.")

    _about_map_data = (
        trust[trust["financial_year"] == "2024-25"]
        .groupby(["code", "name"])
        .agg(perf=("pct_4hr_type1_pct", "mean"), attendances=("type1_attendances", "sum"))
        .reset_index().dropna(subset=["perf"])
        .merge(trust_locations, on="code", how="inner")
    )
    fig_about_map = px.scatter_mapbox(
        _about_map_data,
        lat="lat", lon="lon",
        color="perf",
        size="attendances",
        size_max=22,
        hover_name="name",
        hover_data={"perf": ":.1f", "attendances": ":,.0f", "lat": False, "lon": False},
        labels={"perf": "% seen ≤4hrs", "attendances": "Type 1 attendances"},
        color_continuous_scale=[[0, "#d73027"], [0.45, "#fee08b"], [1, "#1a9850"]],
        range_color=[50, 80],
        mapbox_style="carto-positron",
        center={"lat": 52.6, "lon": -1.5},
        zoom=5.2,
        title="The performance collapse is nationwide — every dot is below the 95% target",
        height=400
    )
    fig_about_map.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar=dict(title="% seen<br>within 4hrs", ticksuffix="%", len=0.7)
    )
    st.plotly_chart(fig_about_map, use_container_width=True)
    st.caption("122 NHS trusts with major A&E departments. Bubble size = annual Type 1 attendances. Hover any bubble to explore. Each bubble represents a trust, not an individual hospital — some trusts run multiple sites, so the pin marks the trust's registered address.")

    st.markdown("---")
    with st.expander("About the data"):
        st.markdown(
            """
            | Dataset | Coverage | Rows |
            |---------|----------|------|
            | National monthly time series | April 2019 – April 2026 | 85 months |
            | Quarterly by-provider | 2019-20 Q1 – 2024-25 Q4 | 5,062 trust-quarters |

            **Type 1 only** — the 4-hour standard applies to major A&E departments. Type 2 and Type 3 are excluded.

            Source: [NHS England A&E Attendances and Emergency Admissions](https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/)
            """
        )
    with st.expander("Further work"):
        st.markdown(
            """
            - **Workforce data.** Quarterly staffing figures by trust (NHS England) — join on ODS code and quarter to test whether understaffing correlates with worse 4-hour performance.
            - **Delayed discharge data.** Monthly delayed transfer of care figures — link to the 12-hour trolley wait trend to quantify how much of the back-door problem is driven by social care delays.
            - **Longer time horizon.** The A&E time series goes back to 2010, including the last period when the 95% target was consistently met (around 2014).
            """
        )


elif page == "National Overview":
    st.title("National Overview")
    st.caption("Attendances recovered to near pre-pandemic levels by 2021-22. Performance kept falling — pointing to a capacity and discharge problem, not a demand problem.")

    era_options = ["All"] + sorted(national["era"].dropna().unique().tolist())
    era_filter = st.selectbox("Filter by era", era_options)

    nat = national.copy()
    if era_filter != "All":
        nat = nat[nat["era"] == era_filter]

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
        delta_color="normal"
    )
    col4.metric(
        "Months at 95% Target (2024-25)",
        f"{int(yr_2024['at_target'].sum())} / 12",
        delta_color="normal"
    )

    st.markdown("---")

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
    fig1.update_xaxes(
        showgrid=False,
        rangeselector=dict(buttons=[
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(count=3, label="3Y", step="year", stepmode="backward"),
            dict(step="all", label="All")
        ]),
        rangeslider=dict(visible=True, thickness=0.05)
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("Attendances are ~6% above the 2019-20 baseline — not enough to explain the performance collapse below.")

    st.markdown("---")

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
        title="Four-hour performance has fallen from 75% to 59% since 2019",
        plot_bgcolor="white", hovermode="x unified",
        xaxis_title="", yaxis_title="% seen within 4 hours",
        yaxis=dict(range=[50, 100], ticksuffix="%")
    )
    fig2.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    fig2.update_xaxes(
        showgrid=False,
        rangeselector=dict(buttons=[
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(count=3, label="3Y", step="year", stepmode="backward"),
            dict(step="all", label="All")
        ]),
        rangeslider=dict(visible=True, thickness=0.05)
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("The sharpest drop was 2021-22 (−15pp in one year). England hasn't consistently hit the 95% target since around 2014.")

    st.markdown("---")

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
        title="12-hour admitted waits have risen 43x — these patients were waiting for a bed, not to be seen",
        plot_bgcolor="white", hovermode="x unified",
        xaxis_title="", yaxis_title="Patients per month"
    )
    fig_trolley.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    fig_trolley.update_xaxes(
        showgrid=False,
        rangeselector=dict(buttons=[
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(count=3, label="3Y", step="year", stepmode="backward"),
            dict(step="all", label="All")
        ]),
        rangeslider=dict(visible=True, thickness=0.05)
    )
    st.plotly_chart(fig_trolley, use_container_width=True)

    val_2019 = national[national["financial_year"] == "2019-20"]["dtoa_over_12hr"].sum()
    val_2024 = national[national["financial_year"] == "2024-25"]["dtoa_over_12hr"].sum()
    st.caption(
        f"{val_2019:,.0f} patients in 2019-20 → {val_2024:,.0f} in 2024-25 "
        f"({val_2024/val_2019:.0f}x increase) — roughly {val_2024/365:,.0f} patients every day."
    )


elif page == "Trust Performance":
    st.title("Trust Performance")
    st.caption("The national average hides a lot — this page breaks performance down to individual trust level.")

    col1, col2, col3 = st.columns(3)
    fy_options = sorted(trust["financial_year"].unique().tolist(), reverse=True)
    selected_fy = col1.selectbox("Financial Year", fy_options)

    region_options = ["All"] + sorted(trust["region_short"].dropna().unique().tolist())
    selected_region = col2.selectbox("Region", region_options)

    band_order = ["1. >= 95% (target)", "2. 85-94%", "3. 75-84%", "4. < 75% (severe)"]
    band_options = ["All"] + band_order
    selected_band = col3.selectbox("Performance Band", band_options)

    search = st.text_input("Search trust name", placeholder="e.g. Cambridge, Portsmouth, Royal Free...")

    t = trust[trust["financial_year"] == selected_fy].copy()
    if selected_region != "All":
        t = t[t["region_short"] == selected_region]
    if selected_band != "All":
        t = t[t["performance_band"] == selected_band]
    if search:
        t = t[t["name"].str.contains(search, case=False, na=False)]

    st.markdown("---")

    _t_by_code = t.groupby("code")["pct_4hr_type1_pct"].mean().dropna()
    _t_total_codes = len(_t_by_code)
    if _t_total_codes > 0:
        _t_at_tgt = int((_t_by_code >= 95).sum())
        _t_severe = int((_t_by_code < 75).sum())
        sm1, sm2, sm3 = st.columns(3)
        sm1.metric("Trusts at 95% Target", f"{_t_at_tgt} / {_t_total_codes}")
        sm2.metric(
            "Trusts Below 75% (Severe)", f"{_t_severe} / {_t_total_codes}",
            delta=f"{_t_severe / _t_total_codes * 100:.0f}% of trusts shown", delta_color="normal"
        )
        sm3.metric(
            "Average Performance", f"{_t_by_code.mean():.1f}%",
            delta=f"{_t_by_code.mean() - 95:.1f}pp vs target", delta_color="normal"
        )
        st.markdown("---")

    _map_data = (
        trust[trust["financial_year"] == selected_fy]
        .groupby(["code", "name", "region_short"])
        .agg(
            perf=("pct_4hr_type1_pct", "mean"),
            attendances=("type1_attendances", "sum")
        )
        .reset_index()
        .dropna(subset=["perf"])
        .merge(trust_locations, on="code", how="inner")
    )
    _map_best_row = _map_data.loc[_map_data["perf"].idxmax()]

    fig_map = px.scatter_mapbox(
        _map_data,
        lat="lat", lon="lon",
        color="perf",
        size="attendances",
        size_max=28,
        hover_name="name",
        hover_data={
            "perf": ":.1f",
            "attendances": ":,.0f",
            "region_short": True,
            "lat": False, "lon": False
        },
        labels={"perf": "% seen ≤4hrs", "attendances": "Type 1 attendances", "region_short": "Region"},
        color_continuous_scale=[[0, "#d73027"], [0.45, "#fee08b"], [1, "#1a9850"]],
        range_color=[50, 80],
        mapbox_style="carto-positron",
        center={"lat": 52.6, "lon": -1.5},
        zoom=5.2,
        title=f"Every trust is failing the 95% target — best performer: {_map_best_row['name']} at {_map_best_row['perf']:.1f}%",
        height=520
    )
    fig_map.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
            title="% seen<br>within 4hrs",
            ticksuffix="%",
            len=0.75
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("Bubble size = annual Type 1 attendances. Colour = average 4-hour performance. Hover for trust detail. Each bubble is a trust, not an individual hospital — some trusts run multiple sites, so the pin marks the trust's registered address.")

    st.markdown("---")

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
    st.caption("Sorted worst-first. Hover for exact figures.")

    st.markdown("---")
    col_left, col_right = st.columns(2)

    trust_agg = (
        t.groupby(["code", "name", "region_short"])
        .agg(total_type1=("type1_attendances", "sum"), avg_perf=("pct_4hr_type1_pct", "mean"))
        .reset_index().dropna()
    )
    fig4 = px.scatter(
        trust_agg, x="total_type1", y="avg_perf",
        color="region_short", hover_name="name",
        title="Volume does not predict performance",
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
    col_left.caption("No clear pattern — busier trusts are not systematically worse. Hover to identify trusts.")

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
    col_right.caption("Change the year filter to watch the green segment disappear.")

    st.markdown("---")

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
        title="The whole distribution shifted — not just a few bad trusts",
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
    st.caption("In 2019-20, a small handful of trust-quarters hit the 95% target. By 2024-25, none did.")


elif page == "Seasonal Patterns":
    st.title("Seasonal Patterns")
    st.caption("The seasonal gap is narrowing — not because winters improved, but because summers collapsed.")

    _yr2425_s = national[national["financial_year"] == "2024-25"]
    _best_2425 = _yr2425_s["pct_4hr_type1_pct"].max()
    _worst_2425 = _yr2425_s["pct_4hr_type1_pct"].min()
    _gap_2425 = (
        _yr2425_s[_yr2425_s["season"] == "Summer"]["pct_4hr_type1_pct"].mean()
        - _yr2425_s[_yr2425_s["season"] == "Winter"]["pct_4hr_type1_pct"].mean()
    )
    _yr1920_s = national[national["financial_year"] == "2019-20"]
    _gap_1920 = (
        _yr1920_s[_yr1920_s["season"] == "Summer"]["pct_4hr_type1_pct"].mean()
        - _yr1920_s[_yr1920_s["season"] == "Winter"]["pct_4hr_type1_pct"].mean()
    )

    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Best month (2024-25)", f"{_best_2425:.1f}%")
    sc2.metric("Worst month (2024-25)", f"{_worst_2425:.1f}%")
    sc3.metric(
        "Seasonal gap", f"{_gap_2425:.1f}pp",
        delta=f"{_gap_2425 - _gap_1920:+.1f}pp since 2019-20 (was {_gap_1920:.1f}pp)", delta_color="normal"
    )
    st.markdown("---")

    col_a, col_b = st.columns(2)
    fy_options = sorted(national["financial_year"].unique().tolist())
    selected_years = col_a.multiselect(
        "Financial years to show (year-on-year chart)",
        fy_options, default=fy_options
    )
    season_options = ["All"] + sorted(national["season"].dropna().unique().tolist())
    selected_season = col_b.selectbox("Season (monthly chart)", season_options)

    st.markdown("---")

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
    st.caption("Even the best summer months are far below the 95% target.")

    st.markdown("---")

    if selected_years:
        yoy = national[national["financial_year"].isin(selected_years)]
        fig7 = px.line(
            yoy, x="fy_month_pos", y="pct_4hr_type1_pct",
            color="financial_year",
            title="Each year since 2019-20 has performed lower than the last",
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
        st.caption("Try isolating 2019-20 vs 2024-25 to see the full shift.")


elif page == "Local Focus":
    st.title("Local Focus — North West Anglia NHS FT")
    st.caption("Hinchingbrooke Hospital (RGN) serves Huntingdon and much of Huntingdonshire. Being near the national average means failing the target by 36 percentage points.")

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

    _trust_perfs_2024 = (
        trust[trust["financial_year"] == "2024-25"]
        .groupby("code")["pct_4hr_type1_pct"].mean().dropna().sort_values()
    )
    _rank = int((_trust_perfs_2024 < rgn_2024).sum())
    _total_ranked = len(_trust_perfs_2024)
    _percentile = _rank / _total_ranked * 100

    _pct_html = (
        f'<div style="margin:12px 0 8px 0;">'
        f'<p style="margin:0 0 4px 0; font-size:13px; font-weight:600; color:#555;">RGN\'s position among all Type 1 trusts (2024-25)</p>'
        f'<div style="display:flex; justify-content:space-between; font-size:11px; color:#aaa; margin-bottom:3px;">'
        f'<span>← Worst performing</span><span>Best performing →</span>'
        f'</div>'
        f'<div style="background:#eee; border-radius:4px; height:20px; position:relative;">'
        f'<div style="position:absolute; top:-3px; left:{_percentile:.0f}%; width:3px; height:26px; background:#005EB8; border-radius:2px;"></div>'
        f'</div>'
        f'<p style="margin:5px 0 0 0; font-size:12px; color:#555;">'
        f'<b style="color:#005EB8;">RGN: {_percentile:.0f}th percentile</b> — better than {_rank} of {_total_ranked} trusts'
        f'</p>'
        f'</div>'
    )
    _pct_col, _ = st.columns([3, 1])
    with _pct_col:
        st.markdown(_pct_html, unsafe_allow_html=True)

    st.markdown("---")

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
        title="RGN tracks the national average closely — this is a system-wide problem, not a local one",
        plot_bgcolor="white", hovermode="x unified",
        yaxis=dict(ticksuffix="%"), xaxis_title=""
    )
    fig8.update_yaxes(showgrid=True, gridcolor="#e0e0e0")
    fig8.update_xaxes(showgrid=False)
    st.plotly_chart(fig8, use_container_width=True)

    st.markdown("---")

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
        title="East of England — RGN sits mid-pack (2024-25)",
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
    st.caption("No trust in the East of England met the 95% target in 2024-25.")

    st.markdown("---")

    _eoe_map = (
        trust[
            trust["region_short"].str.contains("East Of England", na=False) &
            (trust["financial_year"] == "2024-25")
        ]
        .groupby(["code", "name"])
        .agg(perf=("pct_4hr_type1_pct", "mean"), attendances=("type1_attendances", "sum"))
        .reset_index().dropna(subset=["perf"])
        .merge(trust_locations, on="code", how="inner")
    )
    _rgn_row = _eoe_map[_eoe_map["code"] == "RGN"].iloc[0]

    fig_local_map = px.scatter_mapbox(
        _eoe_map,
        lat="lat", lon="lon",
        color="perf",
        size="attendances",
        size_max=24,
        hover_name="name",
        hover_data={"perf": ":.1f", "attendances": ":,.0f", "lat": False, "lon": False},
        labels={"perf": "% seen ≤4hrs", "attendances": "Type 1 attendances"},
        color_continuous_scale=[[0, "#d73027"], [0.45, "#fee08b"], [1, "#1a9850"]],
        range_color=[50, 80],
        mapbox_style="carto-positron",
        center={"lat": 52.3, "lon": 0.3},
        zoom=6.8,
        height=460
    )
    fig_local_map.add_trace(go.Scattermapbox(
        lat=[_rgn_row["lat"]], lon=[_rgn_row["lon"]],
        mode="markers+text",
        marker=dict(size=22, color="#005EB8"),
        text=["Hinchingbrooke"],
        textposition="top right",
        customdata=[[_rgn_row["perf"], _rgn_row["attendances"]]],
        hovertemplate="<b>North West Anglia NHS FT (RGN)</b><br>%{customdata[0]:.1f}% seen within 4hrs<br>%{customdata[1]:,.0f} attendances<extra></extra>",
        showlegend=False
    ))
    fig_local_map.update_layout(
        title="Hinchingbrooke sits mid-table in the East of England — mid-table means failing by 36pp",
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar=dict(title="% seen<br>within 4hrs", ticksuffix="%", len=0.75)
    )
    st.plotly_chart(fig_local_map, use_container_width=True)
    st.caption("Blue = Hinchingbrooke (RGN). Other East of England trusts coloured red-to-green by 4-hour performance (2024-25). Each bubble is a trust — some trusts run multiple sites, so the pin marks the trust's registered address.")
