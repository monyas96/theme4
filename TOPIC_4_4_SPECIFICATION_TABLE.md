# Topic 4.4: Illicit Financial Flows (IFFs) - Indicators Specification Table

## Overview
Topic 4.4 should have **multiple sub-topics** organized into tabs, with various indicators under each sub-topic.

---

## Tab 1: 4.4.1 - Magnitude of Illicit Financial Flows

### Indicator 4.4.1.1: IFFs as Percentage of GDP

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | IFFs as Percentage of GDP (Sum the values from topic 4.4.2 and calculate % to GDP) |
| **Type** | **TEXT-BASED** - Analysis from reports |
| **Analytical Focus Question** | Text based analysis from reports |
| **Graph Type** | Text-based analysis |
| **Implementation** | Use existing `tab_4_4_1.py` function |
| **Source Definition** | UNCTAD (2020). Economic Development in Africa Report |

### Indicator 4.4.1.2: Annual IFF Volume

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Annual IFF Volume (Sum the values from topic 4.4.2/ Text data) |
| **Type** | **TEXT-BASED** - Analysis from reports |
| **Analytical Focus Question** | Text based analysis from reports |
| **Graph Type** | Text-based analysis |
| **Implementation** | Use existing `tab_4_4_1.py` function |
| **Source Definition** | UNCTAD (2020). Economic Development in Africa Report |

---

## Tab 2: 4.4.2 - Channels of IFFs

### Indicator 4.4.2.1: Trade Mispricing

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Trade Mispricing: Volume and value of trade mispricing activities detected |
| **Analytical Focus Question** | How much wealth is lost through trade mispricing — a major channel of Illicit Financial Flows (IFFs) — and how do these losses differ across countries and trading relationships? |
| **Graph Type** | Stacked bar chart with Facet view for absolute value (USD Millions) vs relative (% of total trade) |
| **X-axis Encoding** | Country |
| **Y-axis Encoding** | Trade mispricing value (USD Millions or % of total trade) |
| **Color Encoding** | • #0072BC – Developing vs Advanced Economies<br>• #F26C2B – Global Trading Partners<br>• #FFD34E – Regional Average / Benchmark |
| **Interactivity** | • Hover Tooltip: {Country, Year, Mispricing Type, Value (USD m or % of trade), Partner Group}<br>• Hover Highlight: Highlights entire country bar across all facets |
| **Filters** | • Country Dropdown (multi-select)<br>• Year Slider (2000 → 2023)<br>• Toggle for absolute value vs share of total trade |
| **Analytical Lens** | **Efficiency:** Reveals systemic leakages — inefficient customs enforcement, weak valuation frameworks, or poor transparency that enable IFFs.<br>**Effectiveness:** Shows how well fiscal and regulatory systems prevent illicit outflows that erode domestic resources. |
| **Annotation/Guidance Features** | • Annotate top 5 countries with highest IFF-related trade gaps<br>• Display regional median line |
| **"How to Read This Graph" Text** | Each bar represents the estimated value of mispriced trade flows — the difference between what a country reports and what its trading partners record. The larger the gap, the greater the potential IFFs escaping regulation. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** Persistent or widening mispricing signals gaps in customs data, valuation practices, and inter-agency coordination.<br>**Effectiveness:** Declining mispricing over time suggests stronger IFF prevention, better governance, and enhanced fiscal control. |
| **Pillar Connection Text** | This indicator exposes a key IFF pathway — trade mispricing, where goods are intentionally over- or under-valued to shift profits abroad or avoid taxes. Reducing such gaps enhances transparency, fiscal fairness, and sustainable financing capacity under Theme 4: Ownership and Financial Sovereignty. |
| **Source Definition** | Reference GFI website |

---

### Indicator 4.4.2.2: Tax Evasion (ISORA Data)

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Tax Evasion proxied by ISORA Taxpayer registration data<br>• Active taxpayers on PIT register as percentage of Labor Force<br>• Active taxpayers on PIT register as percentage of Population<br>• On CIT register<br>• On VAT register<br>• On PAYE register<br>• On Excise register<br>• On PIT register |
| **Analytical Focus Question** | How effective are national tax administrations in registering and maintaining active taxpayers — and what share of potential taxpayers remain outside the system, creating domestic channels for IFFs and erosion of the revenue base? |
| **Graph Type** | Clustered bar chart (per tax type) + stacked bar chart (for composition by tax type per country) |
| **X-axis Encoding** | Year |
| **Y-axis Encoding** | Percentage of eligible population or labor force registered for each tax type |
| **Color Encoding** | • #0072BC – PIT register coverage<br>• #00A1A1 – CIT register coverage<br>• #F26C2B – VAT coverage<br>• #FFD34E – PAYE/Excise coverage |
| **Interactivity** | • Hover Tooltip: {Country, Year, Tax Type, % Registered, Change from Previous Year}<br>• Hover Highlight: Highlights a tax type across all countries |
| **Filters** | • Country Selector (Dropdown, multi-select)<br>• Year Filter (2016–2023)<br>• Tax Type Selector (PIT, CIT, VAT, PAYE, Excise) |
| **Analytical Lens** | **Efficiency:** Measures coverage and compliance — how well the tax administration converts economic activity into registered taxpayers.<br>**Effectiveness:** Assesses the capacity of DRM systems to close IFF-related loopholes (evasion, informality, under-registration). |
| **Annotation/Guidance Features** | • Highlight countries where PIT coverage < 5% of labor force (red flag for IFF risk) |
| **"How to Read This Graph" Text** | Each bar shows the share of the eligible population or labor force registered for a specific tax. Lower percentages mean large segments of economic activity remain outside the tax net — potential domestic IFF zones. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** High registration ratios indicate strong institutional capacity to capture economic actors.<br>**Effectiveness:** Expanding coverage reduces tax evasion and leakages, ensuring domestic resources stay within national systems to finance development. |
| **Pillar Connection Text** | Under Theme 4: DRM Systems and Institutions, this indicator examines domestic IFFs via tax evasion. Low taxpayer registration reveals institutional weakness in capturing economic activity and signals potential loss of resources to informal or illicit channels. |
| **Source Definition** | Reference ISORA |

---

### Indicator 4.4.2.3: Criminal Activities

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Criminal Activities: Number of reported total drug seizures times drug price per year |
| **Analytical Focus Question** | How large are criminally generated IFFs (from drug trafficking) in each African country, and how have they evolved over time? |
| **Graph Type** | Interactive line + bar hybrid:<br>• Line: IFF trend over time for selected country<br>• Bar: Country comparison for selected year<br>• Users toggle between "By Country" and "By Year" views |
| **X-axis Encoding** | Year (when viewing trends) or Country (when viewing cross-section) |
| **Y-axis Encoding** | Estimated value of IFFs from criminal activities |
| **Color Encoding** | OSAA gradient from low to high IFF value:<br>• #B7E0F2 → #0072BC → #F26C2B → #B30000 |
| **Interactivity** | • Hover Tooltip: {Country, Year, IFF Value (USD Millions), % of GDP, Top Drug Contributor}<br>• Hover Highlight: Highlights selected country's trend line |
| **Filters** | • Country Selector (Dropdown, multi-select, 1-3 countries)<br>• Year Filter (2010–2023)<br>• Toggle: View Mode = "Trend Over Time" / "Compare Countries" |
| **Analytical Lens** | **Efficiency:** How well law enforcement intercepts and monitors criminal financial flows. Low values may reflect limited data or enforcement capacity.<br>**Effectiveness:** High values signal strong criminal IFF pressures that erode fiscal sovereignty and require cross-border cooperation and asset recovery measures. |
| **Annotation/Guidance Features** | • Annotate top five countries by IFF value<br>• Add regional average marker line |
| **"How to Read This Graph" Text** | Use the filters to explore how much money leaves each country through criminal activity (proxied by drug-trade values). Select a country to see its trend or a year to compare across countries. Higher values = larger criminal economies or better detection. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** Trends showing stable or falling IFFs suggest improving interception systems.<br>**Effectiveness:** Compare IFF intensity across countries to assess where enforcement coordination or financial-intelligence reforms yield results. |
| **Pillar Connection Text** | This indicator quantifies the financial magnitude of criminally generated IFFs using drug-trade seizure values. It helps identify how crime-related financial leakages erode domestic revenues and signal institutional enforcement capacity. |
| **Source Definition** | Reference calculated methodology |

---

### Indicator 4.4.2.4: Corruption and Bribery

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Corruption and Bribery: Calculate (1. Normalize WB Control of Corruption indicator (0-1) Scores, 2. Assign weight to each country, 3. Sum all weights, 4. Calculate Each Country's Share (country weight/total weight * 148)) |
| **Analytical Focus Question** | How does corruption risk, as measured by governance quality, contribute to the estimated share of IFF vulnerability across African countries? |
| **Graph Type** | Weighted proportional bar chart + Map view<br>• Bar: Country's share of Africa's total corruption-linked IFF exposure (in %)<br>• Map: Geographic visualization of governance-linked IFF risk |
| **X-axis Encoding** | Country |
| **Y-axis Encoding** | Weighted IFF Risk Share (%) |
| **Color Encoding** | Governance palette (green = stronger control; red = weaker control):<br>• #007A33 → #F26C2B → #B30000 |
| **Interactivity** | • Hover Tooltip: {Country, Weighted IFF Risk Share (%), Normalized Control of Corruption Score (0–1), Rank}<br>• View Toggle: Switch between Bar View and Map View |
| **Filters** | • View Toggle (radio buttons): Bar View vs Map View<br>• Region Filter (Dropdown): West, East, Southern, North Africa |
| **Analytical Lens** | **Efficiency:** Measures how well institutional and financial governance systems reduce leakage through corruption.<br>**Effectiveness:** Reflects a government's long-term ability to deter IFFs via integrity, transparency, and accountability frameworks. |
| **Annotation/Guidance Features** | • Highlight top 5 countries with weakest governance (highest estimated IFF share)<br>• Add benchmark: African mean Control of Corruption score<br>• Tooltip explanation of the weighting logic |
| **"How to Read This Graph" Text** | Each bar shows the estimated share of corruption-driven IFF vulnerability in Africa, derived from normalized governance scores. Countries with lower control of corruption contribute disproportionately to total potential IFFs. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** Assess how institutional integrity systems (anti-corruption agencies, financial disclosure laws) limit leakages.<br>**Effectiveness:** Track improvements in governance scores as indicators of progress in preventing corruption-linked IFFs. |
| **Pillar Connection Text** | Under Theme 4: DRM Systems and Institutions, this indicator estimates the potential contribution of corruption and bribery to Illicit Financial Flows. It uses governance quality as a proxy for leakage risk — recognizing that weak institutions and rent-seeking behaviors often enable large unrecorded outflows. |
| **Source Definition** | Reference calculated methodology |

---

## Tab 3: 4.4.3 - Detection and Enforcement

**Note:** This tab includes 4 indicators organized as sub-tabs:
- 4.4.3.1: Efficacy of Anti-IFF Measures
- 4.4.3.2.a: Operating Metrics Audit
- 4.4.3.2.b: Resources and ICT Infrastructure
- 4.4.3.2.c: Staff Metrics

### Indicator 4.4.3.1: Efficacy of Anti-IFF Measures

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Efficacy of Anti-IFF Measures (Proxied by enablers framework suggested by Coherent policies for combating Illicit Financial Flows) |
| **Analytical Focus Question** | How strong and coherent are national systems for preventing, detecting, and enforcing measures against illicit financial flows? |
| **Graph Type** | Radar (spider) chart for composite view + Bar chart comparison + Optional trend line<br>• Tab 1: By Enabler (Radar view)<br>• Tab 2: By Country (Bar chart view)<br>• Tab 3: Composite Readiness Trend (Line chart) |
| **X-axis Encoding** | Country (in bar view) or Sub-indicator (in radar view) |
| **Y-axis Encoding** | Score (0-1) |
| **Color Encoding** | Each sub-indicator has its own hue:<br>• Rule of Law (WJP) – #0072BC<br>• Justice (Mo Ibrahim) – #009D8C<br>• Control of Corruption – #F26C2B<br>• Institutions (CPIA) – #FFD34E<br>• Identity Systems – #7C4DFF |
| **Interactivity** | • Hover Tooltip: {Country, Year, Indicator Name, Score (0–1), Source}<br>• Hover Highlight: Emphasizes selected indicator's axis in radar view<br>• Legend Interaction: Click on enabler to isolate or toggle |
| **Filters** | • View Mode Selector (Tabs): By Enabler / By Country / Composite Readiness Trend<br>• Country Selector (Multi-select, up to 5 countries)<br>• Sub-indicator Selector (Dropdown) |
| **Analytical Lens** | **Efficiency:** Evaluates how well anti-IFF systems deploy resources and institutions for compliance and monitoring.<br>**Effectiveness:** Assesses whether governance quality, rule of law, and institutional strength actually translate to reduced IFF risks. |
| **Annotation/Guidance Features** | • Highlight top performers and weakest performers |
| **"How to Read This Graph" Text** | Each sub-indicator represents a key enabler of anti-IFF enforcement. Use the selector to explore performance on rule of law, justice systems, corruption control, institutional quality, and identity documentation. Higher scores = stronger foundations for combating IFFs. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** Focus on how effectively administrative systems (tax, justice, customs) coordinate enforcement.<br>**Effectiveness:** Assess whether strong institutional and governance scores align with actual reductions in IFFs or improved detection/reporting. |
| **Pillar Connection Text** | This composite indicator measures how capable a country is in implementing coherent policies to combat IFFs. It integrates multiple governance and institutional metrics to reflect the "effectiveness architecture" behind detection and enforcement. |
| **Source Definition** | Reference calculated methodology |

---

### Indicator 4.4.3.2.a: Operating Metrics Audit

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Operating Metrics Audit:<br>• Number of audits completed<br>• % of audits leading to adjustment<br>• Additional assessments raised (total / by tax type) |
| **Analytical Focus Question** | How effective are tax administrations in detecting non-compliance and converting audits into additional assessed revenue? |
| **Graph Type** | Dual-axis combination chart:<br>• Bars = Number of audits completed (Y₁)<br>• Line = Value of additional assessments (Y₂, in LCY or USD) |
| **X-axis Encoding** | Year |
| **Y-axis Encoding** | Y₁ = Number of audits completed<br>Y₂ = Value of additional assessments (in thousands, LCY or USD) |
| **Color Encoding** | Bars and lines use distinct colors for clarity |
| **Interactivity** | • Hover Tooltip: {Country, Year, # Audits Completed, % Leading to Adjustment, Value of Assessments, Tax Type}<br>• Hover Highlight: When hovering over a bar, corresponding line point brightens |
| **Filters** | • Tax Type Selector (Dropdown): All Audits, CIT, PIT, VAT, PAYE<br>• Year Range Filter (Slider): 2016–2023<br>• Country Selector (Multi-select, up to 3 countries)<br>• View Mode Toggle: Chart View vs Map View |
| **Analytical Lens** | **Efficiency:** % of audits leading to adjustment — reflects targeting accuracy and administrative resource optimization.<br>**Effectiveness:** Value of additional assessments — shows monetary recovery and enforcement impact. |
| **Annotation/Guidance Features** | • Benchmark line for Africa regional median of "% of audits leading to adjustment"<br>• Highlight top 3 performers in enforcement value<br>• Tooltip explanation for what "adjustment" means |
| **"How to Read This Graph" Text** | Bars show how many audits were completed by each country or year. The line shows the total value of additional assessments raised from those audits. The darker the bar, the more effective audits are at finding discrepancies (higher % of adjustments). |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** A high percentage of audits resulting in adjustments means audit selection is well-targeted and resources are efficiently used.<br>**Effectiveness:** High additional assessments reflect strong institutional capacity for enforcement and revenue recovery. |
| **Pillar Connection Text** | Under Theme 4: DRM Systems and Institutions, this indicator captures a country's operational strength in tax enforcement. It links to Detection and Enforcement by showing how institutional processes translate into real fiscal discipline. |
| **Source Definition** | Reference ISORA |

---

### Indicator 4.4.3.2.b: Resources and ICT Infrastructure

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Resources and ICT Infrastructure:<br>• ICT expenditure (% of total)<br>• ICT operating cost (% of total operating expenditure)<br>• % staff in ICT support |
| **Analytical Focus Question** | Are tax and customs administrations investing enough in digital systems and resources to enable efficient, modern revenue collection? |
| **Graph Type** | Scatterplot showing relationship between ICT spending and ICT staffing<br>• X = % staff in ICT roles<br>• Y = ICT expenditure (% of operating budget)<br>• Color = Region or Income Group<br>• Size = Total operating expenditure (if available) |
| **X-axis Encoding** | % of staff in ICT support roles |
| **Y-axis Encoding** | ICT expenditure as % of total operating expenditure |
| **Color Encoding** | Reflect digital capacity:<br>• High investment = Dark blue (#004C97)<br>• Medium = Teal (#009D8C)<br>• Low = Light orange (#F4B183) |
| **Interactivity** | • Hover Tooltip: {Country, Year, ICT Staff (%), ICT Expenditure (%), Total Operating Expenditure, Income Group, Region, Source}<br>• Hover Highlight: Emphasizes selected country, dynamic crosshair lines show deviation from regional mean |
| **Filters** | • Country Selector (Dropdown, up to 3 countries)<br>• Year Selector (Slider, 2016–2023)<br>• Region Filter (Dropdown) |
| **Analytical Lens** | **Efficiency:** High ICT spending and skilled staffing signal efficient use of resources and automation of manual processes.<br>**Effectiveness:** Stable ICT investment over time enables reliable enforcement and service delivery. |
| **Annotation/Guidance Features** | • Add reference lines for Africa regional average spending and staffing share<br>• Highlight digital front-runners (via color gradient annotation) |
| **"How to Read This Graph" Text** | Each point represents a country's tax administration. The X-axis shows how many staff work in ICT support, while the Y-axis shows how much of the budget is spent on ICT. Countries in the upper-right quadrant combine strong digital workforces with adequate investment — a sign of high administrative capacity. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** Does the share of ICT spending and staffing align with revenue outcomes and audit performance?<br>**Effectiveness:** Sustained digital investment enables data-driven tax compliance and reduces leakages linked to IFFs. |
| **Pillar Connection Text** | This indicator links to Theme 4 (DRM Systems and Institutions) and Topic 4.4.3 (Detection and Enforcement). A digitally enabled revenue administration improves risk assessment, reduces manual errors, and strengthens compliance monitoring — all key to curbing IFFs. |
| **Source Definition** | Reference ISORA |

---

### Indicator 4.4.3.2.c: Staff Metrics

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Staff Metrics:<br>• Staff recruitments vs departures<br>• % of staff by qualification (Bachelor's, Master's)<br>• Age distribution or gender balance |
| **Analytical Focus Question** | How skilled, stable, and representative are the human resources in tax and customs administrations—and what does this reveal about institutional resilience and reform capacity? |
| **Graph Type** | Line chart of staff count change over time to show turnover trend |
| **X-axis Encoding** | Year |
| **Y-axis Encoding** | Percentage of staff |
| **Color Encoding** | • Dark Blue (#004C97) = Recruitments / Qualified Staff<br>• Orange (#F4B183) = Departures / Under-qualified Staff<br>• Teal (#009D8C) = Balanced / Gender equity |
| **Interactivity** | • Hover Tooltip: {Country, Year, Recruitment %, Departure %, Qualified %, Gender Ratio (% female), Total Staff}<br>• Hover Highlight: Emphasizes selected series, dims others |
| **Filters** | • Country Selector (Dropdown, up to 3 countries)<br>• Year Range Filter (Slider, 2010–2023)<br>• Staffing Metric Selector (Dropdown): Recruitments vs Departures, Qualification Profile, Gender Composition<br>• Income Group Filter (Checkbox) |
| **Analytical Lens** | **Efficiency:** Low staff turnover + right skill mix = efficient use of human resources and reduced retraining cost.<br>**Effectiveness:** High share of qualified, diverse staff = institution able to execute audits and enforcement reliably. |
| **Annotation/Guidance Features** | • Highlight median turnover ratio across countries |
| **"How to Read This Graph" Text** | The chart compares recruitment and departure rates in the tax administration over time. Bars extending right indicate inflows (recruitments); bars extending left show outflows (departures). A balanced or positive inflow suggests staff stability; persistent outflows signal capacity erosion. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** Stable workforce reduces hiring costs and training gaps.<br>**Effectiveness:** Skilled and retained staff strengthen audit performance, taxpayer services, and institutional memory—key to sustained DRM outcomes. |
| **Pillar Connection Text** | This indicator relates to Theme 4: DRM Systems and Institutions under Topic 4.4.3: Detection and Enforcement. It captures the human engine behind enforcement capacity. Tax administrations with low turnover and qualified, gender-balanced staff are better positioned to maintain continuity, fairness, and innovation in combating IFFs. |
| **Source Definition** | Reference ISORA |

---

## Tab 4: 4.4.4 - Transparency and Accountability

**Note:** This tab includes 1 indicator:
- 4.4.4.1: Financial Secrecy Index

### Indicator 4.4.4.1: Financial Secrecy Index

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Financial Secrecy Index |
| **Analytical Focus Question** | How does a country's financial secrecy level affect its vulnerability to Illicit Financial Flows and its alignment with global transparency standards? |
| **Graph Type** | Line chart (multi-year) tracking each country's secrecy score (2011–2025) |
| **X-axis Encoding** | Year |
| **Y-axis Encoding** | Financial Secrecy Score |
| **Color Encoding** | Transparency narrative:<br>• Dark Orange (#E87722): High secrecy (risk zone)<br>• Amber (#F4B183): Moderate secrecy<br>• Blue (#1B75BB): Low secrecy (transparent jurisdictions) |
| **Interactivity** | • Hover Tooltip: {Country, Year, Secrecy Score, Rank, Change since 2011} |
| **Filters** | • Country Selector (Dropdown, multi-select)<br>• Region Filter (Dropdown)<br>• Income Group Filter (Checkbox)<br>• Year Range Slider (2011–2025) |
| **Analytical Lens** | **Efficiency:** Low secrecy improves cross-border data exchange, reducing compliance costs and enabling efficient tax administration.<br>**Effectiveness:** Transparent financial systems deter IFFs and improve enforcement outcomes across institutions. |
| **Annotation/Guidance Features** | • Show shaded zones: 0–30 (Transparent), 31–60 (Moderate), 61–100 (Opaque) |
| **"How to Read This Graph" Text** | Each line shows how a country's financial secrecy has evolved since 2011. Lower scores indicate stronger transparency frameworks. Countries with flat or rising scores remain more exposed to IFF-related risks. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** Countries with reduced secrecy simplify financial oversight and international cooperation.<br>**Effectiveness:** Declining secrecy scores reflect effective anti-IFF policies — such as beneficial ownership registries and data-sharing agreements. |
| **Pillar Connection Text** | This indicator links directly to Theme 4 (DRM Systems and Institutions) and specifically Topic 4.4.4: Transparency and Accountability. Financial secrecy fuels illicit financial flows by hiding ownership and transactions. |
| **Source Definition** | Financial Secrecy Index |

---

## Tab 5: 4.4.5 - Financing Resilience

### Indicator 4.4.5.1: Tax Buoyancy

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Tax Buoyancy: Ratio of change in tax revenue in relation to change in gross domestic product or GDP of an economy. It measures how responsive a taxation policy is to growth in economic activities. |
| **Analytical Focus Question** | How responsive is a country's tax system to economic growth — and how might Illicit Financial Flows weaken this relationship? |
| **Graph Type** | Scatter plot — Tax Buoyancy (Y) vs GDP growth (X) across countries<br>Each point represents one country-year; color shows region or IFF risk level |
| **X-axis Encoding** | GDP growth rate (%) — proxy for economic activity |
| **Y-axis Encoding** | Tax buoyancy (elasticity coefficient β) |
| **Color Encoding** | Fiscal-performance palette:<br>• Blue (#1B75BB): Responsive (buoyancy ≥ 1.0)<br>• Orange (#E87722): Weakly responsive (0.5–1.0)<br>• Red (#D32F2F): Unresponsive (< 0.5)<br>• Teal (#009D8C): Over-responsive (>1.5, volatile) |
| **Interactivity** | • Hover Tooltip: {Country, Year, Buoyancy, GDP Growth, Tax Revenue %, Source} |
| **Filters** | • Dropdowns for Country, Income Group, Region |
| **Analytical Lens** | **Efficiency:** A buoyant tax system captures new growth automatically, reducing reliance on external borrowing.<br>**Effectiveness:** Persistent low buoyancy implies leakage through exemptions, evasion, or IFFs, undermining fiscal stability. |
| **Annotation/Guidance Features** | • Highlight outliers — economies with GDP growth but stagnant revenue |
| **"How to Read This Graph" Text** | The graph compares GDP growth and tax responsiveness. A buoyancy of 1.0 means tax revenue grows at the same rate as GDP — a balanced system. Values below 1 indicate that tax revenues are lagging behind economic expansion, signaling inefficiencies or leakages. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** If buoyancy is low despite strong GDP growth, resources are being lost — possibly due to tax evasion or profit shifting.<br>**Effectiveness:** A consistent buoyancy near or above 1 reflects policy effectiveness in translating growth into fiscal capacity, strengthening resilience to IFFs. |
| **Pillar Connection Text** | This indicator sits within Theme 4: DRM Systems and Institutions → Topic 4.4.5: Financing Resilience. It links macroeconomic performance to fiscal efficiency — revealing whether economic growth translates into sustainable domestic revenue. |
| **Source Definition** | Reference calculated methodology |

---

### Indicator 4.4.5.2: Social Impact of Lost Tax

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Social impact of lost tax (Tax loss equivalent to % of health and education budget - sotj20_loss_total_share_healthexpenses all years) |
| **Type** | **TEXT-BASED** - Analysis from reports |
| **Analytical Focus Question** | Text based analysis from reports |
| **Graph Type** | Text-based analysis |

---

## Tab 6: 4.4.6 - Sector-Specific Analysis

### Indicator 4.4.6.1.a: Specific Sectors

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Specific sectors: lists the laws and regulations that govern the taxation and mining activity of each country. (count the number of general regime and mining regime) |
| **Type** | **TEXT-BASED** - Analysis from reports |
| **Analytical Focus Question** | Text based analysis from reports |
| **Graph Type** | Text-based analysis |

### Indicator 4.4.6.1.b: Rent Sharing

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Rent sharing between state and investors |
| **Type** | **TEXT-BASED** - Analysis from reports |
| **Analytical Focus Question** | Text based analysis from reports |
| **Graph Type** | Text-based analysis |

---

## Implementation Structure

### Proposed Tab Organization (with Sub-Tabs):
```
Tab 1: 4.4.1 - Magnitude of IFFs
├── Sub-tab 1: 4.4.1.1: IFFs as % of GDP (Text-based) ✅ (Use tab_4_4_1.py)
└── Sub-tab 2: 4.4.1.2: Annual IFF Volume (Text-based) ✅ (Use tab_4_4_1.py)

Tab 2: 4.4.2 - Channels of IFFs
├── Sub-tab 1: 4.4.2.1: Trade Mispricing (Stacked bar chart)
├── Sub-tab 2: 4.4.2.2: Tax Evasion - ISORA (Clustered/stacked bar chart)
├── Sub-tab 3: 4.4.2.3: Criminal Activities (Line + bar hybrid)
└── Sub-tab 4: 4.4.2.4: Corruption and Bribery (Weighted bar chart + map)

Tab 3: 4.4.3 - Detection and Enforcement
├── Sub-tab 1: 4.4.3.1: Efficacy of Anti-IFF Measures (Radar + bar charts)
├── Sub-tab 2: 4.4.3.2.a: Operating Metrics Audit (Dual-axis chart)
├── Sub-tab 3: 4.4.3.2.b: Resources and ICT Infrastructure (Scatterplot)
└── Sub-tab 4: 4.4.3.2.c: Staff Metrics (Line chart)

Tab 4: 4.4.4 - Transparency and Accountability
└── Sub-tab 1: 4.4.4.1: Financial Secrecy Index (Line chart)

Tab 5: 4.4.5 - Financing Resilience
├── Sub-tab 1: 4.4.5.1: Tax Buoyancy (Scatter plot)
└── Sub-tab 2: 4.4.5.2: Social Impact of Lost Tax (Text-based)

Tab 6: 4.4.6 - Sector-Specific Analysis
├── Sub-tab 1: 4.4.6.1.a: Specific Sectors (Text-based)
└── Sub-tab 2: 4.4.6.1.b: Rent Sharing (Text-based)
```

---

## Summary by Type

### Text-Based Indicators (Use existing functions or create new):
- ✅ 4.4.1.1: IFFs as % of GDP (Use `tab_4_4_1.py`)
- ✅ 4.4.1.2: Annual IFF Volume (Use `tab_4_4_1.py`)
- ⏳ 4.4.5.2: Social Impact of Lost Tax
- ⏳ 4.4.6.1.a: Specific Sectors
- ⏳ 4.4.6.1.b: Rent Sharing

### Calculated Indicators:
- ⏳ 4.4.2.3: Criminal Activities (Number of drug seizures × drug price)
- ⏳ 4.4.2.4: Corruption and Bribery (Normalize Control of Corruption, weight, calculate share)
- ⏳ 4.4.3.1: Efficacy of Anti-IFF Measures (Composite from multiple governance indicators)
- ⏳ 4.4.5.1: Tax Buoyancy (Ratio of tax revenue change to GDP change)

### Direct Indicators (from data sources):
- ⏳ 4.4.2.1: Trade Mispricing (GFI data)
- ⏳ 4.4.2.2: Tax Evasion - ISORA (ISORA taxpayer registration data)
- ⏳ 4.4.3.2.a: Operating Metrics Audit (ISORA audit data)
- ⏳ 4.4.3.2.b: Resources and ICT Infrastructure (ISORA ICT data)
- ⏳ 4.4.3.2.c: Staff Metrics (ISORA staff data)
- ⏳ 4.4.4.1: Financial Secrecy Index (Financial Secrecy Index data)

---

## Confirmation Checklist

Please confirm:
- [ ] The table structure is clear and complete
- [ ] All indicators are correctly specified
- [ ] The tab organization (6 tabs) is acceptable
- [ ] Text-based indicators are correctly identified
- [ ] Calculated indicators and their formulas are correct
- [ ] Data source references are accurate
- [ ] Ready to proceed with implementation

