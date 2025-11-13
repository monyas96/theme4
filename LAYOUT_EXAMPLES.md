# Layout Examples for Different Numbers of Indicators

This document provides concrete examples for implementing pages with different numbers of indicators.

---

## Example 1: Single Indicator (1 graph)

```python
# Topic Description
st.markdown("### Topic Description")
# ... description text ...

# Orange divider before indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

st.markdown("### Key Indicators Overview")

# Single indicator - full width
with st.container():
    # Use indicator_module_template.py here
    # ... indicator code ...

# Orange divider before Data Availability
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Data Availability Section
# ... data availability code ...
```

---

## Example 2: Two Indicators (2 graphs) - Side by Side

```python
# Topic Description
st.markdown("### Topic Description")
# ... description text ...

# Orange divider before indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

st.markdown("### Key Indicators Overview")

# Two indicators - side by side
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container():
        # Indicator 4.1.1
        # Use indicator_module_template.py here
        # ... indicator code ...

with col2:
    with st.container():
        # Indicator 4.1.2
        # Use indicator_module_template.py here
        # ... indicator code ...

# Orange divider after both indicators (before Data Availability)
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Data Availability Section
# ... data availability code ...
```

---

## Example 3: Three Indicators (3 graphs) - Option A: 3 Columns

```python
# Topic Description
st.markdown("### Topic Description")
# ... description text ...

# Orange divider before indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

st.markdown("### Key Indicators Overview")

# Three indicators - 3 columns (may be cramped, consider Option B)
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with st.container():
        # Indicator 1
        # ... indicator code ...

with col2:
    with st.container():
        # Indicator 2
        # ... indicator code ...

with col3:
    with st.container():
        # Indicator 3
        # ... indicator code ...

# Orange divider after all indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Data Availability Section
# ... data availability code ...
```

---

## Example 4: Three Indicators (3 graphs) - Option B: 2+1 Layout

```python
# Topic Description
st.markdown("### Topic Description")
# ... description text ...

# Orange divider before indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

st.markdown("### Key Indicators Overview")

# Row 1: Two indicators side by side
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container():
        # Indicator 1
        # ... indicator code ...

with col2:
    with st.container():
        # Indicator 2
        # ... indicator code ...

# Orange divider after row 1
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Row 2: One indicator full width
with st.container():
    # Indicator 3
    # ... indicator code ...

# Orange divider after all indicators (before Data Availability)
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Data Availability Section
# ... data availability code ...
```

---

## Example 5: Four Indicators (4 graphs) - 2x2 Grid

```python
# Topic Description
st.markdown("### Topic Description")
# ... description text ...

# Orange divider before indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

st.markdown("### Key Indicators Overview")

# Row 1: Two indicators
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container():
        # Indicator 1
        # ... indicator code ...

with col2:
    with st.container():
        # Indicator 2
        # ... indicator code ...

# Orange divider after row 1
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Row 2: Two indicators
col3, col4 = st.columns(2, gap="large")

with col3:
    with st.container():
        # Indicator 3
        # ... indicator code ...

with col4:
    with st.container():
        # Indicator 4
        # ... indicator code ...

# Orange divider after all indicators (before Data Availability)
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Data Availability Section
# ... data availability code ...
```

---

## Example 6: Five Indicators (5 graphs) - 2+2+1 Layout

```python
# Topic Description
st.markdown("### Topic Description")
# ... description text ...

# Orange divider before indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

st.markdown("### Key Indicators Overview")

# Row 1: Two indicators
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container():
        # Indicator 1
        # ... indicator code ...

with col2:
    with st.container():
        # Indicator 2
        # ... indicator code ...

# Orange divider after row 1
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Row 2: Two indicators
col3, col4 = st.columns(2, gap="large")

with col3:
    with st.container():
        # Indicator 3
        # ... indicator code ...

with col4:
    with st.container():
        # Indicator 4
        # ... indicator code ...

# Orange divider after row 2
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Row 3: One indicator full width
with st.container():
    # Indicator 5
    # ... indicator code ...

# Orange divider after all indicators (before Data Availability)
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; width: 100%;"></div>
""", unsafe_allow_html=True)

# Data Availability Section
# ... data availability code ...
```

---

## Key Principles

1. **Always start with**: Orange divider + "Key Indicators Overview" heading
2. **Always end with**: Orange divider before Data Availability section
3. **Between rows**: Add orange divider after each row of indicators
4. **Within rows**: No dividers between side-by-side columns
5. **Session state keys**: Must be unique per indicator (use indicator number in key)

---

## Divider Placement Rules

- ✅ **DO**: Place divider before "Key Indicators Overview"
- ✅ **DO**: Place divider after each row of indicators
- ✅ **DO**: Place divider before Data Availability section
- ❌ **DON'T**: Place divider between side-by-side columns
- ❌ **DON'T**: Place dividers within an indicator module

---

## Notes

- **2-column layout** is recommended for readability (not too narrow)
- **3-column layout** can work but may be cramped on smaller screens
- **Full-width indicators** work well for complex visualizations
- **Grid layouts** (2x2, 2x3, etc.) provide good visual balance
- Always test responsive behavior on different screen sizes

