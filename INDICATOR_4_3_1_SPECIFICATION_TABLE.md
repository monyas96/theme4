# Indicator 4.3.1: Market Capitalization - Sub-Indicators Specification Table

## Overview
Indicator 4.3.1 should have **three sub-indicators** organized as sub-tabs within Tab 1.

**Important Note:** These indicators are **calculated/proxy indicators** that need to be computed from underlying data sources or serve as proxies for broader financial market concepts.

---

## Indicator 4.3.1.1: Market Capitalization to GDP

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Market capitalization in USD as percentage of GDP (Calculated indicator) |
| **Type** | **CALCULATED** - Must be computed from two underlying indicators |
| **Data Source Codes** | • CM.MKT.LCAP.CD (World Bank WDI) - Market capitalization<br>• NY.GDP.MKTP.CD (World Bank WDI) - GDP |
| **Calculation Formula** | MarketCap%GDP = (CM.MKT.LCAP.CD / NY.GDP.MKTP.CD) × 100 |
| **Proxy For** | Financial market depth, capital mobilization capacity, financial sovereignty |
| **Analytical Focus Question** | How deep and mature are domestic financial markets relative to the size of the economy — and what does this say about financial sovereignty and resilience? |
| **Graph Type** | Multi-country line chart (2000–2023)<br>Alternate view: scatter plot (Market Cap vs GDP per capita) |
| **X-axis Encoding** | Year (or GDP per capita for scatter plot) |
| **Y-axis Encoding** | Market Capitalization (% of GDP) |
| **Color Encoding** | • #0072BC → Above 60% of GDP (deep markets)<br>• #F26C2B → 20–60% (developing)<br>• #FFD34E → Below 20% (shallow, underdeveloped) |
| **Interactivity** | • Hover Tooltip: {Country, Year, Market Cap (% GDP), GDP per Capita (USD)}<br>• Shaded Reference Bands:<br>  – 0–20% (Shallow Markets → #FFD34E, translucent)<br>  – 20–60% (Developing → #F26C2B, light opacity)<br>  – >60% (Deep Markets → #0072BC, soft blue tint) |
| **Filters** | • Country Selector: Dropdown to select one or multiple countries<br>• Region Toggle: Switch between Regional Overview and Country Comparison<br>• Year Range Slider (2000–2023) |
| **Analytical Lens** | **Efficiency:** Evaluates whether financial markets efficiently allocate savings into investment.<br>**Effectiveness:** Measures how well markets channel capital toward productive sectors, reducing dependence on debt or aid. |
| **Annotation/Guidance Features** | • Add reference zones (0–20%, 20–60%, >60%) shaded bands<br>• Annotate structural breaks (2014-2016 commodity shocks and COVID) |
| **"How to Read This Graph" Text** | The line shows the ratio of stock market capitalization to GDP. Higher values mean larger, more liquid capital markets relative to the economy — a signal of financial depth and domestic investor confidence. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** A growing market cap/GDP ratio suggests that savings are being mobilized and allocated effectively through capital markets.<br>**Effectiveness:** Sustained depth signals institutional confidence, access to finance, and reduced external vulnerability. |
| **Pillar Connection Text** | Under Theme 4: Ownership and Financial Sovereignty, this indicator reveals how domestic capital markets contribute to national financing capacity. Deep, well-capitalized markets empower governments and firms to fund growth from within rather than rely on external debt. |
| **Source Definition** | Reference calculated methodology |

---

## Indicator 4.3.1.2: Portfolio Investment Bonds

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Portfolio investment, bonds (PPG + PNG) (NFL, current US$) |
| **Type** | **DIRECT** - Available directly from data source (but may need % of GDP calculation for toggle) |
| **Data Source Code** | DT.NFL.BOND.CD (World Bank WDI) |
| **Additional Calculation** | May need to calculate as % of GDP for metric toggle: (DT.NFL.BOND.CD / GDP) × 100 |
| **Proxy For** | External bond market dependency, external financing reliance, fiscal sovereignty |
| **Analytical Focus Question** | How much do African economies rely on external bond markets for financing, and how volatile or sustainable are these flows over time? |
| **Graph Type** | Multi-country line chart (log scale) to track magnitude and volatility |
| **X-axis Encoding** | Year |
| **Y-axis Encoding** | Portfolio Investment, Bonds (log scale recommended) |
| **Color Encoding** | • #0072BC → Moderate & stable inflows (sustainable financing)<br>• #FFD34E → Increasing exposure (watch zone)<br>• #F26C2B → Volatile or large inflows (risk & dependency) |
| **Interactivity** | • Hover Tooltip: {Country, Year, Portfolio Bond Inflows (US$), % of GDP, Year-on-Year Change (%)}<br>• Dynamic interpretation: "Ghana's bond inflows reached 2.4 bn US$ (5.2 % GDP) in 2021 — up 35 % from 2020."<br>• Hover Highlight: Emphasizes hovered line, dims others; region mean line in background |
| **Filters** | • Country Dropdown Selector: Compare one or multiple countries<br>• Year Range Slider (2000–2023)<br>• Region Toggle: Switch between Regional and Country-Level views<br>• Metric Toggle: Switch between Absolute inflows (US$) and Inflows as % of GDP |
| **Analytical Lens** | **Efficiency:** Evaluates how well countries attract capital without excessive volatility or cost.<br>**Effectiveness:** Assesses whether external bond flows contribute to productive financing (vs short-term vulnerability). |
| **Annotation/Guidance Features** | • Highlight major global shocks (2008, 2014, 2020)<br>• Annotate issuance booms (Eurobond waves)<br>• Shaded region for high-risk exposure (>10% GDP) |
| **"How to Read This Graph" Text** | Each line or area shows the scale of foreign bond inflows (public and private) over time. Sharp spikes indicate borrowing surges or foreign investor interest; sudden drops reveal exposure to global financial shocks. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** Sustainable portfolios show stable inflows tied to investment and growth.<br>**Effectiveness:** Overreliance or volatility signals vulnerability — external debt servicing risks and limited domestic absorption capacity. |
| **Pillar Connection Text** | Under Theme 4: Ownership and Financial Sovereignty, this indicator measures how much African countries rely on external portfolio capital. Stable, moderate flows support development; volatile or excessive inflows can erode fiscal sovereignty and increase vulnerability to global shocks. |
| **Source Definition** | Bonds are securities issued with a fixed rate of interest for a period of more than one year. They include net flows through cross-border public and publicly guaranteed and private nonguaranteed bond issues. Data are in current U.S. dollars. https://data.worldbank.org/indicator/DT.NFL.BOND.CD |

---

## Indicator 4.3.1.3: Adequacy of International Reserves

| **Specification Category** | **Details** |
|---------------------------|-------------|
| **Indicator Name** | Adequacy of International Reserves: The ratio of (BoP, current US$) to External Debt Stocks, Short-Term (DOD, Current US$)) |
| **Type** | **CALCULATED** - Must be computed from two underlying indicators |
| **Data Source Codes** | • BN.RES.INCL.CD (World Bank WDI) - Reserves and related items<br>• DT.DOD.DSTC.CD (World Bank WDI) - External debt stocks, short-term |
| **Calculation Formula** | Reserve Adequacy Ratio = BN.RES.INCL.CD / DT.DOD.DSTC.CD<br><br>**Interpretation:**<br>• >1 (≥100%) → full coverage (resilient)<br>• 0.5–1 (50–99%) → partial coverage (vulnerable)<br>• <0.5 (<50%) → high risk (liquidity constraint) |
| **Proxy For** | Macro-financial stability, policy autonomy, ability to manage external shocks |
| **Analytical Focus Question** | Do countries hold enough reserves to manage short-term debt obligations, ensuring macro-financial stability and policy autonomy? |
| **Graph Type** | Ratio-based line chart (multi-country) or diverging bar chart (latest year)<br>Optional: heatmap for multi-year comparison |
| **X-axis Encoding** | Year (or Country for bar chart) |
| **Y-axis Encoding** | Reserve Adequacy Ratio (Reserves / Short-Term Debt) |
| **Color Encoding** | • #007B33 → ≥100% (Adequate coverage – resilient)<br>• #FFD34E → 50–99% (Moderate coverage – vulnerable)<br>• #F26C2B → <50% (Insufficient reserves – high risk) |
| **Interactivity** | • Hover Tooltip: {Country, Year, Reserve Adequacy Ratio, Reserves US$, Short-term Debt US$}<br>• Dynamic interpretation: "Ghana's reserves cover 62 % of short-term debt — below the 100 % adequacy threshold."<br>• Hover Highlight: Brightens selected country line/bar; others dim<br>• Reference Line @ y = 1: visual benchmark for "full coverage" |
| **Filters** | • Country Dropdown: Choose one or more countries<br>• Year Slider (2000 → 2023)<br>• View Toggle: Trend View (line chart) vs Snapshot View (diverging bar chart)<br>• Facet Toggle: Switch between Economic Structure and Region |
| **Analytical Lens** | **Efficiency:** Evaluates prudent financial management — whether reserves are built sustainably without over-hoarding.<br>**Effectiveness:** Measures policy capacity to respond to shocks, stabilize exchange rates, and manage liquidity crises. |
| **Annotation/Guidance Features** | • Reference line at ratio = 1 (full short-term coverage)<br>• Shaded bands for risk tiers (red/orange/green)<br>• Annotate crisis years (2008, 2014 commodity slump, 2020 pandemic) |
| **"How to Read This Graph" Text** | Each country's line shows how much of its short-term external debt could be covered by its reserves. Ratios above 1 mean full coverage; lower values suggest vulnerability to external liquidity shocks. |
| **"How to Apply Analytical Lens" Text** | **Efficiency:** Stable or rising ratios reflect disciplined reserve accumulation without overburdening fiscal space.<br>**Effectiveness:** Adequate reserves enable governments to absorb external shocks — a sign of resilient and self-reliant financial governance. |
| **Pillar Connection Text** | Under Theme 4 this indicator measures a country's ability to protect itself from external volatility. Adequate reserves mean greater control over national financial policy — a foundation for fiscal and monetary independence. |
| **Source Definition** | Reference calculated methodology |

---

## Implementation Structure

### Tab 1: Indicator 4.3.1 - Market Capitalization
```
Tab 1: Indicator 4.3.1 - Market Capitalization
├── Sub-tab 1: 4.3.1.1 Market Capitalization to GDP ⏳ (IN PROGRESS)
├── Sub-tab 2: 4.3.1.2 Portfolio Investment Bonds ⏳
└── Sub-tab 3: 4.3.1.3 Adequacy of International Reserves ⏳
```

---

## Key Implementation Notes

### Common Features Across All Three Indicators:
1. **Unified Dashboard Structure:**
   - Indicator header with analytical focus question and info icon
   - Local filter row (Year, Country, Region, Reset)
   - Multi-view tabs (Graph View, Map View, Data Table)
   - Supporting information layers (Learn more, Analytical Lens)

2. **Color Consistency:**
   - Deep/Adequate/Strong: #0072BC or #007B33 (blue/green)
   - Moderate/Developing/Vulnerable: #FFD34E (yellow)
   - Shallow/High Risk: #F26C2B (orange/red)
   - Selected countries: #003366 (deep blue)

3. **Special Features:**
   - **4.3.1.1:** View toggle (Line Chart vs Scatter Plot), Reference bands
   - **4.3.1.2:** Metric toggle (Absolute US$ vs % of GDP), Log scale, Year-on-year change in tooltip
   - **4.3.1.3:** View toggle (Trend vs Snapshot/Bar chart), Reference line at 1.0, Risk tier bands

---

## Data Source Mapping

| Indicator | Type | World Bank Code | Indicator Label in Data | Calculation Required |
|-----------|------|----------------|------------------------|---------------------|
| 4.3.1.1 | **CALCULATED** | CM.MKT.LCAP.CD | Market capitalization of listed domestic companies (current US$) | Yes - Divide by GDP |
| 4.3.1.1 | **CALCULATED** | NY.GDP.MKTP.CD | GDP (current US$) | Yes - Used as denominator |
| 4.3.1.2 | **DIRECT** | DT.NFL.BOND.CD | Portfolio investment, bonds (PPG + PNG) (NFL, current US$) | Optional - % of GDP for toggle |
| 4.3.1.3 | **CALCULATED** | BN.RES.INCL.CD | Reserves and related items (BoP, current US$) | Yes - Divide by short-term debt |
| 4.3.1.3 | **CALCULATED** | DT.DOD.DSTC.CD | External debt stocks, short-term (DOD, current US$) | Yes - Used as denominator |

### Calculation Requirements Summary:
- **4.3.1.1:** ✅ Requires calculation from Market Cap and GDP
- **4.3.1.2:** ⚠️ Direct indicator, but may need % of GDP calculation for metric toggle
- **4.3.1.3:** ✅ Requires calculation from Reserves and Short-Term Debt

---

## Confirmation Checklist

Please confirm:
- [ ] The table structure is clear and complete
- [ ] All three sub-indicators are correctly specified
- [ ] The implementation structure (sub-tabs) is acceptable
- [ ] Data source codes and indicator labels are correct
- [ ] Color encodings and interactivity features are as specified
- [ ] Ready to proceed with implementation

