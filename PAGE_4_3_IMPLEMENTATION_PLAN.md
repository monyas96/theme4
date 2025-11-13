# Page 4.3: Topic 4.3 - Capital Markets
## Complete Implementation Plan

### Page Structure Overview

Based on the specification matrix, Page 4.3 should have **3 main tabs** with the following structure:

```
Page 4.3: Capital Markets
├── Tab 1: Indicator 4.3.1 - Market Capitalization
│   ├── 4.3.1.1 Market Capitalization to GDP (Multi-country line chart) ⏳
│   ├── 4.3.1.2 Portfolio Investment Bonds (Multi-country line chart, log scale) ⏳
│   └── 4.3.1.3 Adequacy of International Reserves (Ratio line chart) ⏳
├── Tab 2: Indicator 4.3.2 - Financial Intermediation
│   ├── 4.3.2.1 Banking Sector Development Index (Composite index line chart) ⏳
│   └── 4.3.2.2 Private Sector Credit to GDP (Multi-country line chart) ⏳
└── Tab 3: Indicator 4.3.3 - Institutional Investors
    └── 4.3.3.1 Pension Funds and Sovereign Wealth Funds (Text-based analysis) ⏳
```

**Total Indicators:** 6
- ⏳ 6 to implement

---

## Indicator 4.3.1.1: Market Capitalization to GDP
**Status:** ⏳ **TO IMPLEMENT**

**Location:** Tab 1

### Specification Details:
- **Analytical Focus Question:** How deep and mature are domestic financial markets relative to the size of the economy — and what does this say about financial sovereignty and resilience?
- **Graph Type:** Multi-country line chart (2000–2023) with alternate scatter plot view (Market Cap vs GDP per capita)
- **X-axis:** Year (or GDP per capita for scatter)
- **Y-axis:** Market Capitalization (% of GDP)
- **Color Encoding:**
  - #0072BC → Above 60% of GDP (deep markets)
  - #F26C2B → 20–60% (developing)
  - #FFD34E → Below 20% (shallow, underdeveloped)
- **Interactivity:**
  - Hover Tooltip: {Country, Year, Market Cap (% GDP), GDP per Capita (USD)}
  - Shaded Reference Bands:
    - 0–20% (Shallow Markets → #FFD34E, translucent)
    - 20–60% (Developing → #F26C2B, light opacity)
    - >60% (Deep Markets → #0072BC, soft blue tint)
- **Filters:**
  - Country Selector: Dropdown to select one or multiple countries
  - Region Toggle: Switch between Regional Overview and Country Comparison
  - Year Range Slider (2000–2023)
- **Features:**
  - Add reference zones (0–20%, 20–60%, >60%) shaded bands
  - Annotate structural breaks (2014-2016 commodity shocks and COVID)
  - View toggle: Line chart vs Scatter plot (Market Cap vs GDP per capita)
- **How to Read:** The line shows the ratio of stock market capitalization to GDP. Higher values mean larger, more liquid capital markets relative to the economy — a signal of financial depth and domestic investor confidence.
- **Analytical Lens:**
  - Efficiency: A growing market cap/GDP ratio suggests that savings are being mobilized and allocated effectively through capital markets.
  - Effectiveness: Sustained depth signals institutional confidence, access to finance, and reduced external vulnerability.

### Implementation Checklist:
- [ ] Create unified dashboard structure
- [ ] Calculate indicator from Market Cap and GDP
- [ ] Implement multi-country line chart with color encoding by tiers
- [ ] Add shaded reference bands (0-20%, 20-60%, >60%)
- [ ] Add hover tooltips with GDP per capita
- [ ] Implement view toggle (Line chart vs Scatter plot)
- [ ] Add annotations for structural breaks (2014-2016, 2020)
- [ ] Implement filters (Country, Region, Year range)
- [ ] Create Map View tab
- [ ] Create Data Table tab
- [ ] Add supporting information layers

---

## Indicator 4.3.1.2: Portfolio Investment Bonds
**Status:** ⏳ **TO IMPLEMENT**

**Location:** Tab 1

### Specification Details:
- **Analytical Focus Question:** How much do African economies rely on external bond markets for financing, and how volatile or sustainable are these flows over time?
- **Graph Type:** Multi-country line chart (log scale) to track magnitude and volatility
- **X-axis:** Year
- **Y-axis:** Portfolio Investment, Bonds (log scale recommended)
- **Color Encoding:**
  - #0072BC → Moderate & stable inflows (sustainable financing)
  - #FFD34E → Increasing exposure (watch zone)
  - #F26C2B → Volatile or large inflows (risk & dependency)
- **Interactivity:**
  - Hover Tooltip: {Country, Year, Portfolio Bond Inflows (US$), % of GDP, Year-on-Year Change (%)}
  - Hover Highlight: Emphasizes hovered line, dims others
- **Filters:**
  - Country Dropdown Selector
  - Year Range Slider (2000–2023)
  - Region Toggle
  - Metric Toggle: Switch between Absolute inflows (US$) and Inflows as % of GDP
- **Features:**
  - Highlight major global shocks (2008, 2014, 2020)
  - Annotate issuance booms (Eurobond waves)
  - Shaded region for high-risk exposure (>10% GDP)
- **How to Read:** Each line or area shows the scale of foreign bond inflows (public and private) over time. Sharp spikes indicate borrowing surges or foreign investor interest; sudden drops reveal exposure to global financial shocks.
- **Analytical Lens:**
  - Efficiency: Sustainable portfolios show stable inflows tied to investment and growth.
  - Effectiveness: Overreliance or volatility signals vulnerability — external debt servicing risks and limited domestic absorption capacity.

### Implementation Checklist:
- [ ] Create unified dashboard structure
- [ ] Implement multi-country line chart with log scale
- [ ] Add metric toggle (Absolute US$ vs % of GDP)
- [ ] Color encode by risk level (stable, increasing, volatile)
- [ ] Add hover tooltips with year-on-year change
- [ ] Highlight major shocks (2008, 2014, 2020)
- [ ] Add shaded region for high-risk exposure (>10% GDP)
- [ ] Implement filters (Country, Region, Year range)
- [ ] Create Map View tab
- [ ] Create Data Table tab
- [ ] Add supporting information layers

---

## Indicator 4.3.1.3: Adequacy of International Reserves
**Status:** ⏳ **TO IMPLEMENT**

**Location:** Tab 1

### Specification Details:
- **Analytical Focus Question:** Do countries hold enough reserves to manage short-term debt obligations, ensuring macro-financial stability and policy autonomy?
- **Graph Type:** Ratio-based line chart (multi-country) or diverging bar chart (latest year), Optional: heatmap for multi-year comparison
- **X-axis:** Year (or Country for bar chart)
- **Y-axis:** Reserve Adequacy Ratio (Reserves / Short-Term Debt)
- **Color Encoding:**
  - #007B33 → ≥100% (Adequate coverage – resilient)
  - #FFD34E → 50–99% (Moderate coverage – vulnerable)
  - #F26C2B → <50% (Insufficient reserves – high risk)
- **Interactivity:**
  - Hover Tooltip: {Country, Year, Reserve Adequacy Ratio, Reserves US$, Short-term Debt US$}
  - Hover Highlight: brightens selected country line/bar
  - Reference Line @ y = 1: visual benchmark for "full coverage"
- **Filters:**
  - Country Dropdown
  - Year Slider (2000 → 2023)
  - View Toggle: Trend View (line chart) vs Snapshot View (diverging bar chart)
  - Facet Toggle: switch between Economic Structure and Region
- **Features:**
  - Reference line at ratio = 1 (full short-term coverage)
  - Shaded bands for risk tiers (red/orange/green)
  - Annotate crisis years (2008, 2014 commodity slump, 2020 pandemic)
- **How to Read:** Each country's line shows how much of its short-term external debt could be covered by its reserves. Ratios above 1 mean full coverage; lower values suggest vulnerability to external liquidity shocks.
- **Analytical Lens:**
  - Efficiency: Stable or rising ratios reflect disciplined reserve accumulation without overburdening fiscal space.
  - Effectiveness: Adequate reserves enable governments to absorb external shocks — a sign of resilient and self-reliant financial governance.

### Implementation Checklist:
- [ ] Create unified dashboard structure
- [ ] Calculate indicator from Reserves and Short-Term Debt
- [ ] Implement line chart with color encoding by adequacy tiers
- [ ] Add reference line at ratio = 1
- [ ] Add shaded bands for risk tiers
- [ ] Implement view toggle (Trend vs Snapshot/Bar chart)
- [ ] Add hover tooltips with component values
- [ ] Annotate crisis years (2008, 2014, 2020)
- [ ] Implement filters (Country, Year, View, Facet)
- [ ] Create Map View tab
- [ ] Create Data Table tab
- [ ] Add supporting information layers

---

## Indicator 4.3.2.1: Banking Sector Development Index
**Status:** ⏳ **TO IMPLEMENT**

**Location:** Tab 2

### Specification Details:
- **Analytical Focus Question:** How strong, stable, and effective are domestic banking systems in mobilizing and allocating capital?
- **Graph Type:** Composite index line chart (multi-country, 2000–2023)
- **X-axis:** Year
- **Y-axis:** Banking Sector Development Index (normalized scale: 0–1)
- **Color Encoding:**
  - #0072BC → High index values (strong banking development)
  - #FFD34E → Moderate development
  - #F26C2B → Weak or fragile banking systems
- **Interactivity:**
  - Hover Tooltip: {Country, Year, BSDI Value (0–1), Capital Ratio, Liquidity Ratio, Credit Ratio}
  - Hover Highlight: Brightens hovered line and component bands
  - Reference Bands:
    - 0.7–1.0 → #0072BC (High development zone)
    - 0.4–0.69 → #FFD34E (Moderate development zone)
    - < 0.4 → #F26C2B (Weak development zone)
- **Filters:**
  - Country Selector: Select 1–3 countries for direct overlay comparison
  - Year Range Slider (2000–2023)
  - Region Toggle: Switch between "Single Country View" and "Regional Average View"
- **Features:**
  - Add reference bands for "High / Medium / Low" development
  - Tooltip expansion showing component contribution (Capital, Liquidity, Credit)
- **How to Read:** Each line shows the evolution of a country's banking sector strength — combining capital adequacy, liquidity, and credit depth into a single index. A higher index means more resilient and efficient banking systems.
- **Analytical Lens:**
  - Efficiency: Stable or improving BSDI values show well-capitalized banks using assets efficiently.
  - Effectiveness: Growth in BSDI signals banks effectively channel savings into productive lending, supporting inclusive development.

### Implementation Checklist:
- [ ] Create unified dashboard structure
- [ ] Calculate BSDI from component indicators (40% Capital, 30% Liquidity, 30% Credit)
- [ ] Implement line chart with color encoding by development tiers
- [ ] Add reference bands (0.7-1.0, 0.4-0.69, <0.4)
- [ ] Add hover tooltips with component breakdown
- [ ] Implement filters (Country, Year range, Region toggle)
- [ ] Create Map View tab
- [ ] Create Data Table tab
- [ ] Add supporting information layers

---

## Indicator 4.3.2.2: Private Sector Credit to GDP
**Status:** ⏳ **TO IMPLEMENT**

**Location:** Tab 2

### Specification Details:
- **Analytical Focus Question:** How much of a country's total economic output is financed through its domestic financial system — reflecting the role of banks and other financial institutions in supporting real-sector activity?
- **Graph Type:** Multi-country line chart (time trend)
- **X-axis:** Year
- **Y-axis:** Domestic Credit Provided by Financial Sector (% of GDP)
- **Color Encoding:**
  - #0072BC – Deep financial systems (>80% GDP)
  - #FFD34E – Moderate depth (40–80%)
  - #F26C2B – Shallow depth (<40%)
- **Interactivity:**
  - Hover Tooltip: {Country, Year, Domestic Credit (% GDP), Change since 2000, Income Group}
- **Filters:**
  - Country Dropdown: Select 1–3 countries for focused line comparison
  - Year Range Slider (1980 → 2023)
  - Facet Toggle: Switch between "By Income Group" and "By Region"
  - Benchmark Toggle: Option to overlay Regional Average or Africa-wide mean as a thin dashed orange line (#F26C2B)
- **Features:**
  - Annotate selected country examples
- **How to Read:** Each line shows the share of total GDP that flows through the domestic financial system. A higher value means the country's financial sector plays a larger role in funding businesses and households.
- **Analytical Lens:**
  - Efficiency: A growing ratio shows stronger financial intermediation — banks and institutions efficiently converting savings into loans.
  - Effectiveness: Deepening credit-to-GDP indicates broader access to finance and more inclusive economic growth.

### Implementation Checklist:
- [ ] Create unified dashboard structure
- [ ] Implement multi-country line chart
- [ ] Color encode by depth tiers (>80%, 40-80%, <40%)
- [ ] Add benchmark toggle (Regional Average overlay)
- [ ] Add hover tooltips with change since 2000
- [ ] Implement filters (Country, Year range, Facet, Benchmark)
- [ ] Create Map View tab
- [ ] Create Data Table tab
- [ ] Add supporting information layers

---

## Indicator 4.3.3.1: Pension Funds and Sovereign Wealth Funds
**Status:** ⏳ **TO IMPLEMENT**

**Location:** Tab 3

### Specification Details:
- **Analytical Focus Question:** Text-based analysis from reports
- **Graph Type:** Text-based analysis
- **Content:** Analysis of pension fund and sovereign wealth fund investment patterns

### Implementation Checklist:
- [ ] Create unified dashboard structure
- [ ] Implement text-based analysis section
- [ ] Include country examples and key trends
- [ ] Add data sources and methodology

---

## Implementation Order & Priority

### Phase 1: Tab 1 (Market Capitalization)
1. ⏳ Indicator 4.3.1.1 (Market Capitalization to GDP)
2. ⏳ Indicator 4.3.1.2 (Portfolio Investment Bonds)
3. ⏳ Indicator 4.3.1.3 (Adequacy of International Reserves)

### Phase 2: Tab 2 (Financial Intermediation)
4. ⏳ Indicator 4.3.2.1 (Banking Sector Development Index)
5. ⏳ Indicator 4.3.2.2 (Private Sector Credit to GDP)

### Phase 3: Tab 3 (Institutional Investors)
6. ⏳ Indicator 4.3.3.1 (Pension Funds and Sovereign Wealth Funds)

---

## Key Implementation Notes

### Common Patterns Across All Indicators:
1. **Unified Dashboard Structure:**
   - Indicator header with analytical focus question and info icon
   - Local filter row (Year, Country, Region, Reset)
   - Multi-view tabs (Graph View, Map View, Data Table)
   - Supporting information layers (Learn more, Analytical Lens)

2. **Color Consistency:**
   - Deep/High/Strong: #0072BC or #007B33 (blue/green)
   - Moderate/Developing: #FFD34E (yellow)
   - Shallow/Weak/High Risk: #F26C2B (orange/red)
   - Selected countries: #003366 (deep blue)
   - Regional average: #F26C2B (orange, dashed)

3. **Reference Lines/Bands:**
   - Use Plotly shapes for reference bands
   - Use annotations for reference lines
   - Semi-transparent fills for shaded zones

4. **Calculated Indicators:**
   - Market Cap to GDP: (Market Cap / GDP) * 100
   - Adequacy of Reserves: Reserves / Short-Term Debt
   - BSDI: 0.4 * Capital + 0.3 * Liquidity + 0.3 * Credit

5. **Data Requirements:**
   - Need to verify indicator labels in data
   - May need to calculate derived indicators
   - Check for GDP per capita data for scatter plot

---

## Next Steps

1. **Verify Data Availability:**
   - Check which indicators exist in `nexus.parquet`
   - Identify any missing indicators that need calculation
   - Map specification indicator names to actual data labels

2. **Start with Indicator 4.3.1.1:**
   - Implement multi-country line chart
   - Add reference bands and color encoding
   - Add view toggle for scatter plot

3. **Continue with remaining indicators in priority order**

