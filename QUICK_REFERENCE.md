# Quick Reference: Unified Dashboard Changes

## 🎯 Core Principle
**Each indicator is a self-contained module with its own filters, graph, and explanatory layers.**

---

## ✅ DO's

### Structure
- ✅ Use **local filters** for each indicator (Year, Country, Region, Reset)
- ✅ Use **multi-view tabs** (Graph View, Map View, Data Table)
- ✅ Place **"How to Read This Graph"** as hover button above graph
- ✅ Place **legend directly under graph** (if applicable)
- ✅ Use **orange dividers** (`#F26C2B`) between sections
- ✅ Filter to **Africa only** for all indicators
- ✅ Use **Intermediate Region Name** for region filter
- ✅ Use **session state** for filter persistence and reset

### Order of Elements
1. Indicator Header (title + info icon + analytical question)
2. Local Filter Row (Year, Country, Region, Reset)
3. Multi-View Tabs:
   - Graph View (hover button + graph + legend)
   - Map View (if applicable)
   - Data Table
4. Supporting Information:
   - "Learn more about this indicator" (first expander)
   - "Analytical Lens" (second expander)

---

## ❌ DON'Ts

- ❌ **NO global filters** on the page
- ❌ **NO "View" radio buttons** (Heatmap/Map toggle)
- ❌ **NO data source tags** (e.g., "PEFA") in filter row
- ❌ **NO "Key Insights"** expander
- ❌ **NO "Data Source and Methodology"** expander
- ❌ **NO internal dividers** within indicator sections
- ❌ **NO bottom sections** (Geographic Distribution, Key Insights)

---

## 📐 Layout Strategies

### Single Indicator (1 graph)
- Full width, no columns
- No divider between indicators

### Two Indicators (2 graphs)
- 2 columns side-by-side
- Divider after both columns close

### Three Indicators (3 graphs)
- Option A: 3 columns (if space allows)
- Option B: 2 columns + 1 full-width below
- Divider after each row

### Four+ Indicators (4+ graphs)
- Grid layout (2 columns × N rows)
- Divider after each row
- Final divider before Data Availability

## 🔧 Key Code Snippets

### Orange Divider
```python
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)
```

### Reset Button Logic
```python
if st.button("Reset", key="ind_X_X_X_reset"):
    if 'ind_X_X_X_year_filter' in st.session_state:
        del st.session_state.ind_X_X_X_year_filter
    if 'ind_X_X_X_country_filter' in st.session_state:
        del st.session_state.ind_X_X_X_country_filter
    if 'ind_X_X_X_region_filter' in st.session_state:
        del st.session_state.ind_X_X_X_region_filter
    st.rerun()
```

### Filter Application
```python
# Filter to Africa only
africa_ref_data = ref_data[ref_data['Region Name'] == 'Africa'].copy()
africa_countries = sorted(africa_ref_data['Country or Area'].unique())

# Apply filters
filtered_data = indicator_data.copy()
if selected_year_ind != "All Years":
    filtered_data = filtered_data[filtered_data['year'] == selected_year_ind]
if selected_countries_ind:
    filtered_data = filtered_data[filtered_data['country_or_area'].isin(selected_countries_ind)]
if selected_regions_ind:
    region_countries = africa_ref_data[
        africa_ref_data['Intermediate Region Name'].isin(selected_regions_ind)
    ]['Country or Area'].unique()
    filtered_data = filtered_data[filtered_data['country_or_area'].isin(region_countries)]
```

---

## 📋 Checklist for Each Indicator

- [ ] Indicator header with info icon tooltip
- [ ] Local filter row (Year, Country, Region, Reset)
- [ ] Session state initialization
- [ ] Filter application logic
- [ ] Multi-view tabs structure
- [ ] "How to Read This Graph" hover button
- [ ] Chart rendering (correct chart_type from viz spec)
- [ ] Legend (if needed, directly under graph)
- [ ] Map view (if applicable, matches graph colors)
- [ ] Data table with CSV download
- [ ] "Learn more" expander (first)
- [ ] "Analytical Lens" expander (second)
- [ ] Orange divider after indicator section

---

## 🎨 Styling Constants

- **Orange Color**: `#F26C2B`
- **Dark Blue (OSAA)**: `#002B7F`
- **PEFA Colors**:
  - A (4): `#003366` (Deep Blue)
  - B (3): `#3366CC` (Medium Blue)
  - C (2): `#99CCFF` (Light Blue)
  - D (1): `#F26C2B` (Orange)

---

## 📁 Files to Reference

1. **Template**: `UNIFIED_DASHBOARD_TEMPLATE.md` - Full documentation
2. **Code Template**: `indicator_module_template.py` - Reusable Python code
3. **Working Example**: `pages/3_topic_4_1.py` - Indicator 4.1.1 (lines ~84-506)
4. **Viz Spec**: `data/Viz specification matrix.xlsx` - Chart types and specifications

---

## 🔄 Migration Steps

1. **Remove** global filter section
2. **Remove** "View" radio buttons and data source tags
3. **Remove** "Key Insights" and "Data Source" expanders
4. **Add** local filter row with session state
5. **Add** multi-view tabs structure
6. **Convert** "How to Read" from expander to hover button
7. **Reorder** expanders (Learn more first, Analytical Lens second)
8. **Add** orange dividers
9. **Update** map view to match graph view (if applicable)
10. **Test** all filters and reset functionality

---

## 💡 Tips

- Always check `Viz specification matrix.xlsx` for the correct chart type
- Use the same color scheme for map as graph (for discrete categories)
- Keep tooltip text concise but informative
- Test filter combinations thoroughly
- Ensure map reflects graph view when both are present
- Use descriptive session state keys following the pattern `ind_X_X_X_*`

