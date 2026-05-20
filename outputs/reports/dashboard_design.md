# Dashboard Design Spec — NHS A&E Performance 2019–2025

**Tool:** Looker Studio (free, browser-based)  
**Data sources:** Two Google Sheets (upload the dashboard CSVs — see Notebook 07)  
**Audience:** Non-technical — local authority officers, public

---

## Data Sources to Connect

| Looker Studio name | Google Sheet | CSV source |
|--------------------|-------------|------------|
| `NHS AE — National` | NHS AE — National Monthly | `dashboard_national.csv` |
| `NHS AE — Trust` | NHS AE — Trust Quarterly | `dashboard_trust.csv` |

**Date field configuration in Looker Studio:**
- National source: set `period` as Date, format `YYYY-MM-DD`
- Trust source: set `quarter_start_date` as Date, format `YYYY-MM-DD`

---

## Dashboard Structure — 4 Pages

---

### Page 1: National Overview

**Purpose:** High-level story — attendances recovered, performance did not.

**Layout (top to bottom):**

**Row 1 — Scorecards (4 across)**
- Latest month Type 1 attendances (metric: `type1_attendances`, comparison: previous period)
- Latest month Type 1 4hr % (metric: `pct_4hr_type1_pct`, comparison: previous period)
- 2024-25 annual avg vs 2019-20 (use a calculated field or scorecard with filter)
- Number of months at ≥95% target in 2024-25 (metric: SUM of `at_target`)

**Row 2 — Time series: Attendances**
- Chart type: Line chart
- Data source: National
- Dimension: `period`
- Metric: `type1_attendances`
- Title: "Monthly Type 1 A&E Attendances — England"
- Add a reference line at 0 to emphasise COVID drop (April 2020 dip)
- Colour: blue

**Row 3 — Time series: 4-hour performance**
- Chart type: Line chart
- Data source: National
- Dimension: `period`
- Metric: `pct_4hr_type1_pct`
- Add reference line at 95 (the target)
- Title: "% of Type 1 Patients Seen Within 4 Hours — England"
- Colour: red (below target feels appropriate)
- Y-axis: 0 to 100

**Filters (top right):**
- Date range control on `period`
- Dropdown: `era` (Pre-COVID / COVID / Post-COVID)

---

### Page 2: Trust Performance

**Purpose:** Show the distribution across ~136 trusts and allow drilling by region.

**Layout:**

**Row 1 — Filters (controls)**
- Dropdown: `financial_year`
- Dropdown: `region_short`
- Dropdown: `performance_band` (useful for filtering to just severely underperforming trusts)

**Row 2 — Bar chart: Trust league table**
- Chart type: Bar chart (horizontal, sorted)
- Data source: Trust
- Dimension: `name`
- Metric: AVG `pct_4hr_type1_pct`
- Sort: metric ascending (worst first)
- Limit to top/bottom 20 with the chart's "rows to show" setting
- Add reference line at 95
- Title: "Type 1 4-Hour Performance by Trust (2024-25)"
- Tip: filter page to `financial_year = 2024-25` using a page-level filter

**Row 3 (two side by side):**

Left — Scatter plot: size vs performance
- Chart type: Scatter chart
- Data source: Trust
- X dimension: AVG `type1_attendances`
- Y metric: AVG `pct_4hr_type1_pct`
- Colour dimension: `region_short`
- Bubble size: `type1_attendances`
- Title: "Trust Size vs 4-Hour Performance (2024-25)"

Right — Donut: performance banding
- Chart type: Donut chart
- Data source: Trust
- Dimension: `performance_band`
- Metric: COUNT of `code`
- Title: "Trusts by Performance Band (2024-25)"
- Colours: band 1 = green, band 2 = yellow, band 3 = orange, band 4 = red

---

### Page 3: Seasonal Patterns

**Purpose:** Show the seasonal cycle — winter dip, summer recovery (or lack thereof).

**Layout:**

**Row 1 — Bar chart: Monthly profile**
- Chart type: Bar chart
- Data source: National
- Dimension: `month_name`
- Metric: AVG `pct_4hr_type1_pct`
- Sort dimension by `month` (1–12) not alphabetically
- Add reference line at 95
- Title: "Average 4-Hour Performance by Calendar Month"
- Tip: add page-level filter for `era` to compare pre vs post

**Row 2 — Line chart: Year-on-year profiles**
- Chart type: Line chart
- Data source: National
- Dimension: `fy_month_pos` (1=Apr … 12=Mar)
- Breakdown dimension: `financial_year`
- Metric: AVG `pct_4hr_type1_pct`
- Title: "Monthly Performance by Financial Year (Apr → Mar)"
- Colour each year differently
- Add reference line at 95

**Row 3 — Scorecard pair:**
- "Best month (national avg)": use a MAX aggregation + month filter
- "Worst month (national avg)": use a MIN aggregation + month filter

**Filters:**
- Dropdown: `financial_year` (multi-select)
- Dropdown: `season`

---

### Page 4: Local Focus — Huntingdonshire

**Purpose:** Contextualise the analysis for the Huntingdonshire DC audience. North West Anglia NHS FT (RGN) runs Hinchingbrooke Hospital, Huntingdon.

**Layout:**

**Row 1 — Title text box:**
> "North West Anglia NHS Foundation Trust (RGN) — Hinchingbrooke Hospital, Huntingdon"

**Row 2 — Scorecards (3 across)**
- RGN 2024-25 avg 4hr %: filter to `code = RGN`, `financial_year = 2024-25`, AVG `pct_4hr_type1_pct`
- National avg 2024-25 for comparison: no trust filter, same year
- Gap vs national (calculated field: RGN avg − national avg)

**Row 3 — Line chart: RGN performance over time**
- Chart type: Line chart
- Data source: Trust
- Filter: `code = RGN`
- Dimension: `quarter_start_date`
- Metric: `pct_4hr_type1_pct`
- Add reference line at 95
- Add a second metric line for the national average (requires blended data source — see note below)
- Title: "Hinchingbrooke Type 1 4-Hour Performance (2019–2025)"

**Row 4 — Bar chart: RGN vs East of England regional peers**
- Chart type: Bar chart (horizontal)
- Data source: Trust
- Filter: `region_short = East of England`, `financial_year = 2024-25`
- Dimension: `name`
- Metric: AVG `pct_4hr_type1_pct`
- Colour: highlight `is_local_trust = 1` in a distinct colour
- Title: "East of England Trusts — 4-Hour Performance 2024-25"

**Note on blended data:** To show RGN vs national average on the same chart, use Looker Studio's *Blend data* feature:
1. Left join: Trust source filtered to `code = RGN` on `quarter_start_date`
2. Right join: National source on `period`
3. This allows both series on one axis

---

## Styling Guide

| Element | Recommendation |
|---------|---------------|
| Colour palette | Blue for pre-COVID / positive; red/orange for post-COVID / negative; green for 95% target line |
| Background | White (#FFFFFF) — clean, professional |
| Font | Google Sans or Roboto |
| Target line | Always 95%, green, dashed |
| COVID era shading | Not directly supported in Looker Studio — add a text annotation instead |
| Title bar | Dark navy (#1a237e) with white text |
| Page tabs | Label: Overview / Trusts / Seasonal / Local Focus |

---

## Calculated Fields to Create in Looker Studio

If you need any of these in Looker Studio itself (not pre-computed in the CSV):

| Field name | Formula | Where |
|------------|---------|-------|
| `Gap vs target` | `95 - pct_4hr_type1_pct` | Both sources |
| `Year label` | `YEAR(period)` | National |
| `Month number` | `MONTH(period)` | National (use `month` column instead) |

---

## Key Messages to Highlight on Dashboard

These are the findings that should be visible without any drilling:

1. **Zero trusts at target in 2024-25** — make this a prominent scorecard
2. **−15.3pp drop in 2021-22** — annotate on the national trend line
3. **Winter dip is consistent but the floor has fallen** — visible on the seasonal page
4. **RGN (local trust) sits at the national median** — contextualise: average now means 59%
