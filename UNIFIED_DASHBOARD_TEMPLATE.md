# Unified Dashboard Structure Template

This document outlines the standardized structure for all indicator graphs across the dashboard, based on the implementation of Graph 1 (Indicator 4.1.1).

## Table of Contents
1. [Overall Page Structure](#overall-page-structure)
2. [Indicator Module Structure](#indicator-module-structure)
3. [Code Templates](#code-templates)
4. [Key Changes from Previous Version](#key-changes-from-previous-version)
5. [Implementation Checklist](#implementation-checklist)

---

## Overall Page Structure

### Page Layout Order:
1. **Topic Description** (static, at top)
2. **Orange Divider** (`st.markdown` with orange border)
3. **"Key Indicators Overview"** heading
4. **Indicator Modules** (layout depends on number of indicators - see below)
5. **Orange Divider** (after all indicator modules, before Data Availability section)
6. **Data Availability Section**

### Layout Strategies Based on Number of Indicators:

#### **Single Indicator (1 graph)**
- Use full width (no columns)
- No divider between indicators needed
- Structure: `with st.container():` → indicator module

#### **Two Indicators (2 graphs)**
- Use 2-column layout: `col1, col2 = st.columns(2, gap="large")`
- Each indicator in its own column
- No divider between columns (they're side-by-side)
- Divider appears after both columns close

#### **Three Indicators (3 graphs)**
- **Option A**: 3 columns side-by-side (if space allows)
  ```python
  col1, col2, col3 = st.columns(3, gap="large")
  ```
- **Option B**: 2 columns on top, 1 full-width below
  ```python
  col1, col2 = st.columns(2, gap="large")
  # ... indicators in col1 and col2
  st.divider()  # After first row
  # ... indicator in full width below
  ```

#### **Four or More Indicators (4+ graphs)**
- Use a grid approach:
  - 2 columns × 2 rows (for 4 indicators)
  - Or 2 columns with multiple rows
- Add orange divider after each row of indicators
- Example for 4 indicators:
  ```python
  # Row 1
  col1, col2 = st.columns(2, gap="large")
  with col1: # Indicator 1
  with col2: # Indicator 2
  st.divider()  # After row 1
  
  # Row 2
  col3, col4 = st.columns(2, gap="large")
  with col3: # Indicator 3
  with col4: # Indicator 4
  st.divider()  # After row 2 (and before Data Availability)
  ```

---

## Indicator Module Structure

Each indicator should follow this exact structure:

### A. Indicator Header
- **Title**: `Indicator X.X.X: [Name]`
- **Info Icon**: Hover tooltip with indicator description
- **Analytical Focus Question**: Styled paragraph below title

### B. Local Filter Row
- **Select Year(s)**: `st.selectbox` with "All Years" option
- **Select Country**: `st.multiselect` (Africa countries only)
- **Select Region**: `st.multiselect` (Intermediate Region Name, Africa only)
- **Reset Button**: Clears all local filters via session state deletion

### C. Multi-View Tabs
- **Graph View**: Main visualization
  - "How to Read This Graph" hover button (above graph)
  - Graph/Chart
  - Legend (if applicable, directly under graph)
- **Map View**: Choropleth map (if applicable)
  - Should reflect graph view colors/values
  - Custom legend if needed
- **Data Table**: 
  - `st.dataframe` with relevant columns
  - CSV download button

### D. Supporting Information Layers (Collapsible Expanders)
1. **"Learn more about this indicator"** (first expander)
   - Tabs: Definition, Relevance, Proxy Justification, Pillar Connection
2. **"Analytical Lens (Efficiency and Effectiveness)"** (second expander)
   - Efficiency and Effectiveness explanations

---

## Code Templates

### 1. Orange Divider Template

```python
# Orange divider
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)
```

### 2. Indicator Header Template

```python
st.markdown("""
<div class='indicator-card'>
    <h4>
        Indicator X.X.X: [Indicator Name]
        <button type="button" class="info-icon-btn" data-tooltip="[Tooltip text describing the indicator]" style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
    </h4>
    <p style="color: #555; line-height: 1.6; margin-bottom: 1rem;">
        <strong>Analytical Focus Question:</strong> [Question text]
    </p>
</div>
<style>
    .info-icon-btn {
        position: relative;
    }
    .info-icon-btn:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        white-space: normal;
        width: 250px;
        font-size: 0.9em;
        z-index: 1000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)
```

### 3. Local Filter Row Template

```python
# Initialize session state for local filters if not exists
if 'ind_X_X_X_year' not in st.session_state:
    st.session_state.ind_X_X_X_year = None
if 'ind_X_X_X_countries' not in st.session_state:
    st.session_state.ind_X_X_X_countries = []
if 'ind_X_X_X_region_filter' not in st.session_state:
    st.session_state.ind_X_X_X_region_filter = []

# Get indicator data for filter options
indicator_data = df_display[df_display['indicator_label'] == indicator_label].copy()
africa_ref_data = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
africa_countries = sorted(africa_ref_data['Country or Area'].unique()) if not africa_ref_data.empty else []
available_years_ind = sorted(indicator_data['year'].dropna().unique()) if not indicator_data.empty else []
available_regions = sorted(africa_ref_data['Intermediate Region Name'].dropna().unique()) if not africa_ref_data.empty else []

# Filter row
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 0.7])

with filter_col1:
    selected_year_ind = st.selectbox(
        "Select Year(s)",
        options=["All Years"] + available_years_ind,
        index=0,
        key="ind_X_X_X_year_filter"
    )

with filter_col2:
    selected_countries_ind = st.multiselect(
        "Select Country",
        options=africa_countries,
        default=[],
        key="ind_X_X_X_country_filter"
    )

with filter_col3:
    selected_regions_ind = st.multiselect(
        "Select Region",
        options=available_regions,
        default=[],
        key="ind_X_X_X_region_filter"
    )

with filter_col4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Reset", key="ind_X_X_X_reset", use_container_width=True):
        # Delete session state keys to reset widgets to defaults
        if 'ind_X_X_X_year_filter' in st.session_state:
            del st.session_state.ind_X_X_X_year_filter
        if 'ind_X_X_X_country_filter' in st.session_state:
            del st.session_state.ind_X_X_X_country_filter
        if 'ind_X_X_X_region_filter' in st.session_state:
            del st.session_state.ind_X_X_X_region_filter
        st.rerun()

# Apply filters to data
filtered_ind_data = indicator_data.copy()
if selected_year_ind != "All Years":
    filtered_ind_data = filtered_ind_data[filtered_ind_data['year'] == selected_year_ind]
if selected_countries_ind:
    filtered_ind_data = filtered_ind_data[filtered_ind_data['country_or_area'].isin(selected_countries_ind)]
if selected_regions_ind:
    # Filter by intermediate region
    region_countries = africa_ref_data[
        africa_ref_data['Intermediate Region Name'].isin(selected_regions_ind)
    ]['Country or Area'].unique()
    filtered_ind_data = filtered_ind_data[filtered_ind_data['country_or_area'].isin(region_countries)]
```

### 4. Multi-View Tabs Template

```python
# C. Visualization Panel with Multi-View Tabs
tab_graph, tab_map, tab_data = st.tabs(["Graph View", "Map View", "Data Table"])

with tab_graph:
    # Add "How to Read This Graph" hover button
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
        <button type="button" class="how-to-read-btn" data-tooltip="[How to read instructions]" style="background: none; border: none; cursor: help; font-size: 0.9em; color: #666; padding: 0.25rem 0.5rem; margin-left: auto;">
            How to Read This Graph <span style="font-size: 0.8em;">ℹ️</span>
        </button>
    </div>
    <style>
        .how-to-read-btn {
            position: relative;
        }
        .how-to-read-btn:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            right: 0;
            transform: translateX(0);
            background-color: #333;
            color: white;
            padding: 12px 16px;
            border-radius: 6px;
            white-space: normal;
            width: 350px;
            max-width: 90vw;
            font-size: 0.9em;
            line-height: 1.5;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            margin-bottom: 8px;
            text-align: left;
        }
        .how-to-read-btn:hover::before {
            content: '';
            position: absolute;
            bottom: 100%;
            right: 20px;
            border: 6px solid transparent;
            border-top-color: #333;
            margin-bottom: 2px;
            z-index: 1001;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render chart (use appropriate chart_type from viz spec)
    if not filtered_ind_data.empty:
        uv.render_indicator_section(
            df=filtered_ind_data,
            indicator_label=indicator_label,
            title="",
            description="",
            chart_type="[heatmap|line|bar|stacked_bar|map]",  # From viz spec
            selected_countries=selected_countries_ind if selected_countries_ind else None,
            year_range=(selected_year_ind, selected_year_ind) if selected_year_ind != "All Years" else None,
            chart_options={
                # Chart-specific options from viz spec
            },
            show_data_table=False,
            container_key="topic_X_X_ind_X_chart"
        )
        
        # Add legend if needed (directly under graph)
        # [Legend code here]
    else:
        st.info("No data available for the selected filters.")

with tab_map:
    # Map View (if applicable)
    # Should reflect graph view colors/values
    # [Map implementation here]

with tab_data:
    # Data Table
    if not filtered_ind_data.empty:
        cols_to_show = ['country_or_area', 'year', 'value']
        display_df = filtered_ind_data[[col for col in cols_to_show if col in filtered_ind_data.columns]].copy()
        # Rename columns as needed
        st.dataframe(display_df, use_container_width=True)
        
        # Export options
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"indicator_X_X_X_{selected_year_ind if selected_year_ind != 'All Years' else 'all_years'}.csv",
            mime="text/csv",
            key="ind_X_X_X_download_csv"
        )
    else:
        st.info("No data available for the selected filters.")
```

### 5. Supporting Information Layers Template

```python
# D. Supporting Information Layers (collapsible, in order)

# 1. Learn more about this indicator
with st.expander("Learn more about this indicator", expanded=False):
    tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
    with tab_def:
        st.markdown("""
        [Definition text]
        
        **Source:** [Source link]
        """)
    with tab_rel:
        st.markdown("""
        - **Efficiency**: [Efficiency explanation]
        - **Effectiveness**: [Effectiveness explanation]
        """)
    with tab_proxy:
        st.markdown("""
        [Proxy justification text]
        """)
    with tab_pillar:
        st.markdown("""
        [Pillar connection text]
        """)

# 2. Analytical Lens (Efficiency and Effectiveness)
with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
    st.markdown("""
    **Efficiency:** [Efficiency analysis text]
    
    **Effectiveness:** [Effectiveness analysis text]
    """)
```

---

## Key Changes from Previous Version

### ❌ REMOVED:
1. **Global filter section** - All filters are now local to each indicator
2. **"View" radio buttons** (Heatmap/Map toggle) - Use tabs instead
3. **Data Source tags** (e.g., "PEFA") from filter row
4. **"Key Insights" expander**
5. **"Data Source and Methodology" expander**
6. **Bottom sections** (Geographic Distribution, Key Insights at page bottom)
7. **Internal dividers** within indicator sections (header/filters/graph/expanders)

### ✅ ADDED:
1. **Local filter row** for each indicator (Year, Country, Region, Reset)
2. **Session state management** for local filters with reset functionality
3. **Multi-view tabs** (Graph View, Map View, Data Table)
4. **"How to Read This Graph" hover button** (replaces expander)
5. **Region filter** (Intermediate Region Name, Africa only)
6. **Orange dividers** (before sections, between graphs, before Data Availability)
7. **Info icon tooltip** in indicator header

### 🔄 REORDERED:
1. **"How to Read This Graph"** - Now hover button above graph (was expander)
2. **"Learn more about this indicator"** - Now first expander (was second)
3. **"Analytical Lens"** - Now second expander (was first)

### 🎨 STYLING:
1. **Orange dividers** (`#F26C2B`) instead of default gray
2. **Consistent spacing** with `margin: 1.5rem 0`
3. **Tooltip styling** for info icons and "How to Read" buttons

---

## Page-Level Implementation Guide

### Step 1: Determine Page Layout
1. Count the number of indicators on the page
2. Choose appropriate layout strategy (see "Layout Strategies" above)
3. Plan divider placement:
   - One divider before "Key Indicators Overview"
   - One divider after ALL indicator modules (before Data Availability)
   - Additional dividers between rows if using multi-row layout

### Step 2: Implement Page Structure
```python
# Topic Description (if exists)
# ... topic description code ...

# Orange divider before indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

st.markdown("### Key Indicators Overview")

# Choose layout based on number of indicators
# Example for 2 indicators:
col1, col2 = st.columns(2, gap="large")

with col1:
    # Indicator Module 1 (use template)
    # ... indicator code ...

with col2:
    # Indicator Module 2 (use template)
    # ... indicator code ...

# Orange divider after all indicators (before Data Availability)
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Data Availability Section
# ... data availability code ...
```

## Implementation Checklist

For each new indicator graph, follow this checklist:

### Pre-Implementation
- [ ] Review "Viz specification matrix.xlsx" for graph type and specifications
- [ ] Identify indicator label from data
- [ ] Gather all text content (analytical question, definitions, etc.)
- [ ] Determine if map view is applicable

### Structure Implementation
- [ ] Add orange divider before "Key Indicators Overview"
- [ ] Create indicator header with info icon and tooltip
- [ ] Implement local filter row (Year, Country, Region, Reset)
- [ ] Set up session state for filters
- [ ] Create multi-view tabs structure
- [ ] Implement Graph View tab with:
  - [ ] "How to Read This Graph" hover button
  - [ ] Chart rendering (correct chart_type from spec)
  - [ ] Legend (if applicable, directly under graph)
- [ ] Implement Map View tab (if applicable):
  - [ ] Map should reflect graph view colors/values
  - [ ] Custom legend if needed
- [ ] Implement Data Table tab:
  - [ ] Display relevant columns
  - [ ] CSV download button
- [ ] Add supporting information expanders:
  - [ ] "Learn more about this indicator" (first)
  - [ ] "Analytical Lens" (second)
- [ ] Add orange divider after indicator section

### Data & Filtering
- [ ] Filter data to Africa only
- [ ] Apply year filter (if not "All Years")
- [ ] Apply country filter (if selected)
- [ ] Apply region filter (Intermediate Region Name)
- [ ] Handle empty data states with `st.info()`

### Testing
- [ ] Test filter reset functionality
- [ ] Test all filter combinations
- [ ] Verify map matches graph view (if applicable)
- [ ] Check tooltips work correctly
- [ ] Verify CSV download works
- [ ] Test responsive design

### Final Checks
- [ ] No global filters on page
- [ ] No "View" radio buttons
- [ ] No data source tags in filter row
- [ ] No "Key Insights" or "Data Source" cards
- [ ] Orange dividers in correct positions
- [ ] All text matches specifications
- [ ] Chart type matches viz spec

---

## Session State Key Naming Convention

Use this pattern for session state keys:
- `ind_X_X_X_year_filter` - Year filter
- `ind_X_X_X_country_filter` - Country filter
- `ind_X_X_X_region_filter` - Region filter
- `ind_X_X_X_reset` - Reset button
- `ind_X_X_X_download_csv` - CSV download button

Where `X_X_X` is the indicator number (e.g., `4_1_1` for Indicator 4.1.1).

---

## Notes

1. **Chart Types**: Always use the chart type specified in "Viz specification matrix.xlsx"
2. **Map Views**: If the graph uses discrete categories (like PEFA scores), ensure the map uses the same discrete color mapping
3. **Legends**: Place legends directly under the graph, not in a separate section
4. **Tooltips**: Keep tooltip text concise but informative
5. **Reset Functionality**: Always use `del st.session_state[key]` followed by `st.rerun()` for reset buttons
6. **Africa Filtering**: Always filter to Africa countries only for all indicators
7. **Region Filter**: Always use "Intermediate Region Name" from reference data

---

## Example: Complete Indicator Module

See `pages/3_topic_4_1.py` - Indicator 4.1.1 section (lines ~84-506) for a complete working example.

