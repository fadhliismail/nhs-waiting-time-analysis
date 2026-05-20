# NHS Accident and Emergency Waiting Times — Findings Report
## England, April 2019 to March 2025

*Based on NHS England open data: national monthly time series and quarterly trust-level returns.*
*Analysis covers six complete financial years across approximately 124 Type 1 (major Accident and Emergency) NHS trusts.*

---

## Table of Contents

1. About This Project
2. What We Are Studying
3. The 4-Hour Standard — The Headline Metric
4. Why We Are Interested in This Study
5. The Data Used in This Analysis
6. Analytical Questions — What We Were Looking For
7. What We Expected to Find — Going-In Hypotheses
8. Executive Summary
9. Finding 1 — National Attendance Trend
10. Finding 2 — National Performance Trend
11. Finding 3 — The Hidden Driver: 12-Hour Waits After Admission Decision
12. Finding 4 — Acuity — Are Patients Getting Sicker?
13. Finding 5 — Trust-Level Performance Variation
14. Finding 6 — Regional Variation
15. Finding 7 — Seasonal Patterns
16. Finding 8 — Local Focus: North West Anglia NHS Foundation Trust and Hinchingbrooke Hospital
17. Key Numbers for Interview Preparation
18. Narrative Summary

---

## 1. About This Project

This report is the output of an end-to-end data analysis project examining National Health Service Accident and Emergency performance across England from April 2019 to March 2025. The project spans six complete financial years: one pre-pandemic baseline year (the financial year 2019 to 2020), the COVID-19 disruption period (the financial year 2020 to 2021 and into the financial year 2021 to 2022), and the post-pandemic years in which the system has failed to recover (from the financial year 2022 to 2023 through the financial year 2024 to 2025).

A financial year in the United Kingdom National Health Service context runs from April of one calendar year to March of the next. So the financial year 2019 to 2020 covers April 2019 through March 2020. The financial year 2024 to 2025 covers April 2024 through March 2025. This convention matters because it affects how seasonal patterns are interpreted — the National Health Service winter pressure period (December through February) falls across the third and fourth quarters of any given financial year, not at the end of a calendar year.

The analysis carries a specific local angle alongside its national scope, with a focus on the Cambridgeshire and Peterborough Integrated Care Board area and North West Anglia National Health Service Foundation Trust, which runs Hinchingbrooke Hospital in Huntingdon. This geographic focus reflects the direct relevance of national Accident and Emergency performance data to local authority planning, particularly around social care commissioning and its effect on hospital discharge rates and patient flow.

The full analytical pipeline that underpins this report covers raw data loading and inspection, data cleaning and transformation, exploratory data analysis at the national level, trust-level performance variation analysis, seasonal pattern analysis, Structured Query Language-based querying using SQLite, and dashboard data preparation for an interactive Looker Studio report. Everything was built in Python using the pandas, NumPy, matplotlib, and seaborn libraries, together with SQLite for the database queries and Jupyter Notebooks as the working environment. All data used is real, publicly available National Health Service England open data. No proprietary data, no synthetic data, and no estimates have been used.

---

## 2. What We Are Studying

### The National Health Service Accident and Emergency System

National Health Service Accident and Emergency departments — known formally as Emergency Departments — are the front door to urgent hospital care in England. They handle everything from minor injuries to life-threatening emergencies. There are approximately 180 major Accident and Emergency departments in England, each attached to a National Health Service hospital trust, collectively seeing approximately 25 million attendances per year across all department types.

Understanding what goes on inside an Accident and Emergency department is important context for interpreting the performance data. When a patient arrives at a major Accident and Emergency, they are triaged — quickly assessed to determine how urgently they need attention. They then wait to be seen by a doctor or advanced nurse practitioner, who assesses them in detail, orders investigations such as blood tests or X-rays, and makes a clinical decision: send the patient home with or without further follow-up, refer them to another service, or admit them to a hospital ward for ongoing care. The 4-hour standard measures the time from arrival to this final decision and departure from the Accident and Emergency department.

### The Three Types of Accident and Emergency Department

Accident and Emergency departments in England are divided into three types, and this distinction is fundamental to interpreting the performance data correctly.

**Type 1 departments** are full, consultant-led emergency departments. These are the large, round-the-clock major Accident and Emergency departments that most people think of when they hear the phrase. They operate 24 hours a day, seven days a week, 365 days a year. They are staffed by emergency medicine consultants and specialty doctors and are equipped to handle the full range of emergencies: heart attacks, strokes, major trauma from road accidents, severe infections including sepsis, acute mental health crises, respiratory emergencies, and anything else that arrives through the door. Type 1 departments see the most complex, time-sensitive, and high-acuity cases in the National Health Service. The 4-hour standard applies primarily to Type 1 departments, and the performance percentage for Type 1 is the headline metric that politicians, journalists, and the public discuss when they talk about Accident and Emergency waiting times. This analysis focuses almost entirely on Type 1 performance.

**Type 2 departments** are single-specialty emergency departments. These serve a much narrower clinical scope than Type 1 — for example, an ophthalmic casualty unit seeing eye emergencies, or a dental emergency department. They handle lower volume and have a more predictable patient mix. They are not the subject of widespread performance concern and are not the focus of this analysis, though their attendance figures are included in the national totals where relevant.

**Type 3 departments** are Urgent Treatment Centres, Minor Injury Units, and Walk-In Centres. These see substantially higher volumes of patients than Type 2, but lower clinical acuity than Type 1. A patient with a sprained ankle, a minor cut requiring stitches, a urinary tract infection, or a minor respiratory illness would typically attend a Type 3 unit. They are not designed to handle emergencies of the severity seen in Type 1, and they operate with different staffing models — often nurse-led rather than consultant-led. The 4-hour target does not apply to Type 3 in the same regulatory way, and the performance figures for Type 3 are consistently higher than for Type 1, which reflects their lower case complexity rather than superior operational performance. When public debate focuses on Accident and Emergency performance, it is always Type 1 that is the concern.

### National Health Service Trusts

National Health Service hospital services in England are delivered by approximately 225 National Health Service Trusts. These are publicly funded statutory organisations established under the National Health Service Act that are responsible for providing acute hospital services in a defined geographic area. Each trust typically runs one or more hospitals, and each hospital may have multiple departments including an Accident and Emergency department.

Trusts are identified in the data by Organisation Data Service codes — three-letter alphanumeric identifiers assigned centrally by National Health Service England. For example, the Organisation Data Service code for North West Anglia National Health Service Foundation Trust, which runs Hinchingbrooke Hospital in Huntingdon, is RGN. The Organisation Data Service codes allow trusts to be consistently tracked across time even if their names change due to mergers or reconfigurations.

Trusts vary enormously in size, geography, patient demographics, and local health system context. A large urban teaching hospital such as University College London Hospitals, which serves a densely populated inner-city population with high levels of deprivation alongside a major trauma centre function, faces fundamentally different operational pressures from a rural district general hospital such as Hinchingbrooke, which serves a smaller, more dispersed population with different demand patterns and different social care system characteristics. The national average performance figure is a useful summary statistic but conceals this variation almost entirely. A central purpose of the trust-level analysis in this project is to move beyond the national average and understand where the system performs worst, where it performs least-worst, how broadly the failure is distributed, and how much the local trust deviates from the national picture.

### Integrated Care Boards

Since July 2022, National Health Service England has been organised into 42 Integrated Care Boards, which replaced the previous arrangement of Clinical Commissioning Groups. Integrated Care Boards are responsible for planning and commissioning health services for their local area. They sit structurally between National Health Service England nationally and the individual trusts locally. Each Integrated Care Board covers a geographic area broadly aligned with local authority boundaries.

The Integrated Care Board relevant to Huntingdonshire is the NHS Cambridgeshire and Peterborough Integrated Care Board. Understanding which Integrated Care Board covers a given trust is useful for contextualising local performance — the Integrated Care Board is responsible for system-level planning, including decisions about capacity, workforce, and the integration of health and social care.

### Hinchingbrooke Hospital — Local Context

Hinchingbrooke Hospital is a district general hospital located on the outskirts of Huntingdon, in Cambridgeshire. It serves a catchment area including Huntingdon, St Ives, St Neots, Ramsey, and surrounding villages — broadly the area administered by Huntingdonshire District Council.

Hinchingbrooke has a notable history that is worth mentioning as context for understanding its data. Between 2012 and 2015, it became the first National Health Service hospital in England to be managed by a private company, Circle Health, under a franchise agreement. That arrangement was terminated by Circle in 2015 when the hospital was declared to be in financial difficulty, and management returned to the National Health Service. The hospital subsequently became part of North West Anglia National Health Service Foundation Trust, which also runs Peterborough City Hospital. The merger means that trust-level data for Organisation Data Service code RGN reflects the combined performance of both hospitals — though Hinchingbrooke's Accident and Emergency is the primary acute site for Huntingdonshire residents.

---

## 3. The 4-Hour Standard — The Headline Metric

The 4-hour standard is the single most important performance metric in this analysis. It states that **95 percent of patients attending a Type 1 (major) Accident and Emergency department should be assessed, treated, and either admitted to a ward, transferred to another facility, or discharged home within four hours of their arrival.**

The target threshold is 95 percent. This means that a small proportion of patients — those with genuinely complex conditions requiring extended investigation or specialist consultation — are permitted to take longer than four hours without the department being recorded as failing the standard. The standard was introduced in 2004 under the National Health Service Plan as part of a broader package of waiting time targets designed to transform National Health Service performance. For approximately the first decade of the standard's existence, it was consistently met across England. National performance began to deteriorate around the financial year 2013 to 2014, as National Health Service funding growth fell behind demand growth, and it has not been consistently met at a national level since.

### Why Four Hours?

The four-hour threshold was chosen on the basis of clinical evidence suggesting that patients who wait longer than four hours in an Accident and Emergency department have significantly worse outcomes than those seen more quickly. The evidence pointed to higher rates of mortality, higher rates of hospital-acquired infections (because Accident and Emergency environments are not designed for prolonged patient stays and infection control is more difficult), increased rates of missed diagnoses due to cognitive fatigue in clinicians and deterioration in patients, and lasting psychological harm, particularly in elderly and vulnerable patients. The threshold was also chosen because it is operationally meaningful and measurable — it is long enough to allow a thorough clinical assessment for most presentations, and short enough to drive efficient patient flow through the department.

### Why This Metric Is a System-Wide Indicator

This is one of the most important conceptual points in the entire analysis, and it is frequently misunderstood in public discussion. The 4-hour standard isn't simply a measure of how well the Accident and Emergency department itself is functioning. It's a proxy for the functioning of the entire hospital system that the Accident and Emergency sits within — and beyond the hospital, for the functioning of the wider health and care system including social care.

When an Accident and Emergency department is failing the 4-hour standard, there are two broad categories of reason. The first is a front-door problem: too many patients are arriving, or the patients who are arriving are too complex, for the clinical team to assess and treat within four hours. The second, and far more common driver in recent years, is a back-door problem: patients who have been assessed and treated — who have, in effect, been clinically dealt with — cannot leave the Accident and Emergency because there is nowhere for them to go. If they need to be admitted, there is no ward bed available. If they need to be transferred, no capacity exists elsewhere. If they could go home, the social care package they need to be safe at home has not been arranged.

When large numbers of patients are stuck in the Accident and Emergency waiting for ward beds, those beds are occupied by people who do not need Accident and Emergency care — they need ward-level care, but they cannot get it because the wards are also full. The wards are full because they in turn contain patients who have been medically cleared for discharge but cannot leave because social care has not been commissioned to support them at home. This chain — from social care capacity to ward bed availability to Accident and Emergency flow to 4-hour performance — is the central causal mechanism behind the data presented in this report.

The 4-hour performance figure is therefore not primarily a measure of Accident and Emergency clinical quality. It is a measure of hospital system throughput, which is itself a measure of the whole health and care ecosystem including social care. This is why it connects so directly to local authority responsibilities.

### How This Metric Is Stored in the Data

In the raw National Health Service England data, all 4-hour performance figures are stored as decimal numbers between zero and one — not as percentages. A performance of 95 percent is stored as 0.95. A performance of 75 percent is stored as 0.75. Throughout this analysis, these decimal values have been converted to percentages for display (so 0.753 becomes 75.3 percent). The national target of 95 percent is therefore stored in the raw data as 0.95.

---

## 4. Why We Are Interested in This Study

There are three overlapping motivations for this project, each of which adds a layer of relevance.

### First Motivation: It Matters — This Is a Genuine Public Health Emergency

The National Health Service Accident and Emergency system is in the most prolonged and severe crisis in its history. Waiting time performance has been deteriorating since around 2013 and collapsed catastrophically during and in the immediate aftermath of the COVID-19 pandemic. In the financial year 2024 to 2025, the average patient attending a major Accident and Emergency in England experienced a wait of more than four hours four times in ten. In the worst-performing trusts, fewer than one in three patients were seen within the standard. More than half a million people per year waited more than 12 hours in an Accident and Emergency after a doctor had already made the decision to admit them to a ward — not because they had not yet been seen, but because there was no bed available for them to move to.

These are not abstract administrative figures. They represent real patients — many of them elderly, many of them with multiple complex conditions — waiting in environments that are not designed for prolonged stays, in corridors, on trolleys, in spaces that have inadequate toilet access, inadequate infection control, and inadequate monitoring capacity. There is robust clinical evidence linking extended Accident and Emergency waits to increased mortality: studies have found that patients waiting more than six hours in Accident and Emergency have measurably higher in-hospital death rates than those seen within the standard. The data in this project represents a genuine public health story with direct consequences for the health and wellbeing of the population.

The 4-hour target has been official government policy since 2004. That successive governments of different political parties have failed to meet their own declared standard is itself a significant fact, and one that data analysis can quantify and make visible in a way that media reporting alone cannot.

### Second Motivation: It Connects National Data to Local Government Responsibilities

Huntingdonshire District Council, like all English district councils, has responsibilities that connect directly to the performance of the local Accident and Emergency system. These connections are often invisible in public discussion, which tends to treat National Health Service performance and local government as entirely separate spheres. They are not.

The most direct connection is through social care. Local authorities in England are the responsible commissioner for adult social care services — domiciliary care (home care), residential care placements, supported living, and the assessment and care planning process that determines what support a person receives. When a patient is admitted to hospital and is subsequently medically cleared for discharge — meaning they no longer require acute inpatient medical care — they still need to get home safely. If they are an older person with mobility difficulties, dementia, or complex care needs, they cannot simply be discharged without a care package in place. Arranging that care package is the responsibility of the local authority social care department working in partnership with the National Health Service. If that package cannot be arranged quickly — because of a shortage of home care workers, a shortage of residential placements, or delays in the assessment process — the patient stays in a hospital bed they no longer need.

When patients occupy ward beds they do not medically need, those beds are unavailable for new admissions. Patients in the Accident and Emergency who need to be admitted cannot move to a ward. They wait in the Accident and Emergency, occupying trolley spaces, consuming nursing time, and blocking the flow of new patients through the department. The 4-hour performance figure falls.

This means that a local authority's decisions about social care funding, workforce development, and commissioning of home care capacity have a direct and quantifiable effect on the local Accident and Emergency's 4-hour performance. An analyst at Huntingdonshire District Council would be expected to understand this mechanism, to be able to identify it in the data, and to be able to communicate it to elected members and senior officers who are making those social care decisions.

The Decision-to-Admit wait data — discussed in detail in Finding 3 — is the specific metric in this dataset that makes this connection most visible. It isolates the exact patient group experiencing the back-door problem: those who have been clinically assessed, treated, and told they need a hospital bed, but cannot access one.

### Third Motivation: It Is a Technically Rich Analytical Problem

National Health Service Accident and Emergency data combines several properties that make it analytically rich and rewarding.

The data is real and publicly available. It has not been cleaned, simplified, or prepared for educational use. The raw Excel files have complex merged header rows, inconsistent column naming across years, decimal values mixed with dash characters to indicate absent data, and version differences that require specific handling (including a bug in a widely-used Python library that requires a one-line patch to load the two most recent quarterly files correctly). Working with this data requires genuine data engineering skill, not just the application of textbook techniques to a pre-prepared dataset.

The analytical questions reward genuine hypothesis-testing. The most obvious question — is demand driving performance decline? — has a clear, data-supported answer that contradicts the most common public narrative. Reaching that answer requires explicitly testing and ruling out the demand hypothesis, testing and ruling out the acuity hypothesis, and then identifying the actual driver in the Decision-to-Admit wait data. This is what analytical thinking looks like: not just describing the data, but using it to answer a question and revise an assumption.

The analysis operates at multiple levels of granularity. The national aggregate tells one story. The trust-level analysis tells a richer story about variation. The seasonal analysis tells a story about how the system's dynamics have changed over time. The local analysis connects the whole to a specific place and a specific set of policy decisions. Each level of analysis adds understanding that the others cannot provide alone.

The domain knowledge required is genuinely interesting. Understanding why the 4-hour metric is a system-wide indicator rather than just an Accident and Emergency indicator, understanding what a Decision-to-Admit wait is and why it matters, understanding the role of Organisation Data Service codes and Integrated Care Boards and the distinction between Type 1 and Type 3 departments — all of this domain knowledge makes the analysis more meaningful and the findings more credible.

---

## 5. The Data Used in This Analysis

All data in this project is publicly available from the National Health Service England website. No proprietary data, no confidential data, no estimates, and no synthetic data have been used at any point. The two datasets are described below.

### Dataset 1 — National Monthly Time Series

This is a single Excel file produced by National Health Service England covering monthly aggregate totals for all of England from August 2010 to April 2026. For this project, the April 2019 to April 2026 slice has been used — 85 monthly rows in total. The file has two sheets that are used in this analysis: the Activity sheet, which contains attendance and admission counts, and the Performance sheet, which contains the 4-hour performance percentages.

After loading, cleaning, and merging these two sheets, the national dataset has 85 rows and 22 columns. The key columns include:

- Monthly Type 1, Type 2, and Type 3 attendance counts, and a combined total
- Emergency admission counts broken down by department type and a combined total
- The Decision-to-Admit wait metrics: counts of patients waiting more than 4 hours and more than 12 hours after a decision to admit was made
- The 4-hour performance percentages for Type 1, Type 2, Type 3, and combined all-types

The period column — which represents the month — is stored as a date value (for example, 2019-04-01 representing April 2019). All percentage columns are stored as decimals.

### Dataset 2 — Quarterly Trust-Level Data (24 Files)

This is a set of 24 individual Excel files, one per financial year quarter, covering the financial year 2019 to 2020 Quarter 1 through the financial year 2024 to 2025 Quarter 4. Each file contains one row per National Health Service trust, with the same metrics as the national file but broken down at the individual trust level. Some trusts do not have a Type 1 department and therefore have blank or dash values in the Type 1 performance columns.

After loading all 24 files, cleaning each one, and concatenating them into a single combined dataset, the quarterly trust dataset has 5,062 rows and 30 columns. The key additional columns compared to the national dataset include:

- The Organisation Data Service code (three-letter trust identifier)
- The trust name
- The National Health Service England region
- The Integrated Care Board name
- The financial year label (for example, "2024-25")
- The quarter number (1 through 4)
- Breach counts for each department type, giving the number of patients who waited more than four hours

**Important technical notes about the raw data:**

All percentage columns are stored as decimal numbers, not percentages. A dash character in a percentage column means the trust has no department of that type, not that performance was zero — these dashes are converted to NaN (not a number) values during cleaning. Two specific files, covering the financial year 2024 to 2025 Quarter 3 and Quarter 4, trigger an assertion error in the xlrd library version 2.0.1, which is the Python library used to read older Excel formats. A one-line patch to the xlrd library source code is required to load these files correctly. The raw Excel files use two-row merged headers in the quarterly data, which pandas resolves by appending numerical suffixes to duplicate column names — these require explicit renaming during the cleaning step. One column in the Activity sheet has a column name that pandas reads as the Python float 0.95 rather than the string "0.95", because the header cell contains a number rather then text — this requires specific handling during cleaning.

---

## 6. Analytical Questions — What We Were Looking For

This project was structured around six core analytical questions. Stating these questions explicitly before the findings is important, because it frames the analysis as an inquiry — an attempt to answer specific questions using evidence — rather than simply a description of what the charts show.

**Question 1: What happened to national Accident and Emergency attendance and performance between April 2019 and March 2025?**

This is the broadest question and the foundation of the analysis. Before examining variation across trusts, regions, or seasons, we need to understand the national trajectory. What were the totals? What was the trend? What was the COVID-19 disruption? Has the system recovered? Without answering this question first, there is no baseline against which anything else can be evaluated.

**Question 2: Is the performance decline explained by rising demand?**

The most common public narrative about National Health Service Accident and Emergency is that more people are going to Accident and Emergency, and this increase in demand is responsible for longer waits. This hypothesis is easy to test by comparing the trend in attendance volumes with the trend in performance. If demand drove performance decline, attendance growth and performance decline should track proportionately — a given percentage increase in demand should produce a predictable decrease in performance. If attendance is broadly stable but performance is falling sharply, demand cannot be the primary driver and the explanation must lie elsewhere.

**Question 3: Are patients getting sicker — could increasing clinical complexity explain the performance decline?**

A more sophisticated version of the demand argument is that the same number of patients are arriving, but they are individually more acutely unwell or more clinically complex, requiring longer assessment and treatment times per patient. This would make the 4-hour standard harder to meet even if overall numbers were unchanged. The emergency admission rate — the proportion of Type 1 Accident and Emergency attendees who are subsequently admitted to a ward — serves as a proxy for patient acuity. If a higher proportion of attendees are sick enough to need admission, this suggests the patient population is becoming more complex. Tracking this rate over time tests the acuity hypothesis.

**Question 4: What does the Decision-to-Admit wait data reveal about the underlying cause of performance decline?**

The Decision-to-Admit metric measures a specific and diagnostically important subset of delays: patients who have been assessed and treated, for whom a clinical decision has been made that they need to be admitted to a hospital ward, but who are still waiting in the Accident and Emergency because no ward bed is available. These patients are not waiting to be seen. They are not waiting because the Accident and Emergency is slow at assessing them. They are waiting because the rest of the hospital is full. Tracking this metric separately from overall 4-hour performance tells us whether the crisis is primarily a front-door problem (the Accident and Emergency itself is overwhelmed) or a back-door problem (the rest of the hospital is full and patients cannot flow through).

**Question 5: How much does performance vary between individual trusts and between regions?**

The national average is a single number that represents none of the 124 individual trusts exactly. A nationwide crisis with uniform underperformance tells a fundamentally different story from a crisis concentrated in a small number of severely underperforming trusts. Understanding the distribution of performance matters for policy: if variation is wide, targeted intervention at the worst-performing trusts is the appropriate response. If variation is narrow and the problem is universal, systemic change is required. Identifying which trusts have declined the most — not just which are currently lowest, but which have fallen furthest from where they were — is more informative than a simple league table.

**Question 6: What are the seasonal patterns, and have they changed since the pandemic?**

Winter pressure is a recurring and well-established National Health Service phenomenon: demand for urgent care rises in winter, performance tends to dip, and this is widely discussed in media and policy circles. The question here is whether that seasonal dynamic is getting worse, getting better, or has changed in character. Has the winter dip deepened year on year? Or has the system deteriorated so comprehensively across all months that the seasonal signal is now smaller in relative terms, because the summer performance that used to provide a recovery period has also collapsed?

Running through all six of these questions is a local angle specific to the Huntingdonshire application context: how does North West Anglia National Health Service Foundation Trust — the trust running Hinchingbrooke Hospital in Huntingdon — compare to the national distribution, and what does its trajectory tell us about the public health and social care context in Huntingdonshire?

---

## 7. What We Expected to Find — Going-In Hypotheses

Before running any analysis, the following hypotheses were formed on the basis of publicly available information, media reporting, and general knowledge of the National Health Service. Stating these up front matters — it lets the findings be read as confirmations, revisions, or outright surprises rather than just conclusions that appeared from nowhere. Analytical honesty means acknowledging both what was expected and what caught us off guard.

**Hypothesis 1: Attendances would recover to pre-pandemic levels by 2021 to 2022, but performance would not recover at the same rate.**

Before the analysis, it was clear from media reporting that Accident and Emergency attendances had fallen sharply during the first COVID-19 lockdown in spring 2020, and had subsequently returned to something close to previous levels. The hypothesis was that this recovery in attendance volume would not be matched by a recovery in performance, because the factors that had driven performance decline before the pandemic — staffing shortages, bed pressures, social care discharge delays — would have been worsened by the pandemic and would take much longer to address. The expectation was that a gap between attendance trends and performance trends would be visible in the data.

This hypothesis was confirmed. Attendances recovered to pre-pandemic levels by the financial year 2021 to 2022 and have continued rising modestly since. Performance fell to its lowest point in the financial year 2022 to 2023 and has shown only marginal improvement since. The divergence between these two trends — demand up 6 percent, performance down 21 percentage points — is the central quantitative story of the national analysis.

**Hypothesis 2: The financial year 2020 to 2021 would show artificially elevated performance due to COVID-19 suppressing attendance demand.**

It was anticipated that the COVID-19 lockdowns would create a misleading improvement in 4-hour performance statistics. With fewer people attending Accident and Emergency, the departments would face less pressure, and a higher proportion of the reduced patient volume would be seen within four hours — not because the service had improved, but because the denominator had shrunk. The expectation was that treating 2020 to 2021 as a genuine high-water mark would be an analytical error.

This hypothesis was confirmed. The financial year 2020 to 2021 produced the highest average Type 1 performance in the dataset at 81.4 percent — well above the pre-pandemic baseline of 75.3 percent and well above the post-pandemic figures. But this was achieved with 22 percent fewer patients. The same staff, the same beds, and 3.5 million fewer patients per year will always produce better statistics. The financial year 2020 to 2021 is treated throughout this analysis as an exceptional outlier requiring annotation rather than as a meaningful data point in the performance trend.

**Hypothesis 3: Trust-level performance would vary meaningfully, and the national average would conceal significant differences between best and worst performers.**

It was expected that the national average performance figure would mask a wide spread between the best and worst trusts. Media reporting periodically highlights specific trusts with very poor performance, and it was reasonable to assume that the national figure was dragged down substantially by a subset of severely underperforming organisations.

This hypothesis was confirmed, but the extent of the variation was larger than anticipated. The range in performance across Type 1 trusts in the financial year 2024 to 2025 was from 34.3 percent (United Lincolnshire Hospitals National Health Service Trust) to 90.7 percent (Sheffield Children's National Health Service Foundation Trust) — a spread of 56.4 percentage points between the best and worst performer. The distribution was heavily skewed: 119 out of 124 trusts with Type 1 data were performing below 75 percent, which would have been considered severe underperformance in any pre-pandemic year.

**Hypothesis 4: Winter would be the worst performing season, with a meaningful recovery in summer months.**

The winter pressure narrative — higher demand in December through February driven by cold weather, respiratory illness, flu, and the frailty of older people — is deeply established in public discourse about National Health Service performance. The expectation was that performance would follow a clear seasonal cycle, dipping in winter and recovering toward the 4-hour target in summer, and that this cycle would be consistent and visible year on year.

This hypothesis was partially confirmed but produced the most analytically interesting surprise in the project. The winter dip is real — December and January are consistently the worst-performing months in every year of the dataset. However, the pre-COVID seasonal gap between summer and winter performance was 7.8 percentage points. The post-COVID seasonal gap is only 2.6 percentage points. This narrowing of the seasonal gap wasn't anticipated. It sounds like good news — like the winter dip has become smaller. It isn't good news. What has happened is that the summer floor has collapsed so far that there is now very little room left to fall in winter. The system no longer recovers between winters. Summer performance in the financial year 2024 to 2025 averaged approximately 60 percent — which would have been a crisis-level figure in any month in the financial year 2019 to 2020. The seasonal pattern hasn't improved. The system has become uniformly poor rather than seasonally poor.

**Hypothesis 5: Rising demand would be at least a contributing factor to performance decline.**

Even if demand growth was not the primary driver, it seemed reasonable to expect that the modest increase in Type 1 attendances — going from 15.8 million in the financial year 2019 to 2020 to 16.8 million in the financial year 2024 to 2025 — would contribute something to performance decline. A marginal increase in volume on a system already under strain should translate to some additional pressure.

This hypothesis was not confirmed in any meaningful sense. A 6 percent increase in demand against a 21 percentage point decrease in performance cannot be explained by demand even as a partial driver. The acuity proxy — the emergency admission rate — was also stable at 27 to 30 percent throughout the period, ruling out increasing patient complexity as an alternative demand-side explanation. Demand is not the story.

**Hypothesis 6: The Decision-to-Admit wait figures would show a worsening trend, reflecting growing pressure on ward capacity and social care discharge.**

Before the analysis, it was expected that Decision-to-Admit waits — the metric that directly measures the back-door problem — would have increased substantially as the pandemic created lasting structural damage to hospital flow. Delayed discharges, reduced bed capacity due to infection control requirements, and workforce depletion from COVID-19 were all expected to drive up the number of patients stuck waiting in Accident and Emergency for a ward bed.

This hypothesis was confirmed, but the scale of the increase was far beyond what was anticipated. The number of patients waiting more than 12 hours after a decision to admit increased from 12,435 in the financial year 2019 to 2020 to 532,451 in the financial year 2024 to 2025. This is a 43-fold increase over six years. In no way was a 43-fold increase anticipated. This single statistic is, in the view of this analysis, the most important number in the entire dataset. It isolates, precisely and quantitatively, the scale of the back-door problem — and it places the cause of the Accident and Emergency crisis clearly in the hospital system beyond Accident and Emergency itself.

---

## 8. Executive Summary

National Health Service Accident and Emergency performance collapsed in the financial year 2021 to 2022 and has not recovered. Accident and Emergency attendances returned to pre-pandemic levels by 2021 to 2022 and have continued rising, but the proportion of patients seen within the 4-hour standard fell from 75 percent in the financial year 2019 to 2020 to a low of 57 percent in the financial year 2022 to 2023, with only marginal improvement since. In the financial year 2024 to 2025, not a single Type 1 trust in England met the 95 percent target. The number of patients waiting more than 12 hours after a decision to admit them rose 43-fold between the financial year 2019 to 2020 and the financial year 2024 to 2025.

The data tells a clear story: demand volume is not the primary driver of the crisis. Attendances are only 6 percent above pre-pandemic levels, yet performance has fallen by 16 percentage points. The crisis is structural — driven by a combination of staffing pressures, hospital bed constraints, and the collapse of social care discharge pathways that leave admitted patients blocking Accident and Emergency beds while waiting for ward space that cannot be freed until social care takes patients home.

---

## 9. Finding 1 — National Attendance Trend

**Attendances recovered quickly after COVID-19 and have continued rising, but remain only modestly above pre-pandemic levels.**

| Financial Year | Type 1 Attendances | Compared to 2019 to 2020 |
|---------------|-------------------|--------------------------|
| 2019 to 2020  | 15,810,686        | Baseline                 |
| 2020 to 2021  | 12,287,286        | Minus 22 percent         |
| 2021 to 2022  | 16,137,559        | Plus 2 percent           |
| 2022 to 2023  | 16,202,978        | Plus 2.5 percent         |
| 2023 to 2024  | 16,525,835        | Plus 4.5 percent         |
| 2024 to 2025  | 16,763,266        | Plus 6 percent           |

The COVID-19 disruption to attendance is clearly visible in this data. April 2020 — the first full month of the first national lockdown — saw just 689,720 Type 1 attendances, which is approximately 40 percent of the volume of a typical pre-pandemic month. The public health messaging to avoid hospitals unless absolutely necessary, the fear of COVID-19 transmission in healthcare settings, and the cancellation of elective pathways that might otherwise generate Accident and Emergency attendance all contributed to this dramatic suppression of demand.

Attendance recovered faster than many observers expected. By the financial year 2021 to 2022, Type 1 attendances across England had returned to above pre-pandemic levels at 16.1 million. This was the first full year after COVID-19 restrictions were substantially lifted in the summer of 2021. By the financial year 2024 to 2025, the annual total had risen to 16.8 million — the highest in this dataset, and 6 percent above the pre-pandemic baseline.

The critical analytical point is this: a 6 percent increase in demand across six years cannot explain a 21 percentage point fall in the proportion of patients seen within four hours. If the same number of staff with the same number of beds and the same operational processes were handling 6 percent more patients, one might expect a very modest deterioration in performance — perhaps 1 to 2 percentage points at most, and even that would depend on whether the system was already operating at or near capacity. The actual deterioration is more than ten times larger than demand growth could plausibly account for. Demand is not the explanation for the performance collapse.

This finding is worth establishing early, because the demand narrative is the default public explanation for NHS A&E problems. It's easy to say "more people are going to A&E" and leave it there. The data doesn't support this explanation as more than a marginal contributing factor.

---

## 10. Finding 2 — National Performance Trend

**The 4-hour standard has collapsed and shows no meaningful recovery.**

| Financial Year | Average Type 1 4-Hour Performance | Change in Percentage Points |
|---------------|----------------------------------|----------------------------|
| 2019 to 2020  | 75.3 percent                     | Baseline                    |
| 2020 to 2021  | 81.4 percent                     | Plus 6.1 percentage points  |
| 2021 to 2022  | 66.1 percent                     | Minus 15.3 percentage points|
| 2022 to 2023  | 56.7 percent                     | Minus 9.4 percentage points |
| 2023 to 2024  | 58.2 percent                     | Plus 1.4 percentage points  |
| 2024 to 2025  | 59.3 percent                     | Plus 1.2 percentage points  |

Four distinct phases are visible in this trajectory.

### Phase 1 — The Pre-Pandemic Baseline (Financial Year 2019 to 2020)

The baseline year of 75.3 percent is itself a failing figure by the government's own standard. The 95 percent target had not been met nationally in any financial year since approximately 2013 to 2014. The financial year 2019 to 2020 represents normal — but normal was already broken. This matters because it means the COVID-19 pandemic did not create the crisis from a standing start; it severely worsened a system that was already struggling.

Even at 75.3 percent nationally, the best month in the baseline year — May 2019 at 79.1 percent — was still nearly 16 percentage points below the 95 percent target. The National Health Service was not hovering just below its own target in 2019. It was falling well short of it, at a system-wide level, even before any pandemic pressure.

### Phase 2 — The COVID-19 Artefact (Financial Year 2020 to 2021)

The 81.4 percent national average in the financial year 2020 to 2021 is the highest figure in the dataset but should not be interpreted as a genuine improvement. It is a statistical artefact produced by the suppression of demand during the COVID-19 lockdowns. Approximately 3.5 million fewer patients attended Type 1 Accident and Emergency departments in that year compared to the pre-pandemic baseline. The same clinical staff, working with the same number of beds, handled a dramatically reduced patient volume. Naturally, a higher proportion of that reduced volume was processed within four hours.

It's a bit like saying a motorway is performing well because there are very few cars on it during a heavy snowstorm that has kept drivers at home. The road's underlying capacity hasn't improved. The moment normal traffic returns, the same congestion will appear — or worse congestion, if the snowstorm has damaged the road surface while traffic was absent. The financial year 2020 to 2021 should be treated throughout any analysis of this data as an exceptional year requiring specific annotation. It does not represent a genuine trajectory data point.

### Phase 3 — The Catastrophe (Financial Years 2021 to 2022 and 2022 to 2023)

The minus 15.3 percentage point fall in the financial year 2021 to 2022 is the single largest annual decline in this dataset and is the pivotal event in the entire performance trajectory. In the financial year 2021 to 2022, COVID-19 restrictions were progressively lifted. Patients who had avoided Accident and Emergency during the pandemic — some of whom had allowed conditions to worsen during their absence — returned. Attendance volumes surged back to and above pre-pandemic levels in the same financial year. The system was simultaneously dealing with an enormous backlog of deferred care across the whole of the National Health Service, workforce depletion from COVID-19 illness and long-COVID, infection control requirements that reduced bed capacity in many wards, and the structural collapse of social care discharge pathways that had been deteriorating before the pandemic and had been further damaged by it.

The system could not absorb the returning demand. The 15.3 percentage point fall — from 81.4 percent in the COVID year to 66.1 percent — represents the moment that the artificial COVID-era improvement unwound all at once. The financial year 2022 to 2023 continued the decline, falling a further 9.4 percentage points to 56.7 percent. December 2022 was the worst single month in the dataset at 49.6 percent — fewer than half of patients at a major Accident and Emergency were seen within four hours.

### Phase 4 — Flatline (Financial Years 2023 to 2024 and 2024 to 2025)

The modest improvements of plus 1.4 percentage points in the financial year 2023 to 2024 and plus 1.2 percentage points in the financial year 2024 to 2025 are real but need to be put in context. At an improvement rate of approximately 1.3 percentage points per year, reaching the 95 percent target would take approximately 27 years. The system hasn't recovered. It's found a new, much lower equilibrium at approximately 59 percent. Performance has stabilised at a catastrophically low level, not recovered toward the target.

---

## 11. Finding 3 — The Hidden Driver: 12-Hour Waits After Admission Decision

**This is one of the most important findings in the entire dataset, and one that receives far less public attention than the headline 4-hour figure.**

The Decision-to-Admit wait metric measures the following very specific situation: a patient has arrived at an Accident and Emergency, has been triaged, has been assessed by a clinician, has undergone investigation, and has been told by a doctor that they need to be admitted to a hospital ward. The decision has been made. The medical work in the Accident and Emergency is complete. The patient is now waiting — not for clinical attention, but for a physical bed in a ward to become available. The Decision-to-Admit wait clock measures how long that wait is. The 12-hour threshold identifies patients who waited more than 12 hours in the Accident and Emergency after the admission decision was made.

| Financial Year | Patients Waiting More Than 12 Hours After Admission Decision | Change Compared to 2019 to 2020 |
|---------------|-------------------------------------------------------------|--------------------------------|
| 2019 to 2020  | 12,435                                                      | Baseline                       |
| 2020 to 2021  | 14,150                                                      | Plus 14 percent                |
| 2021 to 2022  | 98,564                                                      | Plus 693 percent               |
| 2022 to 2023  | 410,092                                                      | Plus 3,200 percent             |
| 2023 to 2024  | 439,411                                                      | Plus 3,434 percent             |
| 2024 to 2025  | 532,451                                                      | Plus 4,184 percent             |

This is a 43-fold increase over six years. In the financial year 2024 to 2025, more than half a million patients waited more than 12 hours in a major Accident and Emergency after being told they needed a bed. That is approximately 1,460 patients every single day of the year.

### Why This Statistic Is the Most Diagnostically Important Number in the Dataset

The headline 4-hour performance figure tells us that the system is failing, but it does not tell us specifically why it is failing. It could be failing because Accident and Emergency departments are slow to assess and treat patients — a front-door problem. Or it could be failing because patients who have been assessed and treated cannot leave the Accident and Emergency to go to a ward — a back-door problem. The Decision-to-Admit wait separates these two explanations. A patient counted in the Decision-to-Admit wait has, by definition, been seen, assessed, and treated. Their wait is not a clinical failure in the Accident and Emergency. It is a capacity failure in the hospital and the wider care system.

The 43-fold increase in 12-hour Decision-to-Admit waits is the clearest quantitative evidence available that the Accident and Emergency crisis is primarily a back-door problem. These patients have been clinically managed. The Accident and Emergency has done its job. The failure lies in the inability of the rest of the system to absorb them.

### The Chain of Causation

Understanding why ward beds are unavailable requires tracing back through the chain of causation. Hospital wards are full because they contain patients who have been assessed as medically fit for discharge — patients who do not require acute inpatient care — but who cannot be discharged. These patients cannot go home because no social care package is in place to support them safely in the community. Arranging that package — whether it is home care visits, a residential care placement, equipment for the home, or a supported living arrangement — is a process that involves the local authority social care department, the National Health Service community teams, and independent care providers. When that process is slow, underfunded, or simply unable to source the required care because there is a shortage of care workers or residential placements, the patient stays in the hospital bed they no longer medically need.

In the financial year 2024 to 2025, the number of patients in National Health Service hospital beds who were medically fit for discharge but could not go home because social care was not in place regularly exceeded 13,000 at any given point in time. Each of those patients was occupying a bed that could otherwise have taken a patient from the Accident and Emergency who needed admission. Each Accident and Emergency patient waiting for admission was contributing to the Decision-to-Admit wait total and to the failure of the 4-hour standard.

### The Direct Relevance to Huntingdonshire District Council

The Decision-to-Admit wait explosion is not an abstract national statistic from the perspective of a local authority officer. It is a direct consequence of decisions about social care funding, social care commissioning, and social care workforce that are made at local authority level. When Huntingdonshire District Council commissions home care services — the domiciliary care visits that allow a person to live at home with support — the volume, quality, and responsiveness of those services determines how quickly hospital patients can be safely discharged. When social care capacity is insufficient to absorb hospital discharges at the pace required, the consequences appear in this data as Decision-to-Admit waits.

A data analyst at Huntingdonshire District Council would be expected to understand this causal chain and to be able to make it visible in data, both to support internal planning and to communicate it to elected members, partners in the National Health Service, and the public. The 43-fold increase in 12-hour Decision-to-Admit waits is a number worth knowing.

---

## 12. Finding 4 — Acuity: Are Patients Getting Sicker?

**The available evidence suggests patients are not systematically sicker. Increasing clinical complexity does not explain the performance decline.**

One alternative and analytically important hypothesis for the performance collapse is that the patients attending major Accident and Emergency departments have become more acutely unwell, more clinically complex, or more dependent on investigation-heavy pathways — and that this increase in clinical complexity, rather than capacity failure, is what makes the 4-hour standard harder to meet. If each patient requires more time and more clinical resource, then even a stable number of attendances could produce longer waits and worse performance.

This hypothesis is tested using the emergency admission rate — the proportion of Type 1 Accident and Emergency attendees who are subsequently admitted to a hospital ward as an emergency. Emergency admission is not a perfect measure of acuity — some admitted patients are admitted for relatively straightforward conditions, and some non-admitted patients are genuinely unwell but can be safely managed in the community. However, as a rough proxy for the overall clinical complexity of the Accident and Emergency patient population, it is the best measure available in this dataset.

| Financial Year | Type 1 Emergency Admission Rate |
|---------------|--------------------------------|
| 2019 to 2020  | 30.0 percent                   |
| 2020 to 2021  | 33.5 percent                   |
| 2021 to 2022  | 28.3 percent                   |
| 2022 to 2023  | 27.0 percent                   |
| 2023 to 2024  | 28.5 percent                   |
| 2024 to 2025  | 28.6 percent                   |

The admission rate has remained broadly stable throughout the six-year period, oscillating in the range of 27 to 30 percent. The financial year 2020 to 2021 spike to 33.5 percent is readily explained: during COVID-19 lockdowns, the public health messaging to avoid hospitals meant that many people with minor and moderate conditions did not attend. Those who did attend tended to be more seriously unwell, with conditions that could not reasonably be managed at home. As a result, a higher proportion of the reduced attendance volume required admission. This is a selection effect, not evidence of a population-level change in acuity. Once restrictions lifted and attendance volumes normalised, the admission rate returned to the pre-pandemic range.

**The conclusion from this analysis is that the acuity hypothesis is not supported by the data.** Patients are not systematically sicker. The volume and complexity of work arriving at major Accident and Emergency departments has remained roughly constant in terms of the proportion requiring admission. The problem is not that the incoming work has increased in difficulty. The problem is that the system's capacity to process and discharge that work has deteriorated — the front door is no more difficult; the back door is blocked.

---

## 13. Finding 5 — Trust-Level Performance Variation

**The national average of 59 percent in the financial year 2024 to 2025 conceals enormous variation between individual trusts. The problem is nearly universal but is not uniformly severe.**

### The Distribution of Performance Across Trusts in the Financial Year 2024 to 2025

There were 124 National Health Service trusts with Type 1 Accident and Emergency data in the financial year 2024 to 2025 — meaning trusts that reported Type 1 attendances and 4-hour performance for at least one quarter in that year.

| Performance Band | Number of Trusts | Percentage of All Trusts |
|-----------------|-----------------|--------------------------|
| 95 percent or above (at the national target) | 0 | 0 percent |
| 85 to 94 percent | 1 | 0.8 percent |
| 75 to 84 percent | 4 | 3.2 percent |
| Below 75 percent (severe underperformance) | 119 | 95.9 percent |

Not one of England's 124 major Accident and Emergency trusts met the 95 percent target in the financial year 2024 to 2025. This is a remarkable fact. The government's formal performance standard for the National Health Service — a standard that has been in place since 2004 — was met by zero of the organisations responsible for delivering it.

The best-performing Type 1 trust in England in the financial year 2024 to 2025 was Sheffield Children's National Health Service Foundation Trust, averaging 90.7 percent across the year. It is worth noting that Sheffield Children's is a specialist paediatric hospital rather than a district general hospital. Its patient population is children and young people, its case mix is different from a general adult emergency department, and some of its operational characteristics — including patient behaviour in terms of attendance patterns — are different from a typical district general. It approaches the target more closely than any other Type 1 trust, but it is arguably not comparable on a like-for-like basis to the vast majority of trusts in this dataset. Even so, 90.7 percent is 4.3 percentage points below the 95 percent standard.

The worst-performing Type 1 trust in England in the financial year 2024 to 2025 was United Lincolnshire Hospitals National Health Service Trust, averaging 34.3 percent across the year. This means that in the organisation responsible for providing major Accident and Emergency care across Lincolnshire — a large, predominantly rural county — fewer than one in three patients were seen within four hours during the financial year 2024 to 2025. This is not a statistical blip or a temporarily poor quarter. It is a sustained average across a full year.

The gap between the best-performing general trust and the worst-performing trust in the financial year 2024 to 2025 is more than 56 percentage points. This is an extraordinary level of variation for a national public service with a single declared performance standard.

### Comparison with the Financial Year 2019 to 2020

In the pre-pandemic baseline year of 2019 to 2020, 120 trusts had Type 1 data. Of those, 1 trust met the 95 percent target. The national average was 76.0 percent. The fact that only 1 trust met the target even in the pre-pandemic period underlines a point made in the trajectory analysis: the crisis predates the pandemic. The financial year 2019 to 2020 was not a successful year against the 95 percent standard. It was a year in which the system was already failing comprehensively to meet its own declared target. COVID-19 did not create the crisis; it accelerated and entrenched a pre-existing failure.

### The Five Trusts That Declined the Most Between the Financial Year 2019 to 2020 and the Financial Year 2024 to 2025

Identifying the trusts that declined the most in percentage point terms — not simply those with the lowest absolute performance in 2024 to 2025 — is a more analytically useful question than a simple league table. A trust that has always performed poorly tells a different story from one that used to perform well and has collapsed. The biggest decliners are the trusts where something specifically went wrong, or where a pre-existing structure was particularly vulnerable to the post-pandemic pressures.

The five trusts that fell the furthest between the financial year 2019 to 2020 and the financial year 2024 to 2025 are:

**South Tees Hospitals National Health Service Foundation Trust** — fell from 83.3 percent in the financial year 2019 to 2020 to 48.5 percent in the financial year 2024 to 2025, a decline of 34.8 percentage points. South Tees runs James Cook University Hospital in Middlesbrough, a large regional hospital serving Teesside and parts of County Durham and North Yorkshire.

**Countess of Chester Hospital National Health Service Foundation Trust** — fell from 79.8 percent in the financial year 2019 to 2020 to 46.0 percent in the financial year 2024 to 2025, a decline of 33.7 percentage points. This trust runs the Countess of Chester Hospital, the main acute hospital for Chester and the surrounding area of west Cheshire.

**Western Sussex Hospitals National Health Service Foundation Trust** — fell from 89.2 percent in the financial year 2019 to 2020 to 58.3 percent in the financial year 2024 to 2025, a decline of 30.8 percentage points. This trust runs Worthing Hospital and Southlands Hospital in West Sussex. The pre-pandemic performance of 89.2 percent — one of the higher figures in the pre-pandemic dataset — makes the subsequent collapse particularly striking.

**Gateshead Health National Health Service Foundation Trust** — fell from 86.3 percent in the financial year 2019 to 2020 to 55.5 percent in the financial year 2024 to 2025, a decline of 30.8 percentage points. Gateshead runs the Queen Elizabeth Hospital in Gateshead, Tyne and Wear.

**The Newcastle Upon Tyne Hospitals National Health Service Foundation Trust** — fell from 89.6 percent in the financial year 2019 to 2020 to 60.1 percent in the financial year 2024 to 2025, a decline of 29.5 percentage points. This is one of England's largest and most prestigious teaching hospital trusts, running the Royal Victoria Infirmary and Freeman Hospital in Newcastle.

None of these were failing trusts in the financial year 2019 to 2020. Most were performing above the national average. Several were approaching the 90 percent level which, while still below target, represented genuinely good performance relative to peers. Their dramatic subsequent decline reflects local conditions — specific staffing pressures, social care discharge challenges, hospital configuration issues, or geographical factors — operating on top of the national deterioration. Identifying these trusts and understanding their trajectories is the kind of analysis that moves beyond headline statistics into genuine diagnostic insight.

---

## 14. Finding 6 — Regional Variation

**All seven National Health Service England regions underperform against the 95 percent target. The regional spread is meaningful but narrower than the trust-level spread.**

**Average Type 1 4-Hour Performance by Region, Financial Year 2024 to 2025:**

| Rank | Region | Average Performance |
|------|--------|-------------------|
| 1 | National Health Service England South East | 63.2 percent |
| 2 | National Health Service England London | 60.6 percent |
| 3 | National Health Service England North East and Yorkshire | 60.0 percent |
| 4 | National Health Service England Midlands | 58.6 percent |
| 5 | National Health Service England East of England | 58.5 percent |
| 6 | National Health Service England South West | 56.8 percent |
| 7 | National Health Service England North West | 55.9 percent |

The spread between the best-performing region, the South East at 63.2 percent, and the worst-performing region, the North West at 55.9 percent, is 7.3 percentage points. This is a real and non-trivial difference — the South East is performing approximately 13 percent better in relative terms than the North West. However, the regional spread of 7.3 percentage points is dramatically smaller than the trust-level spread of 56 percentage points. Regional averages smooth out the extremes by aggregating many trusts together, and the result is that all seven regions look broadly similar compared to the variation between individual trusts.

This matters for how the data should be interpreted. If you were to conclude from the regional analysis alone that England's Accident and Emergency performance is relatively uniform, with regions clustered within a 7-point range, you would be missing the much wider variation underneath. Within any given region, the best and worst individual trusts may differ by 30 to 40 percentage points or more.

**The South East region** performing best at 63.2 percent is notable but should not be interpreted as the South East having a particularly well-functioning system — 63.2 percent is still 32 percentage points below the 95 percent target. The South East includes some relatively high-performing trusts alongside others that underperform significantly.

**The North West region** performing worst at 55.9 percent reflects persistent pressures in several of its constituent trusts. The North West contains some of England's most deprived communities, particularly in Greater Manchester, Liverpool, and parts of Lancashire, which typically generate higher Accident and Emergency demand and present with more complex social care discharge challenges.

**The East of England region**, which contains North West Anglia National Health Service Foundation Trust and therefore serves the Huntingdonshire population, sits fifth out of seven at 58.5 percent — essentially at the national average of 59.0 percent. The East of England is neither an outlier performing substantially above the national picture nor one performing substantially below it. This contextualises the local trust's performance: Hinchingbrooke Hospital sits within a region that is broadly average, within a national system that is comprehensively failing its own target.

---

## 15. Finding 7 — Seasonal Patterns

### The Nature of the Seasonal Pattern

Accident and Emergency performance has always shown some seasonal variation, and this variation is expected and well understood. Winter brings cold weather, which worsens respiratory conditions and increases falls among elderly people. Seasonal influenza peaks in December and January, generating both direct Accident and Emergency attendances and significant inpatient admissions that then affect the flow of patients through the wider hospital. The combination of higher demand and reduced capacity — staff sickness from winter illnesses affects all healthcare settings — produces the well-known winter dip in Accident and Emergency performance.

However, the conventional understanding of winter pressure assumes that the system recovers in spring and summer. The summer months have historically provided a recovery period: lower demand, better staff health, fewer respiratory emergencies. The pre-COVID data confirms this pattern — summer months consistently produced better performance than winter months.

The question this analysis set out to answer is whether this seasonal dynamic has changed since the pandemic.

### Seasonal Attendance Variation

Type 1 Accident and Emergency attendances do show seasonal variation, but it is more modest than the seasonal variation in performance. The swing between the highest-demand and lowest-demand calendar months is approximately 5 to 10 percent. December and January tend to be slightly busier months in terms of attendance, but the difference compared to quieter months such as May and September is not large enough to explain the magnitude of the performance dip seen in those months.

This is an important contextual point: if winter attendance were dramatically higher than summer attendance — if, for example, January saw double the attendances of August — then the performance dip in January might be expected on capacity grounds alone. But the data does not show this. Seasonal demand variation in Accident and Emergency is a real but modest phenomenon. It is not large enough to drive the seasonal performance variation observed.

### The Surprising Finding — The Seasonal Gap Has Narrowed

| Period | Average Performance, Summer Months (June, July, August) | Average Performance, Winter Months (December, January, February) | Seasonal Gap |
|--------|--------------------------------------------------------|------------------------------------------------------------------|-------------|
| Pre-COVID (financial year 2019 to 2020) | 78.7 percent | 70.9 percent | 7.8 percentage points |
| Post-COVID (October 2021 to March 2025) | 59.8 percent | 57.2 percent | 2.6 percentage points |

The seasonal gap — the difference between summer and winter average performance — has shrunk from 7.8 percentage points in the pre-pandemic period to 2.6 percentage points in the post-pandemic period. At first reading, this sounds like an improvement: the winter dip has become smaller relative to summer performance. This interpretation is incorrect.

What has actually happened is that the summer performance floor has collapsed to such a low level that there is no longer much room left to fall further in winter. In the pre-pandemic financial year 2019 to 2020, summer performance averaged 78.7 percent — well below the 95 percent target, but a meaningful recovery from the winter low of 70.9 percent. In the post-COVID period, summer performance averages 59.8 percent. This is approximately the same level at which winter performance used to sit before the pandemic. Winter performance post-COVID averages 57.2 percent — only 2.6 percentage points lower than summer.

The system is no longer recovering between winters. The capacity that used to become available in summer — as respiratory demand fell, staff health improved, and demand moderated — is no longer sufficient to drive a meaningful performance improvement. Year-round pressures, including persistent bed-blocking due to social care discharge delays, ward staffing vacancies, and infrastructure constraints, are suppressing performance in all seasons, not just winter.

**The key take-away from the seasonal analysis:** the NHS A&E crisis is no longer primarily a winter pressure story. It's a year-round structural capacity and flow failure that happens to have a modest seasonal modulation on top. Addressing this through winter preparedness measures alone — surge capacity, additional beds opened for winter, extra staffing during peak winter months — is necessary but not sufficient. The underlying structural problems that suppress performance in summer must also be addressed.

---

## 16. Finding 8 — Local Focus: North West Anglia National Health Service Foundation Trust and Hinchingbrooke Hospital

### About the Trust

North West Anglia National Health Service Foundation Trust is an acute hospital trust operating in Cambridgeshire and surrounding areas. Its principal hospitals are Hinchingbrooke Hospital in Huntingdon and Peterborough City Hospital. The trust's Organisation Data Service code is RGN. It sits within the National Health Service Cambridgeshire and Peterborough Integrated Care Board area and serves the populations of Huntingdonshire, Peterborough, and parts of neighbouring districts.

The trust's Accident and Emergency data in this analysis refers to the combined Type 1 performance across its sites. For the purposes of this project, RGN is the local trust serving the population of Huntingdonshire and is therefore the specific organisation of most direct relevance to Huntingdonshire District Council.

### Full Performance History by Quarter

The table below shows North West Anglia's Type 1 4-hour performance for every quarter across all six financial years in the dataset. Each quarter runs for three calendar months: Quarter 1 covers April through June, Quarter 2 covers July through September, Quarter 3 covers October through December, and Quarter 4 covers January through March.

| Financial Year | Quarter 1 | Quarter 2 | Quarter 3 | Quarter 4 | Annual Average |
|---------------|-----------|-----------|-----------|-----------|----------------|
| 2019 to 2020  | 77.3%     | 77.2%     | 70.7%     | 74.0%     | **74.8%**      |
| 2020 to 2021  | 97.1%     | 84.3%     | 73.7%     | 72.8%     | **82.0%**      |
| 2021 to 2022  | 72.3%     | 49.7%     | 49.8%     | 44.2%     | **54.0%**      |
| 2022 to 2023  | 43.0%     | 44.5%     | 47.5%     | 53.6%     | **47.2%**      |
| 2023 to 2024  | 56.3%     | 58.8%     | 49.1%     | 54.4%     | **54.7%**      |
| 2024 to 2025  | 58.6%     | 64.2%     | 55.2%     | 57.3%     | **58.8%**      |

Several features of this trajectory are worth examining in detail.

**The financial year 2019 to 2020 baseline** shows North West Anglia performing at approximately 74.8 percent — slightly below the national average of 75.3 percent for that year. The trust's seasonal pattern is visible: Quarter 3 (October through December) was the weakest quarter at 70.7 percent, reflecting the onset of winter pressure.

**The financial year 2020 to 2021 COVID artefact** is dramatic for this trust. Quarter 1 of the financial year 2020 to 2021 — covering April through June 2020, the first full quarter under COVID-19 lockdown — produced a performance of 97.1 percent. This is the only quarter in the entire dataset for any trust in which North West Anglia met or exceeded the 95 percent target. It was achieved with attendance at Hinchingbrooke falling to approximately 70 percent of normal levels during that period. As demand recovered through the remaining quarters of that financial year, performance fell back toward and below pre-pandemic levels.

**The financial year 2021 to 2022 collapse** is the most striking feature of this trust's trajectory. Quarter 2 of that year — July through September 2021 — shows performance falling to 49.7 percent, and Quarter 4 — January through March 2022 — reached 44.2 percent. The trust fell from a COVID-inflated 82.0 percent annual average to 54.0 percent in a single year. This mirrors the national picture but illustrates how rapidly and severely local conditions deteriorated once COVID-19 restrictions were lifted.

**The financial year 2022 to 2023** shows the trust reaching its lowest annual average at 47.2 percent — fewer than half of patients seen within four hours across the whole year. Quarter 1 of that year, covering April through June 2022, saw performance fall to 43.0 percent. This is a level of sustained underperformance that, in any pre-pandemic context, would have triggered formal regulatory intervention by National Health Service England.

**The financial years 2023 to 2024 and 2024 to 2025** show a gradual improvement — from an annual average of 54.7 percent to 58.8 percent. The improvement is welcome and real, but it is very modest. The trust remains more than 36 percentage points below the 95 percent target even after two consecutive years of improvement.

### North West Anglia in National Context

In the financial year 2024 to 2025, North West Anglia averaged 58.8 percent on Type 1 4-hour performance. The national average for all Type 1 trusts was 59.0 percent and the national median was 58.8 percent. North West Anglia sits at the 50th percentile of all Type 1 trusts nationally — precisely at the middle of the distribution.

This has two implications that are worth stating plainly.

The first implication is that North West Anglia is not an unusually poor performer. It is not a trust that is failing to a degree significantly worse than its peers. Its performance reflects the national picture accurately. A narrative that frames Hinchingbrooke as a uniquely struggling hospital would not be supported by this data.

The second and more important implication is that being average in 2024 to 2025 means performing at a level that would have been considered an exceptional failure in any pre-pandemic year. The 50th percentile nationally in 2024 to 2025 is 58.8 percent. Half of England's Type 1 trusts perform worse than this. But 58.8 percent means that 4 in 10 patients at this trust are not seen within four hours — a standard that the government's own policy says should apply to only 5 in 100. Mediocrity in a broken system is still broken.

### The Connection to Huntingdonshire District Council's Responsibilities

For an analyst or officer at Huntingdonshire District Council, the North West Anglia data is not just a number to note. It is a data point that connects to decisions the council makes.

The 12-hour Decision-to-Admit wait explosion — from 12,435 nationally in the financial year 2019 to 2020 to 532,451 in the financial year 2024 to 2025 — is driven substantially by delayed hospital discharges waiting for social care. North West Anglia's catchment area falls within Cambridgeshire, where adult social care is the responsibility of Cambridgeshire County Council working in partnership with the district councils including Huntingdonshire. The commissioning, quality, and responsiveness of home care services in Huntingdonshire is a direct input into the speed at which patients can be discharged from Hinchingbrooke and Peterborough City Hospitals — and therefore a direct input into the 4-hour performance figures shown in this table.

A council analyst who understands this connection — who can show, using data, that social care discharge rates connect to Accident and Emergency performance, and who can communicate this to elected members and National Health Service partners — adds a dimension of analytical value that goes beyond technical competence into genuine public service impact.

---

## 17. Key Numbers for Interview Preparation

The following are the most analytically significant statistics from this project, presented in a form suitable for recall and use in a job interview or presentation context.

| What the Statistic Measures | The Number |
|----------------------------|-----------|
| Type 1 attendances in the financial year 2019 to 2020 (the pre-pandemic baseline) | 15,810,686 |
| Type 1 attendances in the financial year 2024 to 2025 | 16,763,266 — which is 6 percent above the pre-pandemic baseline |
| National average Type 1 4-hour performance in the financial year 2019 to 2020 | 75.3 percent |
| National average Type 1 4-hour performance in the financial year 2024 to 2025 | 59.3 percent — a fall of 16 percentage points over the same period that demand rose 6 percent |
| The largest single-year decline in performance | Minus 15.3 percentage points in the financial year 2021 to 2022 — when COVID-19 restrictions lifted and demand rebounded faster than capacity could respond |
| The worst single month in the dataset | December 2022 at 49.6 percent — fewer than half of patients seen within four hours |
| Number of Type 1 trusts meeting the 95 percent target in the financial year 2024 to 2025 | Zero out of 124 |
| Number of Type 1 trusts performing below 75 percent in the financial year 2024 to 2025 | 119 out of 124, which is 95.9 percent of all trusts |
| Patients waiting more than 12 hours after a decision to admit in the financial year 2019 to 2020 | 12,435 |
| Patients waiting more than 12 hours after a decision to admit in the financial year 2024 to 2025 | 532,451 — an increase of 4,184 percent, or 43 times the baseline figure |
| Pre-pandemic seasonal gap in performance (summer months versus winter months) | 7.8 percentage points |
| Post-pandemic seasonal gap in performance (summer months versus winter months) | 2.6 percentage points — narrowed not because winter improved but because summer performance collapsed to near-winter levels |
| North West Anglia National Health Service Foundation Trust average performance in the financial year 2024 to 2025 | 58.8 percent — sitting at the 50th percentile nationally |
| The trust that declined the most between the financial year 2019 to 2020 and the financial year 2024 to 2025 | South Tees Hospitals National Health Service Foundation Trust, which fell from 83.3 percent to 48.5 percent — a decline of 34.8 percentage points |
| The best-performing Type 1 trust in the financial year 2024 to 2025 | Sheffield Children's National Health Service Foundation Trust at 90.7 percent |
| The worst-performing Type 1 trust in the financial year 2024 to 2025 | United Lincolnshire Hospitals National Health Service Trust at 34.3 percent |

---

## 18. Narrative Summary

The story told by this data is not complicated, even though the data itself is large and the analysis is detailed. It can be summarised in a small number of clear statements, each of which the preceding analysis has demonstrated and quantified.

National Health Service Accident and Emergency departments in England are seeing only modestly more patients than they did before the COVID-19 pandemic — 6 percent more, to be precise. The patients arriving are not individually more acutely unwell than they used to be. The clinical work of assessment and treatment has not become significantly harder. And yet the proportion of patients seen within the government's own four-hour standard has fallen from 75 percent to 59 percent, and half a million patients per year now wait more than 12 hours in Accident and Emergency after a doctor has already decided they need to be admitted to a ward.

This can't be explained by what happens at the Accident and Emergency front door. The explanation lies at the back door: patients who need to go to a ward can't go, because ward beds are full of patients who need to go home but can't, because social care hasn't been commissioned or resourced at the level required to take them. That is the chain. The Accident and Emergency performance figures are the visible end of a problem that starts in social care funding and commissioning decisions made by local authorities and national government.

The seasonal analysis adds a further dimension to this picture. The crisis was once worst in winter and better in summer. That is no longer true in any meaningful sense. The seasonal gap has shrunk from 7.8 percentage points to 2.6 percentage points — not because winters have improved, but because summers have deteriorated. The system no longer uses the relative quiet of the summer months to recover. It is under persistent structural pressure year-round.

At the trust level, the breadth of the failure is striking. In the financial year 2024 to 2025, not one of England's 124 major Accident and Emergency trusts met the declared national target. The best-performing trust was a specialist paediatric hospital at 90.7 percent — 4.3 percentage points below the target. The worst-performing trust saw fewer than one in three patients within four hours. The trust at the national median — North West Anglia, running Hinchingbrooke Hospital in Huntingdon — averaged 58.8 percent. That is what the middle of the distribution looks like in 2024 to 2025.

The local trust for Huntingdonshire is not uniquely struggling. It is ordinarily failing, in exactly the same way and to approximately the same degree as every other major Accident and Emergency trust in England. The problem is not one organisation or one management team. It is a system that is broken at every level, in every region, in every season, and for every demographic. The only question that remains — and the one that data analysis alone can't fully answer — is what it would actually take to fix it.

---

*Analysis produced as part of the NHS A&E Waiting Times project.*
*Data source: National Health Service England — Accident and Emergency Attendances and Emergency Admissions statistics.*
*Coverage: April 2019 to March 2025, six complete financial years.*
*All figures are derived from publicly available open data. No confidential or proprietary data has been used.*
