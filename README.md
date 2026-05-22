# NHS A&E Waiting Times Analysis (2019–2025)

An end-to-end analysis of NHS England Accident and Emergency performance data across six financial years: the pre-COVID baseline, the pandemic period, and the recovery that didn't really materialise.

The analysis looks at national trends, trust-level variation across roughly 135 major A&E departments, seasonal demand and performance patterns, and the local picture for the Cambridgeshire and Peterborough Integrated Care Board area.

---

## Summary

NHS A&E performance has been in structural decline for a decade, but the data from 2019 onwards makes the scale of that decline hard to ignore. Before COVID, roughly three-quarters of Type 1 patients were being seen within the 4-hour target, already well below the 95% standard but broadly stable. By 2024-25 that figure has fallen to around 59%, and not a single major A&E trust in England met the target for the entire year.

What's striking is that rising demand doesn't explain it. Patient volumes are only 6% above pre-pandemic levels. The 12-hour "trolley wait" metric (patients who've been assessed and are waiting for a hospital bed) rose 43-fold over the same period. The bottleneck isn't at the front door, it's at the back: the hospital can't discharge patients into the community fast enough to free up beds, so admitted patients pile up in A&E and block the flow. That's a social care and capacity problem, not purely an A&E problem.

The seasonal picture has shifted too. The traditional winter spike still exists, but the summer trough has almost vanished. The system is now under pressure year-round. Winter used to be the exception; it's starting to look like the baseline.

---

## Key Findings

- **Demand recovered; performance didn't.** Type 1 A&E attendances are 6% above pre-pandemic levels by 2024-25. The 4-hour standard has fallen from 75% to 59% over the same period, a divergence that rules out rising demand as the primary explanation.
- **The worst single year was 2021-22: −15.3 percentage points** on Type 1 performance, as post-lockdown attendance rebounded faster than NHS capacity could respond.
- **In 2024-25, not one Type 1 trust in England met the 95% target.** 95.9% of trusts performed below 75%.
- **12-hour Decision-to-Admit waits rose 43-fold** (from 12,435 in 2019-20 to 532,451 in 2024-25). This metric isolates the back-door cause: patients waiting in A&E for a ward bed after clinical assessment is complete.
- **Seasonal patterns have changed.** The summer–winter performance gap narrowed from 7.8 to 4.3 percentage points. Not because winters improved, but because summer performance collapsed to near-winter levels. The crisis is now year-round.
- **The local trust (RGN, North West Anglia / Hinchingbrooke, Huntingdon) sits at the 50th national percentile**, averaging 58.8% in 2024-25. Being average now means failing the target by 36 percentage points.

---

## Stack

| Tool | Purpose |
|------|---------|
| Python (pandas, NumPy) | Data loading, cleaning, transformation |
| matplotlib / seaborn | Exploratory visualisation |
| SQLite | Structured querying |
| Jupyter Notebook | Analysis environment |
| Plotly | Interactive HTML charts |
| Streamlit | Dashboard app (deployed on Streamlit Community Cloud) |

---

## Live Dashboard

**[View the dashboard](https://nhs-waiting-time-analysis-ftffjzfb52xgeqyn2mgc5d.streamlit.app/)**

No installation needed. Open the link and explore the data directly in your browser.

Five pages: About & Key Findings, National Overview, Trust Performance, Seasonal Patterns, Local Focus (Hinchingbrooke / North West Anglia NHS Trust).

---

## Data Source

NHS England — [A&E Attendances and Emergency Admissions](https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/)

| Dataset | Path | Description |
|---------|------|-------------|
| National time series | `data/raw/time_series/` | Monthly England-wide totals, Aug 2010–Apr 2026 (1 file) |
| Quarterly by-provider | `data/raw/quarterly_by_provider/` | Trust-level data, 2019-20 Q1 through 2024-25 Q4 (24 files) |

Raw data files are excluded from version control. Download from the link above and place in `data/raw/`.

---

## Getting Started

```bash
git clone <repo-url>
cd nhs_waiting_time

python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python -m ipykernel install --user --name=nhs-venv --display-name="NHS Waiting Time"

# Run the dashboard locally
streamlit run app.py
```

> **xlrd compatibility note:** There's a bug in xlrd 2.0.1 that affects the 2024-25 Q3 and Q4 files. After installing, patch one line in `.venv/lib/python3.x/site-packages/xlrd/book.py` at line 1472:
> ```python
> # Change:
> assert _unused_i == nstrings - 1
> # To:
> pass
> ```
> All 24 quarterly files load correctly after this patch.

---

## Project Structure

```
├── app.py                              # Streamlit dashboard
├── data/
│   ├── raw/                            # Source XLS files (not in repo — download separately)
│   │   ├── time_series/                # National monthly aggregate
│   │   └── quarterly_by_provider/      # 24 quarterly trust-level files
│   └── processed/                      # Cleaned CSVs produced by notebooks
├── notebooks/                          # Jupyter notebooks (numbered — run in order)
├── outputs/
│   └── figures/                        # Chart exports (PNG and interactive HTML)
└── requirements.txt
```

---

## Notebooks

| # | Notebook | Description |
|---|----------|-------------|
| 01 | `01_data_loading_and_inspection.ipynb` | Load raw files, inspect structure, identify cleaning requirements |
| 02 | `02_data_cleaning.ipynb` | Clean and standardise; export `national_monthly.csv` and `quarterly_by_provider.csv` |
| 03 | `03_eda_national_trends.ipynb` | National attendance and 4-hour performance trends, 6 charts |
| 04 | `04_eda_trust_level.ipynb` | Trust-level performance distribution, league table, regional heatmap, local trust analysis |
| 05 | `05_seasonal_analysis.ipynb` | Monthly attendance and performance profiles, winter vs summer gap, year-on-year overlay |
| 06 | `06_sql_exploration.ipynb` | SQLite database; 6 queries using LAG, RANK, CTEs, CASE WHEN, correlated subqueries |
| 07 | `07_dashboard_prep.ipynb` | Enriched CSVs for the Streamlit dashboard: derived columns, performance bands, quarter start dates |
| 08 | `08_plotly_charts.ipynb` | Five interactive HTML charts (Plotly) — national trend, seasonal profile, regional box plot, volume scatter, band distribution |

---

## Processed Data Schemas

### `national_monthly.csv` — 85 rows × 22 columns
Monthly England-wide totals, April 2019 to April 2026.

Key columns: `period` (date), `type1_attendances`, `total_attendances`, `pct_4hr_type1`, `pct_4hr_all`, `dtoa_over_4hr`, `dtoa_over_12hr`. All percentage columns stored as decimals (0.0–1.0).

### `quarterly_by_provider.csv` — 5,062 rows × 30 columns
One row per trust per quarter, 2019-20 Q1 through 2024-25 Q4.

Key columns: `code` (ODS trust identifier), `name`, `region`, `icb_name`, `financial_year`, `quarter`, plus the same metrics as the national file at trust level.

---

## Further Work

A few things I'd want to add with more time:

- **Workforce data** — NHS England publishes quarterly staffing figures by trust (headcount and FTE by staff group). Joining that to the trust performance data on ODS code and quarter would let you test whether understaffing correlates with worse 4-hour performance. It's a separate download and a fair bit of extra cleaning, but it'd make the analysis more explanatory rather than just descriptive.
- **Delayed discharge data** — NHS England also publishes monthly delayed transfer of care figures. Linking those to the 12-hour trolley wait trend would help quantify how much of the back-door problem is driven by social care delays specifically, which is directly relevant for a local authority audience.
- **Longer time horizon** — the A&E time series goes back to 2010. Including pre-2019 data would show the full decline from the last time the 95% target was consistently hit (around 2014) and give more context to the COVID impact.
