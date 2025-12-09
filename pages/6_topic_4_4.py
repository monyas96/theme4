import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
import composite_indicator_methods as cim
import universal_viz as uv
from special_pages.tab_4_4_1 import render_tab_4_4_1

# Navigation - Home button and logo
try:
    from app_core.components.navigation import render_page_logo
    render_page_logo("top-right")
except ImportError:
    pass  # Navigation not critical

# --- Load OSAA CSS ---
try:
    with open("app_core/styles/style_osaa.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# --- Data Loading ---
ref_data = uv.load_country_reference_data()
df_main = uv.load_main_data()

if df_main.empty or ref_data.empty:
    st.error("Failed to load essential data (main data or reference data). Page rendering stopped.")
    st.stop()

# --- Sidebar Filters ---
filters = uv.setup_sidebar_filters(ref_data, df_main, key_prefix="topic4_4")
df_filtered = uv.filter_dataframe_by_selections(df_main, filters, ref_data)

# ========================================
# SECTION: Topic Header with Home Button
# ========================================
# Home button styling - horizontal text in light gray box
st.markdown("""
<style>
    button[key="nav_home_topic_4_4"] {
        background: #F9FAFB !important;
        background-color: #F9FAFB !important;
        color: #555 !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        line-height: 1.4 !important;
        min-height: 40px !important;
        transition: all 0.3s ease !important;
        white-space: nowrap !important;
    }
    button[key="nav_home_topic_4_4"]:hover {
        background: #F3F4F6 !important;
        background-color: #F3F4F6 !important;
        border-color: #D1D5DB !important;
    }
</style>
""", unsafe_allow_html=True)

home_col, title_col = st.columns([0.15, 3.85])

with home_col:
    if st.button("Home", key="nav_home_topic_4_4", use_container_width=True):
        st.switch_page("pages/00_prototype_switcher.py")

with title_col:
    st.markdown("""
    <div class="section-header">
        <h1>Topic 4.4: Illicit Financial Flows (IFFs)</h1>
        <p>This section analyzes illicit financial flows (IFFs) in Africa, including their magnitude, types, and enforcement measures. IFFs undermine domestic resource mobilization, erode trust in institutions, and hinder sustainable development. Understanding and combating IFFs is crucial for achieving fiscal stability and development goals.</p>
    </div>
    """, unsafe_allow_html=True)

# Use filtered data directly (no global filters)
df_display = df_filtered.copy()

# ========================================
# SECTION: Key Indicators (Tabs)
# ========================================
# Add orange divider before indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
""", unsafe_allow_html=True)

st.markdown("### Key Indicators Overview")

# Create tabs for each sub-topic (matching Topic 4.3 structure)
tab_subtopic_1, tab_subtopic_2, tab_subtopic_3, tab_subtopic_4, tab_subtopic_5, tab_subtopic_6 = st.tabs([
    "Sub-topic 4.4.1 – Magnitude of IFFs",
    "Sub-topic 4.4.2 – Channels of IFFs",
    "Sub-topic 4.4.3 – Detection & Enforcement",
    "Sub-topic 4.4.4 – Transparency & Accountability",
    "Sub-topic 4.4.5 – Financing Resilience",
    "Sub-topic 4.4.6 – Sector-Specific Analysis"
])

# Add CSS to remove white space
st.markdown("""
<style>
    /* Remove excessive margins and padding */
    .element-container {
        margin-bottom: 0.25rem !important;
        padding-bottom: 0.25rem !important;
    }
    
    /* Remove white space between markdown elements */
    .stMarkdown {
        margin-bottom: 0.15rem !important;
        margin-top: 0.15rem !important;
    }
    
    /* Ensure indicator cards have minimal spacing */
    .indicator-card {
        margin-bottom: 0.5rem !important;
        padding-bottom: 0.25rem !important;
    }
    
    .indicator-card h4 {
        margin-bottom: 0.5rem !important;
    }
    
    .indicator-card p {
        margin-bottom: 0.75rem !important;
        line-height: 1.5 !important;
    }
    
    /* Ensure tabs have minimal spacing */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Reduce spacing in expanders */
    .streamlit-expanderHeader {
        margin-bottom: 0.25rem !important;
    }
    
    /* Make charts fill available space */
    .js-plotly-plot {
        margin: 0 !important;
    }
    
    /* Info icon tooltip styling */
    .info-icon-btn {
        position: relative;
    }
    
    .info-icon-btn::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: white;
        padding: 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s;
        z-index: 1000;
        margin-bottom: 0.5rem;
    }
    
    .info-icon-btn:hover::after {
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# SUB-TOPIC 4.4.1 – Magnitude of IFFs
# ========================================
with tab_subtopic_1:
    # Create sub-tabs for the two indicators under 4.4.1
    subtab_441_1, subtab_441_2 = st.tabs([
        "4.4.1.1 – IFFs as % of GDP",
        "4.4.1.2 – Annual IFF Volume"
    ])
    
    # ========================================
    # SUB-TAB 1: Indicator 4.4.1.1 - IFFs as % of GDP
    # ========================================
    with subtab_441_1:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class='indicator-card'>
                <h4>
                    Indicator 4.4.1.1: IFFs as Percentage of GDP
                    <button type="button" class="info-icon-btn" data-tooltip="Illicit financial flows (IFFs) are cross-border movements of money that are illegal in origin, transfer, or use. This includes tax evasion, trade mispricing, corruption, and proceeds from criminal activity. Measuring IFFs as a percentage of GDP helps contextualize their relative economic burden on countries." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> What share of national GDP is estimated to leave through illicit financial channels?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # C. Content (Text-based indicator)
            st.markdown("""
            <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 6px; margin-bottom: 1rem; border-left: 4px solid #0072BC;">
                <p style="margin: 0; color: #555; font-size: 0.95em;">
                    <strong>Data Source:</strong> This indicator is based on qualitative sources and text-based analysis from reports.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="line-height: 1.8; color: #333;">
            <h5 style="color: #003366; margin-top: 1rem; margin-bottom: 0.5rem;">Definition</h5>
            <p style="margin-bottom: 1rem;">
            Illicit financial flows (IFFs) are cross-border movements of money that are illegal in origin, transfer, or use. This includes tax evasion, trade mispricing, corruption, and proceeds from criminal activity. Measuring IFFs as a percentage of GDP helps contextualize their relative economic burden on countries.
            </p>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Africa-wide Estimates</h5>
            <ul style="margin-bottom: 1rem; padding-left: 1.5rem;">
                <li>Africa loses an estimated <strong>3.7% of its GDP annually</strong> to IFFs, based on mid-2010s data.</li>
                <li>Over the period 2000–2015, the average was around <strong>2.6% of GDP</strong>, suggesting the scale of the problem has grown.</li>
                <li>This ratio is among the highest globally, indicating that IFFs are a major systemic drain on Africa's economies.</li>
            </ul>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Regional Variations</h5>
            <ul style="margin-bottom: 1rem; padding-left: 1.5rem;">
                <li><strong>West Africa:</strong> Median IFFs reach <strong>10.3% of GDP</strong>, the highest in the continent.</li>
                <li><strong>North Africa:</strong> Experiences the lowest relative levels, at around <strong>2.7% of GDP</strong>.</li>
            </ul>
            <p style="margin-bottom: 1rem; font-style: italic; color: #666;">
            These differences often reflect sectoral exposure (e.g. extractives), institutional quality, and tax base structure.
            </p>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Policy Relevance</h5>
            <p style="margin-bottom: 1rem;">
            IFFs of this magnitude reduce fiscal space, increase debt dependence, and compromise SDG financing. Reducing IFFs could recapture significant domestic resources for investment in health, education, and infrastructure.
            </p>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Sources & Footnotes</h5>
            <p style="margin-bottom: 1rem; font-size: 0.9em; color: #666;">
            UNCTAD (2020). Economic Development in Africa Report: Tackling Illicit Financial Flows for Sustainable Development in Africa, p. 3, 24, 28–29, 52.
            </p>
            </div>
            """, unsafe_allow_html=True)
            
            # D. Supporting Information Layers
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
                    Illicit financial flows (IFFs) are cross-border movements of money that are illegal in origin, transfer, or use. This includes tax evasion, trade mispricing, corruption, and proceeds from criminal activity. Measuring IFFs as a percentage of GDP helps contextualize their relative economic burden on countries.
                    """)
                with tab_rel:
                    st.markdown("""
                    - **Efficiency**: Understanding IFF magnitude helps identify systemic leakages that reduce fiscal efficiency.
                    - **Effectiveness**: Tracking IFF trends assesses how well governance and enforcement systems prevent illicit outflows.
                    """)
                with tab_proxy:
                    st.markdown("""
                    Text-based analysis from UNCTAD reports provides estimates of IFF magnitude as a percentage of GDP.
                    """)
                with tab_pillar:
                    st.markdown("""
                    Under Theme 4: Ownership and Financial Sovereignty, this indicator measures the scale of illicit financial flows that erode domestic resources and undermine sustainable financing capacity.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
                **Efficiency:** Understanding IFF magnitude helps identify systemic leakages that reduce fiscal efficiency. Countries with lower IFF-to-GDP ratios demonstrate more effective resource retention and better institutional capacity to prevent illicit outflows.
                
                **Effectiveness:** Tracking IFF trends assesses how well governance and enforcement systems prevent illicit outflows. Declining IFF ratios over time indicate successful implementation of anti-IFF measures, stronger financial transparency, and improved regulatory frameworks.
                """)
    
    # ========================================
    # SUB-TAB 2: Indicator 4.4.1.2 - Annual IFF Volume
    # ========================================
    with subtab_441_2:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class='indicator-card'>
                <h4>
                    Indicator 4.4.1.2: Annual IFF Volume
                    <button type="button" class="info-icon-btn" data-tooltip="UNCTAD estimates that Africa loses approximately USD 88.6 billion each year through illicit financial flows. This far exceeds the annual aid inflows (~USD 48 billion) and foreign direct investment (~USD 54 billion) received by the continent." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> How large are illicit financial outflows each year, and how do they vary across countries and over time?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # C. Content (Text-based indicator)
            st.markdown("""
            <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 6px; margin-bottom: 1rem; border-left: 4px solid #0072BC;">
                <p style="margin: 0; color: #555; font-size: 0.95em;">
                    <strong>Data Source:</strong> This indicator is based on qualitative sources and text-based analysis from reports.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="line-height: 1.8; color: #333;">
            <h5 style="color: #003366; margin-top: 1rem; margin-bottom: 0.5rem;">Estimate</h5>
            <p style="margin-bottom: 1rem;">
            UNCTAD estimates that Africa loses approximately <strong>USD 88.6 billion each year</strong> through illicit financial flows. This far exceeds the annual aid inflows (~USD 48 billion) and foreign direct investment (~USD 54 billion) received by the continent.
            </p>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Country-Level Figures (2013–2015)</h5>
            <ul style="margin-bottom: 1rem; padding-left: 1.5rem;">
                <li><strong>Nigeria:</strong> USD 41 billion</li>
                <li><strong>Egypt:</strong> USD 17.5 billion</li>
                <li><strong>South Africa:</strong> USD 14.1 billion</li>
            </ul>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Cumulative Losses</h5>
            <p style="margin-bottom: 1rem;">
            From 2000–2015, cumulative IFFs from Africa amounted to about <strong>USD 836 billion</strong>.
            </p>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Main Channels of IFFs</h5>
            <ul style="margin-bottom: 1rem; padding-left: 1.5rem;">
                <li><strong>Commercial Tax Practices</strong> (e.g. trade mispricing, profit shifting): ~65% of total IFFs</li>
                <li><strong>Corruption-related flows:</strong> Bribery, embezzlement, and public sector theft</li>
                <li><strong>Illicit Markets and Smuggling:</strong> Drugs, arms, wildlife, etc.</li>
                <li><strong>Terrorist Financing and Criminal Proceeds</strong></li>
            </ul>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Sector Spotlight – Extractives</h5>
            <p style="margin-bottom: 1rem;">
            In 2015, under-invoicing of African extractive exports accounted for <strong>USD 40 billion in losses</strong> — with gold alone representing 77% of the total mispriced value.
            </p>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Policy Implications</h5>
            <p style="margin-bottom: 1rem;">
            IFFs deprive Africa of the financial means to achieve sustainable development. Combatting IFFs would directly support SDG 16.4 and unlock billions in domestic resources. Targeted policies in financial transparency, tax reform, anti-money laundering, and global asset recovery are critical.
            </p>
            
            <h5 style="color: #003366; margin-top: 1.5rem; margin-bottom: 0.5rem;">Sources & Footnotes</h5>
            <p style="margin-bottom: 1rem; font-size: 0.9em; color: #666;">
            UNCTAD (2020). Economic Development in Africa Report: Tackling Illicit Financial Flows for Sustainable Development in Africa, p. 3, 24, 25, 28–29, 35, 40, 44, 52.
            </p>
            </div>
            """, unsafe_allow_html=True)
            
            # D. Supporting Information Layers
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
                    UNCTAD estimates that Africa loses approximately USD 88.6 billion each year through illicit financial flows. This far exceeds the annual aid inflows (~USD 48 billion) and foreign direct investment (~USD 54 billion) received by the continent.
                    """)
                with tab_rel:
                    st.markdown("""
                    - **Efficiency**: Understanding annual IFF volume helps quantify the scale of resource leakage that reduces fiscal efficiency.
                    - **Effectiveness**: Tracking IFF volumes assesses how well enforcement systems prevent illicit outflows and protect domestic resources.
                    """)
                with tab_proxy:
                    st.markdown("""
                    Text-based analysis from UNCTAD reports provides estimates of annual IFF volume in absolute terms.
                    """)
                with tab_pillar:
                    st.markdown("""
                    Under Theme 4: Ownership and Financial Sovereignty, this indicator quantifies the absolute magnitude of illicit financial flows that erode domestic resources and undermine sustainable financing capacity.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
                **Efficiency:** Understanding annual IFF volume helps quantify the scale of resource leakage that reduces fiscal efficiency. Countries with lower absolute IFF volumes relative to their economic size demonstrate more effective resource retention and better institutional capacity to prevent illicit outflows.
                
                **Effectiveness:** Tracking IFF volumes assesses how well enforcement systems prevent illicit outflows and protect domestic resources. Declining IFF volumes over time indicate successful implementation of anti-IFF measures, stronger financial transparency, improved regulatory frameworks, and enhanced cross-border cooperation.
                """)

# ========================================
# SUB-TOPIC 4.4.2 – Channels of IFFs
# ========================================
with tab_subtopic_2:
    # Create sub-tabs for the four indicators under 4.4.2
    subtab_442_1, subtab_442_2, subtab_442_3, subtab_442_4 = st.tabs([
        "4.4.2.1 – Trade Mispricing",
        "4.4.2.2 – Tax Evasion",
        "4.4.2.3 – Criminal Activities",
        "4.4.2.4 – Corruption and Bribery"
    ])
    
    # ========================================
    # SUB-TAB 1: Indicator 4.4.2.1 - Trade Mispricing
    # ========================================
    with subtab_442_1:
        with st.container():
            # A. Indicator Header
            st.markdown("""
        <div class='indicator-card'>
                <h4>
                    Indicator 4.4.2.1: Trade Mispricing
                    <button type="button" class="info-icon-btn" data-tooltip="Trade mispricing is a major channel of Illicit Financial Flows (IFFs), where goods are intentionally over- or under-valued to shift profits abroad or avoid taxes. This indicator measures the volume and value of trade mispricing activities detected." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> How much wealth is lost through trade mispricing — a major channel of Illicit Financial Flows (IFFs) — and how do these losses differ across countries and trading relationships?
            </p>
        </div>
        """, unsafe_allow_html=True)
        
            # B. Local Filter Row
            col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([2, 2, 2, 1])
            
            with col_filter1:
                # Year filter
                available_years = sorted(df_filtered['year'].dropna().unique()) if not df_filtered.empty else []
                if available_years:
                    default_year_idx = len(available_years) - 1 if available_years else 0
                    if 'ind_4_4_2_1_year_filter' not in st.session_state:
                        st.session_state.ind_4_4_2_1_year_filter = available_years[default_year_idx] if available_years else None
                    selected_year = st.selectbox(
                        "Select Year(s)",
                        options=available_years,
                        index=available_years.index(st.session_state.ind_4_4_2_1_year_filter) if st.session_state.ind_4_4_2_1_year_filter in available_years else default_year_idx,
                        key="ind_4_4_2_1_year_filter"
                    )
                else:
                    selected_year = None
            
            with col_filter2:
                # Country filter
                africa_countries_list = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
                available_countries = sorted([c for c in df_filtered['country_or_area'].unique() if c in africa_countries_list]) if not df_filtered.empty else []
                if 'ind_4_4_2_1_country_filter' not in st.session_state:
                    st.session_state.ind_4_4_2_1_country_filter = []
                selected_countries = st.multiselect(
                    "Select Country",
                    options=available_countries,
                    default=st.session_state.ind_4_4_2_1_country_filter,
                    key="ind_4_4_2_1_country_filter"
                )
            
            with col_filter3:
                # Region filter
                available_regions = sorted(ref_data[ref_data['Region Name'] == 'Africa']['Intermediate Region Name'].dropna().unique())
                if 'ind_4_4_2_1_region_filter' not in st.session_state:
                    st.session_state.ind_4_4_2_1_region_filter = []
                selected_regions = st.multiselect(
                    "Select Region",
                    options=available_regions,
                    default=st.session_state.ind_4_4_2_1_region_filter,
                    key="ind_4_4_2_1_region_filter"
                )
            
            with col_filter4:
                st.markdown("<br>", unsafe_allow_html=True)  # Spacing
                if st.button("Reset", key="ind_4_4_2_1_reset"):
                    if 'ind_4_4_2_1_year_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_1_year_filter
                    if 'ind_4_4_2_1_country_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_1_country_filter
                    if 'ind_4_4_2_1_region_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_1_region_filter
                    st.rerun()
            
            # Filter data
            indicator_data_442_1 = df_filtered.copy()
            
            # Define trade mispricing indicators
            trade_mispricing_indicators = {
                "Developing vs Advanced Economies (USD Millions)": {
                    "label": "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, in USD Millions",
                    "code": "GFI.TableA.gap_usd_adv",
                    "color": "#0072BC"
                },
                "Global Trading Partners (USD Millions)": {
                    "label": "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and all of their Global Trading Partners, 2009–2018 in USD Millions",
                    "code": "GFI.TableE.gap_usd_all",
                    "color": "#F26C2B"
                },
                "Developing vs Advanced Economies (% of Total Trade)": {
                    "label": "The Total Value Gaps Identified Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, as a Percent of Total Trade",
                    "code": "GFI.TableC.gap_pct_adv",
                    "color": "#0072BC"
                },
                "Global Trading Partners (% of Total Trade)": {
                    "label": "The Total Value Gaps Identified in Trade Between 134 Developing Countries and all of their Trading Partners, 2009–2018 as a Percent of Total Trade",
                    "code": "GFI.TableG.gap_pct_all",
                    "color": "#F26C2B"
                }
            }
            
            # C. Multi-View Tabs
            tab_graph_442_1, tab_map_442_1, tab_table_442_1 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_442_1:
                # View toggle: Absolute vs Relative
                view_toggle = st.radio(
                    "View Type",
                    options=["Absolute Value (USD Millions)", "Relative (% of Total Trade)"],
                    horizontal=True,
                    key="ind_4_4_2_1_view_toggle"
                )
                
                # Filter indicators based on view
                if view_toggle == "Absolute Value (USD Millions)":
                    available_indicators = {k: v for k, v in trade_mispricing_indicators.items() if "USD Millions" in k}
                else:
                    available_indicators = {k: v for k, v in trade_mispricing_indicators.items() if "% of Total Trade" in k}
                
                selected_indicator_name = st.selectbox(
                "Select Trade Mispricing Indicator:",
                    options=list(available_indicators.keys()),
                    key="ind_4_4_2_1_indicator_select"
                )
                
                indicator_details = available_indicators[selected_indicator_name]
                
                # Filter data for selected indicator
                chart_data = indicator_data_442_1[
                    indicator_data_442_1['indicator_label'] == indicator_details["label"]
                ].copy()
                
                if selected_countries:
                    chart_data = chart_data[chart_data['country_or_area'].isin(selected_countries)]
                if selected_regions:
                    region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                    chart_data = chart_data[chart_data['country_or_area'].isin(region_countries)]
                
                if not chart_data.empty:
                    # Create chart based on view type
                    if view_toggle == "Absolute Value (USD Millions)":
                        # Horizontal grouped bar chart: y-axis=Country, x-axis=Value, color=Year
                        fig = go.Figure()
                        
                        # Group by year and country
                        years = sorted(chart_data['year'].unique())
                        countries = sorted(chart_data['country_or_area'].unique())
                        
                        # OSAA color palette for years
                        osaa_colors = [
                            '#003366',  # Deep Blue
                            '#0072BC',  # Mid Blue
                            '#3366CC',  # Medium Blue
                            '#99CCFF',  # Light Blue
                            '#F26C2B',  # Orange
                            '#FFD34E',  # Yellow
                            '#007B33',  # Green
                            '#002B7F',  # Dark Blue
                        ]
                        
                        # Assign colors to years (cycle through palette if more years than colors)
                        year_colors = {}
                        for idx, year in enumerate(years):
                            year_colors[year] = osaa_colors[idx % len(osaa_colors)]
                        
                        # Add a trace for each year
                        for year in years:
                            year_data = chart_data[chart_data['year'] == year]
                            country_values = []
                            # Ensure all countries are included, even if no data for that year
                            for country in countries:
                                country_row = year_data[year_data['country_or_area'] == country]
                                if len(country_row) > 0:
                                    country_values.append(country_row['value'].values[0])
                                else:
                                    country_values.append(0)  # Use 0 if no data for this country-year
                            
                            fig.add_trace(go.Bar(
                                y=countries,
                                x=country_values,
                                name=str(int(year)),
                                orientation='h',
                                marker_color=year_colors.get(year, indicator_details["color"]),
                                hovertemplate=f"<b>%{{y}}</b><br>Year: {int(year)}<br>Value: %{{x:,.0f}} USD Millions<br><extra></extra>"
                            ))
                        
                        fig.update_layout(
                            title=f"Trade Mispricing: {selected_indicator_name}",
                            xaxis_title="Value Gap (USD Millions)",
                            yaxis_title="Country",
                            barmode='stack',
                            height=max(500, len(countries) * 30),  # Adjust height based on number of countries
                            hovermode='closest',
                            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
                            yaxis=dict(categoryorder='total ascending')  # Sort countries by total value
                        )
                    else:
                        # Line chart for % of Total Trade (like old implementation)
                        fig = go.Figure()
                        
                        countries = sorted(chart_data['country_or_area'].unique())
                        for country in countries:
                            country_data = chart_data[chart_data['country_or_area'] == country].sort_values('year')
                            fig.add_trace(go.Scatter(
                                x=country_data['year'],
                                y=country_data['value'],
                                mode='lines+markers',
                                name=country,
                                line=dict(color=indicator_details["color"], width=2),
                                hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>Value: %{{y:.2f}}%<br><extra></extra>"
                            ))
                        
                        fig.update_layout(
                            title=f"Trade Mispricing: {selected_indicator_name}",
                            xaxis_title="Year",
                            yaxis_title="Percent of Total Trade",
                            height=500,
                            hovermode='closest',
                            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
                        )
                    
                    st.plotly_chart(fig, use_container_width=True, key="plot_442_1_graph")
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_map_442_1:
                # Map view
                view_toggle_map = st.radio(
                    "View Type",
                    options=["Absolute Value (USD Millions)", "Relative (% of Total Trade)"],
                    horizontal=True,
                    key="ind_4_4_2_1_view_toggle_map"
                )
                
                if view_toggle_map == "Absolute Value (USD Millions)":
                    available_indicators_map = {k: v for k, v in trade_mispricing_indicators.items() if "USD Millions" in k}
                else:
                    available_indicators_map = {k: v for k, v in trade_mispricing_indicators.items() if "% of Total Trade" in k}
                
                selected_indicator_name_map = st.selectbox(
                    "Select Trade Mispricing Indicator:",
                    options=list(available_indicators_map.keys()),
                    key="ind_4_4_2_1_indicator_select_map"
                )
                
                indicator_details_map = available_indicators_map[selected_indicator_name_map]
                
                # Year selector for map (allow all years or specific year)
                map_years = sorted(indicator_data_442_1['year'].dropna().unique()) if not indicator_data_442_1.empty else []
                if map_years:
                    selected_map_year = st.selectbox(
                        "Select Year for Map:",
                        options=["All Years"] + [str(int(y)) for y in map_years],
                        index=len(map_years),  # Default to "All Years" (latest)
                        key="ind_4_4_2_1_map_year"
                    )
                else:
                    selected_map_year = None
                
                map_data = indicator_data_442_1[
                    indicator_data_442_1['indicator_label'] == indicator_details_map["label"]
                ].copy()
                
                # Ensure year is numeric before filtering
                map_data['year'] = pd.to_numeric(map_data['year'], errors='coerce')
                
                # Apply filters
                if selected_map_year and selected_map_year != "All Years":
                    selected_year_num = float(selected_map_year)
                    map_data = map_data[map_data['year'] == selected_year_num]
                if selected_countries:
                    map_data = map_data[map_data['country_or_area'].isin(selected_countries)]
                if selected_regions:
                    region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                    map_data = map_data[map_data['country_or_area'].isin(region_countries)]
                
                if not map_data.empty:
                    # If "All Years" selected, aggregate by country (sum or average)
                    if selected_map_year == "All Years":
                        map_data_agg = map_data.groupby('country_or_area')['value'].sum().reset_index()
                        map_data_agg['year'] = 'All Years'
                        map_data_display = map_data_agg
                    else:
                        map_data_display = map_data.copy()
                    
                    # Remove rows with missing values
                    map_data_display = map_data_display.dropna(subset=['value'])
                    
                    if not map_data_display.empty:
                        # Merge with reference data for ISO codes using inner join
                        africa_ref = ref_data[ref_data['Region Name'] == 'Africa'].copy()
                        if not africa_ref.empty and 'Country or Area' in africa_ref.columns:
                            map_data_merged = map_data_display.merge(
                                africa_ref[['Country or Area', 'iso3']],
                                left_on='country_or_area',
                                right_on='Country or Area',
                                how='inner'
                            )
                            
                            if not map_data_merged.empty:
                                # Determine the correct ISO column name after merge
                                iso_col = 'iso3_y' if 'iso3_y' in map_data_merged.columns else ('iso3_x' if 'iso3_x' in map_data_merged.columns else 'iso3')
                                if iso_col != 'iso3' and iso_col in map_data_merged.columns:
                                    map_data_merged['iso3'] = map_data_merged[iso_col]
                                
                                # Filter out rows with missing ISO codes
                                map_data_merged = map_data_merged[map_data_merged['iso3'].notna()]
                                
                                if not map_data_merged.empty:
                                    fig = px.choropleth(
                                        map_data_merged,
                                        locations='iso3',
                                        color='value',
                                        hover_name='country_or_area',
                                        hover_data={'year': True, 'value': ':,.0f'},
                                        color_continuous_scale='Blues',
                                        title=f"Geographical Distribution: {selected_indicator_name_map}" + (f" ({selected_map_year})" if selected_map_year != "All Years" else " (All Years - Sum)")
                                    )
                                    fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="lightgray")
                                    fig.update_layout(height=600, margin=dict(l=0, r=0, t=40, b=0))
                                    st.plotly_chart(fig, use_container_width=True, key="plot_442_1_map")
                                else:
                                    st.info("No geographic data available for mapping after filtering ISO codes.")
                            else:
                                st.info("No matching countries found between data and reference data.")
                        else:
                            st.info("No reference data available for mapping.")
                    else:
                        st.info("No data available after removing missing values.")
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_table_442_1:
                # Data table
                view_toggle_table = st.radio(
                    "View Type",
                    options=["Absolute Value (USD Millions)", "Relative (% of Total Trade)"],
                    horizontal=True,
                    key="ind_4_4_2_1_view_toggle_table"
                )
                
                if view_toggle_table == "Absolute Value (USD Millions)":
                    available_indicators_table = {k: v for k, v in trade_mispricing_indicators.items() if "USD Millions" in k}
                else:
                    available_indicators_table = {k: v for k, v in trade_mispricing_indicators.items() if "% of Total Trade" in k}
                
                selected_indicator_name_table = st.selectbox(
                    "Select Trade Mispricing Indicator:",
                    options=list(available_indicators_table.keys()),
                    key="ind_4_4_2_1_indicator_select_table"
                )
                
                indicator_details_table = available_indicators_table[selected_indicator_name_table]
                
                # Table view toggle: Long format vs Pivot format
                table_format = st.radio(
                    "Table Format:",
                    options=["Long Format (Country × Year)", "Pivot Format (Years as Columns)"],
                    horizontal=True,
                    key="ind_4_4_2_1_table_format"
                )
                
                table_data = indicator_data_442_1[
                    indicator_data_442_1['indicator_label'] == indicator_details_table["label"]
                ].copy()
                
                # Apply filters
                if selected_countries:
                    table_data = table_data[table_data['country_or_area'].isin(selected_countries)]
                if selected_regions:
                    region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                    table_data = table_data[table_data['country_or_area'].isin(region_countries)]
                
                if not table_data.empty:
                    if table_format == "Long Format (Country × Year)":
                        # Long format: Country, Year, Value
                        display_table = table_data[['country_or_area', 'year', 'value']].copy()
                        display_table = display_table.sort_values(['country_or_area', 'year'])
                        display_table = display_table.rename(columns={
                            'country_or_area': 'Country',
                            'year': 'Year',
                            'value': 'Value (USD Millions)' if view_toggle_table == "Absolute Value (USD Millions)" else 'Value (% of Total Trade)'
                        })
                        # Format values
                        if view_toggle_table == "Absolute Value (USD Millions)":
                            display_table['Value (USD Millions)'] = display_table['Value (USD Millions)'].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "")
                        else:
                            display_table['Value (% of Total Trade)'] = display_table['Value (% of Total Trade)'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "")
                    else:
                        # Pivot format: Countries as rows, Years as columns
                        pivot_table = table_data.pivot_table(
                            index='country_or_area',
                            columns='year',
                            values='value',
                            aggfunc='first'
                        ).reset_index()
                        pivot_table.columns.name = None
                        pivot_table = pivot_table.rename(columns={'country_or_area': 'Country'})
                        # Sort by country name
                        pivot_table = pivot_table.sort_values('Country')
                        # Format column names (years) as integers
                        new_columns = []
                        for col in pivot_table.columns:
                            if col == 'Country':
                                new_columns.append(col)
                            else:
                                try:
                                    new_columns.append(str(int(float(col))))
                                except (ValueError, TypeError):
                                    new_columns.append(str(col))
                        pivot_table.columns = new_columns
                        # Format values
                        for col in pivot_table.columns:
                            if col != 'Country':
                                if view_toggle_table == "Absolute Value (USD Millions)":
                                    pivot_table[col] = pivot_table[col].apply(
                                        lambda x: f"{x:,.0f}" if pd.notna(x) else ""
                                    )
                                else:
                                    pivot_table[col] = pivot_table[col].apply(
                                        lambda x: f"{x:.2f}%" if pd.notna(x) else ""
                                    )
                        display_table = pivot_table
                    
                    st.dataframe(display_table, use_container_width=True, height=400)
                    
                    # CSV download
                    csv = display_table.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"trade_mispricing_{selected_indicator_name_table.replace(' ', '_').lower()}_{table_format.lower().replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            st.markdown("---")
            
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
Trade mispricing is a major channel for illicit financial flows, where goods are intentionally over- or under-valued to shift profits abroad or avoid taxes. This indicator measures the volume and value of trade mispricing activities detected through bilateral trade mismatch analysis.
                    """)
                with tab_rel:
                    st.markdown("""
**Efficiency:** Reveals systemic leakages — inefficient customs enforcement, weak valuation frameworks, or poor transparency that enable IFFs.

**Effectiveness:** Shows how well fiscal and regulatory systems prevent illicit outflows that erode domestic resources.
                    """)
                with tab_proxy:
                    st.markdown("""
GFI's trade gap data is widely used for estimating IFFs due to trade mispricing, as direct measurement is not feasible. The indicators show trade mispricing between developing and advanced economies and with all global trading partners.
                    """)
                with tab_pillar:
                    st.markdown("""
This indicator exposes a key IFF pathway — trade mispricing, where goods are intentionally over- or under-valued to shift profits abroad or avoid taxes. Reducing such gaps enhances transparency, fiscal fairness, and sustainable financing capacity under Theme 4: Ownership and Financial Sovereignty.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
**How to Read This Graph:**  
Each bar represents the estimated value of mispriced trade flows — the difference between what a country reports and what its trading partners record. The larger the gap, the greater the potential IFFs escaping regulation.

**How to Apply Analytical Lens:**  
- **Efficiency:** Persistent or widening mispricing signals gaps in customs data, valuation practices, and inter-agency coordination.
- **Effectiveness:** Declining mispricing over time suggests stronger IFF prevention, better governance, and enhanced fiscal control.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicators for this sub-tab
            subtab_indicators_442_1 = {}
            for ind_name, ind_details in trade_mispricing_indicators.items():
                if ind_details["label"] in df_filtered['indicator_label'].unique():
                    subtab_indicators_442_1[ind_name] = ind_details["label"]
                elif ind_details.get("code") and 'indicator_code' in df_filtered.columns:
                    if ind_details["code"] in df_filtered['indicator_code'].astype(str).values:
                        subtab_indicators_442_1[ind_name] = ind_details["label"]
            
            if subtab_indicators_442_1:
                africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
                df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
                
                # Calculate coverage summary
                countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_442_1.values())]['country_or_area'].nunique()
                total_africa_countries = len(africa_countries)
                coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
                
                st.markdown(f"""
                <div class="data-availability-box">
                  <div class="left">
                    <h4>Data Availability in Africa</h4>
                    <p>
                      Data availability determines how confidently we can interpret trade mispricing trends across Africa. 
                      This view highlights which countries report recent data and where gaps persist — often due to differences in statistical capacity, reporting cycles, or institutional coverage.
                    </p>
                    <p><strong>Use the heatmap below to explore:</strong></p>
                    <ul>
                      <li><strong>Countries with up-to-date reporting</strong> (strong coverage)</li>
                      <li><strong>Countries with partial or outdated data</strong></li>
                      <li><strong>Indicators missing post-2021 updates</strong></li>
                    </ul>
                    <p style="margin-top: 1rem;"><em>Current data coverage: {coverage}% of African countries</em></p>
                  </div>
                  <div class="right">
                    <p><strong>Legend:</strong></p>
                    <ul style="text-align: left;">
                      <li><strong>Dark cells:</strong> Recent, consistent reporting (post-2020)</li>
                      <li><strong>Light cells:</strong> Partial or outdated reporting</li>
                      <li><strong>Empty cells:</strong> Missing or unreported values</li>
                    </ul>
                    <p><em>Hover over a cell in the heatmap below to view country-year coverage.</em></p>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View data availability heatmap", expanded=False):
                    selected_gap_indicator = st.selectbox(
                        "Select indicator to view data availability:",
                        options=list(subtab_indicators_442_1.keys()),
                        key="ind_4_4_2_1_gap_indicator_select"
                    )
                    uv.render_data_availability_heatmap(
                        df=df_africa,
                        indicator_label=subtab_indicators_442_1[selected_gap_indicator],
                        title=f"Data Availability for {selected_gap_indicator} (Africa)",
                        container_key="ind_4_4_2_1_gap"
                    )
    
    # ========================================
    # SUB-TAB 2: Indicator 4.4.2.2 - Tax Evasion (ISORA)
    # ========================================
    with subtab_442_2:
        with st.container():
            # A. Indicator Header
            st.markdown("""
        <div class='indicator-card'>
                <h4>
                    Indicator 4.4.2.2: Tax Evasion (ISORA Taxpayer Registration Data)
                    <button type="button" class="info-icon-btn" data-tooltip="Measures the share of active and inactive taxpayers on various registers (PIT, CIT, VAT, PAYE, Excise) as a percentage of the labor force or population. Low registration reveals institutional weakness in capturing economic activity." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> How effective are national tax administrations in registering and maintaining active taxpayers — and what share of potential taxpayers remain outside the system, creating domestic channels for IFFs and erosion of the revenue base?
            </p>
        </div>
        """, unsafe_allow_html=True)
        
            # B. Local Filter Row
            col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([2, 2, 2, 1])
            
            with col_filter1:
                available_years = sorted(df_filtered['year'].dropna().unique()) if not df_filtered.empty else []
                if available_years:
                    default_year_idx = len(available_years) - 1 if available_years else 0
                    if 'ind_4_4_2_2_year_filter' not in st.session_state:
                        st.session_state.ind_4_4_2_2_year_filter = available_years[default_year_idx] if available_years else None
                    selected_year = st.selectbox(
                        "Select Year(s)",
                        options=available_years,
                        index=available_years.index(st.session_state.ind_4_4_2_2_year_filter) if st.session_state.ind_4_4_2_2_year_filter in available_years else default_year_idx,
                        key="ind_4_4_2_2_year_filter"
                    )
                else:
                    selected_year = None
            
            with col_filter2:
                africa_countries_list = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
                available_countries = sorted([c for c in df_filtered['country_or_area'].unique() if c in africa_countries_list]) if not df_filtered.empty else []
                if 'ind_4_4_2_2_country_filter' not in st.session_state:
                    st.session_state.ind_4_4_2_2_country_filter = []
                selected_countries = st.multiselect(
                    "Select Country",
                    options=available_countries,
                    default=st.session_state.ind_4_4_2_2_country_filter,
                    key="ind_4_4_2_2_country_filter"
                )
            
            with col_filter3:
                available_regions = sorted(ref_data[ref_data['Region Name'] == 'Africa']['Intermediate Region Name'].dropna().unique())
                if 'ind_4_4_2_2_region_filter' not in st.session_state:
                    st.session_state.ind_4_4_2_2_region_filter = []
                selected_regions = st.multiselect(
                    "Select Region",
                    options=available_regions,
                    default=st.session_state.ind_4_4_2_2_region_filter,
                    key="ind_4_4_2_2_region_filter"
                )
            
            with col_filter4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_4_2_2_reset"):
                    if 'ind_4_4_2_2_year_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_2_year_filter
                    if 'ind_4_4_2_2_country_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_2_country_filter
                    if 'ind_4_4_2_2_region_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_2_region_filter
                    st.rerun()
            
            # Define tax type indicators with colors
            tax_type_indicators = {
                "Active taxpayers on PIT register as percentage of Labor Force": {"color": "#0072BC", "type": "PIT"},
                "Active taxpayers on PIT register as percentage of Population": {"color": "#0072BC", "type": "PIT"},
                "On PIT register": {"color": "#0072BC", "type": "PIT"},
                "On CIT register": {"color": "#00A1A1", "type": "CIT"},
                "On VAT register": {"color": "#F26C2B", "type": "VAT"},
                "On PAYE register": {"color": "#FFD34E", "type": "PAYE"},
                "On Excise register": {"color": "#FFD34E", "type": "Excise"}
            }
            
            # Filter to only available indicators
            available_tax_indicators = {
                k: v for k, v in tax_type_indicators.items()
                if k in df_filtered['indicator_label'].unique()
            }
            
            # C. Multi-View Tabs
            tab_graph_442_2, tab_map_442_2, tab_table_442_2 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_442_2:
                selected_tax_types = st.multiselect(
                    "Select Tax Type(s):",
                    options=list(available_tax_indicators.keys()),
                    default=list(available_tax_indicators.keys()),
                    key="ind_4_4_2_2_tax_type_select"
                )
                
                if selected_tax_types:
                    chart_data = df_filtered[df_filtered['indicator_label'].isin(selected_tax_types)].copy()
                    
                    if selected_countries:
                        chart_data = chart_data[chart_data['country_or_area'].isin(selected_countries)]
                    if selected_regions:
                        region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                        chart_data = chart_data[chart_data['country_or_area'].isin(region_countries)]
                    
                    if not chart_data.empty:
                        # Create line chart (like old implementation)
                        fig = go.Figure()
                        
                        # Determine which countries are being displayed
                        countries_in_data = sorted(chart_data['country_or_area'].unique())
                        num_countries = len(countries_in_data)
                        
                        # Group by tax type and create lines
                        years = sorted(chart_data['year'].unique())
                        for tax_label in selected_tax_types:
                            tax_data = chart_data[chart_data['indicator_label'] == tax_label].sort_values('year')
                            tax_color = available_tax_indicators[tax_label]["color"]
                            
                            # Show individual country lines if 1-3 countries, otherwise show average
                            if num_countries <= 3:
                                # Show separate lines for each country
                                for country in countries_in_data:
                                    country_tax_data = tax_data[tax_data['country_or_area'] == country].sort_values('year')
                                    if not country_tax_data.empty:
                                        fig.add_trace(go.Scatter(
                                            x=country_tax_data['year'],
                                            y=country_tax_data['value'],
                                            mode='lines+markers',
                                            name=f"{tax_label} - {country}",
                                            line=dict(color=tax_color, width=2, dash='solid' if num_countries == 1 else 'dash'),
                                            marker=dict(size=6),
                                            hovertemplate=f"<b>{country}</b><br>{tax_label}<br>Year: %{{x}}<br>Value: %{{y:.2f}}%<br><extra></extra>"
                                        ))
                            else:
                                # Aggregate by year (average across countries if multiple)
                                tax_data_agg = tax_data.groupby('year')['value'].mean().reset_index()
                                tax_data_agg = tax_data_agg.sort_values('year')
                                fig.add_trace(go.Scatter(
                                    x=tax_data_agg['year'],
                                    y=tax_data_agg['value'],
                                    mode='lines+markers',
                                    name=tax_label,
                                    line=dict(color=tax_color, width=2),
                                    hovertemplate=f"<b>{tax_label}</b><br>Year: %{{x}}<br>Average Value: %{{y:.2f}}%<br>Countries: {num_countries}<br><extra></extra>"
                                ))
                        
                        # Build title with country information
                        if selected_countries:
                            if num_countries <= 3:
                                title = f"Tax Evasion Indicators - {', '.join(countries_in_data)}"
                            else:
                                title = f"Tax Evasion Indicators - Average across {num_countries} countries"
                        elif selected_regions:
                            title = f"Tax Evasion Indicators - {', '.join(selected_regions)} ({num_countries} countries)"
                        else:
                            title = f"Tax Evasion Indicators - All Countries ({num_countries} countries)"
                        
                        fig.update_layout(
                            title=title,
                            xaxis_title="Year",
                            yaxis_title="Percentage",
                            height=500,
                            hovermode='closest',
                            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True, key="plot_442_2_graph")
                    else:
                        st.info("No data available for the selected filters.")
                else:
                    st.info("Please select at least one tax type.")
            
            with tab_map_442_2:
                selected_tax_type_map = st.selectbox(
                    "Select Tax Type for Map:",
                    options=list(available_tax_indicators.keys()),
                    key="ind_4_4_2_2_tax_type_map"
                )
                
                map_data = df_filtered[df_filtered['indicator_label'] == selected_tax_type_map].copy()
                
                if selected_year:
                    map_data = map_data[map_data['year'] == selected_year]
                else:
                    latest_year = map_data['year'].max()
                    map_data = map_data[map_data['year'] == latest_year]
                
                if not map_data.empty:
                    africa_ref = ref_data[ref_data['Region Name'] == 'Africa'][['Country or Area', 'iso3']].drop_duplicates()
                    map_data_merged = map_data.merge(africa_ref, left_on='country_or_area', right_on='Country or Area', how='left')
                    
                    if 'iso3' in map_data_merged.columns and not map_data_merged['iso3'].isna().all():
                        fig = px.choropleth(
                            map_data_merged,
                            locations='iso3',
                            color='value',
                            hover_name='country_or_area',
                            hover_data={'year': True, 'value': ':.2f'},
                            color_continuous_scale='Blues',
                            title=f"Geographical Distribution: {selected_tax_type_map}"
                        )
                        fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="white")
                        st.plotly_chart(fig, use_container_width=True, key="plot_442_2_map")
                    else:
                        st.info("No geographic data available for mapping.")
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_table_442_2:
                selected_tax_types_table = st.multiselect(
                    "Select Tax Type(s):",
                    options=list(available_tax_indicators.keys()),
                    default=list(available_tax_indicators.keys()),
                    key="ind_4_4_2_2_tax_type_table"
                )
                
                if selected_tax_types_table:
                    table_data = df_filtered[df_filtered['indicator_label'].isin(selected_tax_types_table)].copy()
                    
                    if selected_year:
                        table_data = table_data[table_data['year'] == selected_year]
                    if selected_countries:
                        table_data = table_data[table_data['country_or_area'].isin(selected_countries)]
                    if selected_regions:
                        region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                        table_data = table_data[table_data['country_or_area'].isin(region_countries)]
                    
                    if not table_data.empty:
                        display_table = table_data[['country_or_area', 'year', 'indicator_label', 'value']].rename(columns={
                            'country_or_area': 'Country',
                            'year': 'Year',
                            'indicator_label': 'Tax Type',
                            'value': 'Percentage Registered'
                        })
                        st.dataframe(display_table, use_container_width=True)
                        
                        csv = display_table.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="taxpayer_registration_data.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            st.markdown("---")
            
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
Tax evasion indicators measure the share of active and inactive taxpayers on various registers (PIT, CIT, VAT, PAYE, Excise) as a percentage of the labor force or population. Proxied by IMF ISORA Tax Registration Data.
                    """)
                with tab_rel:
                    st.markdown("""
**Efficiency:** Measures coverage and compliance — how well the tax administration converts economic activity into registered taxpayers.

**Effectiveness:** Assesses the capacity of DRM systems to close IFF-related loopholes (evasion, informality, under-registration).
                    """)
                with tab_proxy:
                    st.markdown("""
IMF ISORA tax registration data provides a standardized approach to estimate taxpayer activity and evasion across countries.
                    """)
                with tab_pillar:
                    st.markdown("""
Under Theme 4: DRM Systems and Institutions, this indicator examines domestic IFFs via tax evasion. Low taxpayer registration reveals institutional weakness in capturing economic activity and signals potential loss of resources to informal or illicit channels. Strengthening tax administration efficiency directly reduces IFFs and enhances fiscal sovereignty.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
**How to Read This Graph:**  
Each bar shows the share of the eligible population or labor force registered for a specific tax. Lower percentages mean large segments of economic activity remain outside the tax net — potential domestic IFF zones.

**How to Apply Analytical Lens:**  
- **Efficiency:** High registration ratios indicate strong institutional capacity to capture economic actors.
- **Effectiveness:** Expanding coverage reduces tax evasion and leakages, ensuring domestic resources stay within national systems to finance development.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicators for this sub-tab
            subtab_indicators_442_2 = {}
            for ind_name in tax_type_indicators.keys():
                if ind_name in df_filtered['indicator_label'].unique():
                    subtab_indicators_442_2[ind_name] = ind_name
            
            if subtab_indicators_442_2:
                africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
                df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
                
                # Calculate coverage summary
                countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_442_2.values())]['country_or_area'].nunique()
                total_africa_countries = len(africa_countries)
                coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
                
                st.markdown(f"""
                <div class="data-availability-box">
                  <div class="left">
                    <h4>Data Availability in Africa</h4>
                    <p>
                      Data availability determines how confidently we can interpret tax evasion trends across Africa. 
                      This view highlights which countries report recent data and where gaps persist — often due to differences in statistical capacity, reporting cycles, or institutional coverage.
                    </p>
                    <p><strong>Use the heatmap below to explore:</strong></p>
                    <ul>
                      <li><strong>Countries with up-to-date reporting</strong> (strong coverage)</li>
                      <li><strong>Countries with partial or outdated data</strong></li>
                      <li><strong>Indicators missing post-2021 updates</strong></li>
                    </ul>
                    <p style="margin-top: 1rem;"><em>Current data coverage: {coverage}% of African countries</em></p>
                  </div>
                  <div class="right">
                    <p><strong>Legend:</strong></p>
                    <ul style="text-align: left;">
                      <li><strong>Dark cells:</strong> Recent, consistent reporting (post-2020)</li>
                      <li><strong>Light cells:</strong> Partial or outdated reporting</li>
                      <li><strong>Empty cells:</strong> Missing or unreported values</li>
                    </ul>
                    <p><em>Hover over a cell in the heatmap below to view country-year coverage.</em></p>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View data availability heatmap", expanded=False):
                    selected_gap_indicator = st.selectbox(
                        "Select indicator to view data availability:",
                        options=list(subtab_indicators_442_2.keys()),
                        key="ind_4_4_2_2_gap_indicator_select"
                    )
                    uv.render_data_availability_heatmap(
                        df=df_africa,
                        indicator_label=subtab_indicators_442_2[selected_gap_indicator],
                        title=f"Data Availability for {selected_gap_indicator} (Africa)",
                        container_key="ind_4_4_2_2_gap"
                    )
    
    # ========================================
    # SUB-TAB 3: Indicator 4.4.2.3 - Criminal Activities
    # ========================================
    with subtab_442_3:
        with st.container():
            # A. Indicator Header
            st.markdown("""
        <div class='indicator-card'>
                <h4>
                    Indicator 4.4.2.3: Criminal Activities (Drug Trafficking)
                    <button type="button" class="info-icon-btn" data-tooltip="Monetary losses (in USD) to drug sales. Calculated as drug seizures in kilograms multiplied by drug price per kilogram. Proxied by UNODC Crime Flow Data." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> How large are criminally generated IFFs (from drug trafficking) in each African country, and how have they evolved over time?
            </p>
        </div>
        """, unsafe_allow_html=True)
        
            # B. Local Filter Row
            col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([2, 2, 2, 1])
            
            with col_filter1:
                available_years = sorted(df_filtered['year'].dropna().unique()) if not df_filtered.empty else []
                if available_years:
                    default_year_idx = len(available_years) - 1 if available_years else 0
                    if 'ind_4_4_2_3_year_filter' not in st.session_state:
                        st.session_state.ind_4_4_2_3_year_filter = available_years[default_year_idx] if available_years else None
                    selected_year = st.selectbox(
                        "Select Year(s)",
                        options=available_years,
                        index=available_years.index(st.session_state.ind_4_4_2_3_year_filter) if st.session_state.ind_4_4_2_3_year_filter in available_years else default_year_idx,
                        key="ind_4_4_2_3_year_filter"
                    )
                else:
                    selected_year = None
            
            with col_filter2:
                africa_countries_list = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
                available_countries = sorted([c for c in df_filtered['country_or_area'].unique() if c in africa_countries_list]) if not df_filtered.empty else []
                if 'ind_4_4_2_3_country_filter' not in st.session_state:
                    st.session_state.ind_4_4_2_3_country_filter = []
                selected_countries = st.multiselect(
                    "Select Country (max 3)",
                    options=available_countries,
                    default=st.session_state.ind_4_4_2_3_country_filter[:3] if len(st.session_state.ind_4_4_2_3_country_filter) > 0 else [],
                    key="ind_4_4_2_3_country_filter"
                )
            
            with col_filter3:
                available_regions = sorted(ref_data[ref_data['Region Name'] == 'Africa']['Intermediate Region Name'].dropna().unique())
                if 'ind_4_4_2_3_region_filter' not in st.session_state:
                    st.session_state.ind_4_4_2_3_region_filter = []
                selected_regions = st.multiselect(
                    "Select Region",
                    options=available_regions,
                    default=st.session_state.ind_4_4_2_3_region_filter,
                    key="ind_4_4_2_3_region_filter"
                )
            
            with col_filter4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_4_2_3_reset"):
                    if 'ind_4_4_2_3_year_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_3_year_filter
                    if 'ind_4_4_2_3_country_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_3_country_filter
                    if 'ind_4_4_2_3_region_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_3_region_filter
                    st.rerun()
            
            # C. Multi-View Tabs
            tab_graph_442_3, tab_map_442_3, tab_table_442_3 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_442_3:
                view_mode = st.radio(
                    "View Mode",
                    options=["Trend Over Time", "Compare Countries"],
                    horizontal=True,
                    key="ind_4_4_2_3_view_mode"
                )
                
                # Get UNODC data - check both indicator_label and indicator_code
                unodc_indicator_label = "Monetary losses (in USD) to drug sales. Amount of drugs seized in kilograms multiplied by the drug price in kilograms. Excludes all seizures not measured in grams or kilograms."
                unodc_indicator_code = "UNODC.DPS.losses"
                
                # Try to get data by code first, then by label
                if 'indicator_code' in df_filtered.columns:
                    chart_data = df_filtered[df_filtered['indicator_code'].astype(str).str.strip() == unodc_indicator_code].copy()
                else:
                    chart_data = df_filtered[df_filtered['indicator_label'] == unodc_indicator_label].copy()
                
                if chart_data.empty:
                    # Try by label if code didn't work
                    chart_data = df_filtered[df_filtered['indicator_label'] == unodc_indicator_label].copy()
                
                if selected_countries:
                    chart_data = chart_data[chart_data['country_or_area'].isin(selected_countries)]
                if selected_regions:
                    region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                    chart_data = chart_data[chart_data['country_or_area'].isin(region_countries)]
                
                if not chart_data.empty:
                    if view_mode == "Trend Over Time":
                        # Line chart for trends (like old implementation)
                        fig = go.Figure()
                        
                        countries = sorted(chart_data['country_or_area'].unique())
                        # Generate distinct colors for countries
                        import colorsys
                        n_countries = len(countries)
                        color_gradient = ['#B7E0F2', '#0072BC', '#F26C2B', '#B30000']
                        
                        for idx, country in enumerate(countries):
                            country_data = chart_data[chart_data['country_or_area'] == country].sort_values('year')
                            if idx < len(color_gradient):
                                color = color_gradient[idx]
                            else:
                                hue = idx / n_countries
                                rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                                color = f'rgb({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)})'
                            
                            fig.add_trace(go.Scatter(
                                x=country_data['year'],
                                y=country_data['value'],
                                mode='lines+markers',
                                name=country,
                                line=dict(color=color, width=2),
                                hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>Value: $%{{y:,.0f}}<br><extra></extra>"
                            ))
                        
                        fig.update_layout(
                    title="Criminal Activities: Proceeds from Illegal Activities",
                            xaxis_title="Year",
                            yaxis_title="Value (USD)",
                            height=500,
                            hovermode='closest',
                            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
                        )
                    else:
                        # Bar chart for country comparison
                        if selected_year:
                            year_data = chart_data[chart_data['year'] == selected_year]
                        else:
                            latest_year = chart_data['year'].max()
                            year_data = chart_data[chart_data['year'] == latest_year]
                        
                        if not year_data.empty:
                            year_data_sorted = year_data.sort_values('value', ascending=False).head(15)
                            
                            fig = go.Figure()
                            fig.add_trace(go.Bar(
                                x=year_data_sorted['country_or_area'],
                                y=year_data_sorted['value'],
                                marker=dict(
                                    color=year_data_sorted['value'],
                                    colorscale='Reds',
                                    showscale=True
                                ),
                                hovertemplate="<b>%{x}</b><br>Year: " + str(selected_year if selected_year else latest_year) + "<br>Value: $%{y:,.0f}<br><extra></extra>"
                            ))
                            
                            fig.update_layout(
                                title=f"Criminal Activities: Country Comparison ({selected_year if selected_year else latest_year})",
                                xaxis_title="Country",
                                yaxis_title="Value (USD)",
                                height=500,
                                xaxis={'categoryorder': 'total descending'}
                            )
                        else:
                            st.info("No data available for the selected year.")
                            fig = None
                    
                    if fig:
                        st.plotly_chart(fig, use_container_width=True, key="plot_442_3_graph")
                else:
                    st.info("No data available for Criminal Activities")
            
            with tab_map_442_3:
                unodc_indicator_label = "Monetary losses (in USD) to drug sales. Amount of drugs seized in kilograms multiplied by the drug price in kilograms. Excludes all seizures not measured in grams or kilograms."
                unodc_indicator_code = "UNODC.DPS.losses"
                
                # Try to get data by code first, then by label
                if 'indicator_code' in df_filtered.columns:
                    map_data = df_filtered[df_filtered['indicator_code'].astype(str).str.strip() == unodc_indicator_code].copy()
                else:
                    map_data = df_filtered[df_filtered['indicator_label'] == unodc_indicator_label].copy()
                
                if map_data.empty:
                    map_data = df_filtered[df_filtered['indicator_label'] == unodc_indicator_label].copy()
                
                # Ensure year is numeric before filtering
                map_data['year'] = pd.to_numeric(map_data['year'], errors='coerce')
                
                # Apply year filter
                if selected_year is not None:
                    # Convert selected_year to numeric for comparison
                    try:
                        selected_year_num = float(selected_year)
                        map_data = map_data[map_data['year'] == selected_year_num]
                    except (ValueError, TypeError):
                        # If conversion fails, try string matching
                        map_data = map_data[map_data['year'].astype(str) == str(selected_year)]
                else:
                    if not map_data.empty:
                        latest_year = map_data['year'].max()
                        map_data = map_data[map_data['year'] == latest_year]
                
                # Apply country and region filters
                if selected_countries:
                    map_data = map_data[map_data['country_or_area'].isin(selected_countries)]
                if selected_regions:
                    region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                    map_data = map_data[map_data['country_or_area'].isin(region_countries)]
                
                if not map_data.empty:
                    # Remove rows with missing values
                    map_data = map_data.dropna(subset=['value'])
                    
                    if not map_data.empty:
                        # Merge with reference data for ISO codes using inner join
                        africa_ref = ref_data[ref_data['Region Name'] == 'Africa'].copy()
                        if not africa_ref.empty and 'Country or Area' in africa_ref.columns:
                            map_data_merged = map_data.merge(
                                africa_ref[['Country or Area', 'iso3']],
                                left_on='country_or_area',
                                right_on='Country or Area',
                                how='inner'
                            )
                            
                            if not map_data_merged.empty:
                                # Determine the correct ISO column name after merge
                                iso_col = 'iso3_y' if 'iso3_y' in map_data_merged.columns else ('iso3_x' if 'iso3_x' in map_data_merged.columns else 'iso3')
                                if iso_col != 'iso3' and iso_col in map_data_merged.columns:
                                    map_data_merged['iso3'] = map_data_merged[iso_col]
                                
                                # Filter out rows with missing ISO codes
                                map_data_merged = map_data_merged[map_data_merged['iso3'].notna()]
                                
                                if not map_data_merged.empty:
                                    fig = px.choropleth(
                                        map_data_merged,
                                        locations='iso3',
                                        color='value',
                                        hover_name='country_or_area',
                                        hover_data={'year': True, 'value': ':,.0f'},
                                        color_continuous_scale='Reds',
                                        title=f"Geographical Distribution: Criminal Activities (Drug Trafficking)" + (f" ({int(selected_year)})" if selected_year is not None else "")
                                    )
                                    fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="lightgray")
                                    fig.update_layout(height=600, margin=dict(l=0, r=0, t=40, b=0))
                                    st.plotly_chart(fig, use_container_width=True, key="plot_442_3_map")
                                else:
                                    st.info("No geographic data available for mapping after filtering ISO codes.")
                            else:
                                st.info("No matching countries found between data and reference data.")
                        else:
                            st.info("No reference data available for mapping.")
                    else:
                        st.info("No data available after removing missing values.")
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_table_442_3:
                unodc_indicator_label = "Monetary losses (in USD) to drug sales. Amount of drugs seized in kilograms multiplied by the drug price in kilograms. Excludes all seizures not measured in grams or kilograms."
                unodc_indicator_code = "UNODC.DPS.losses"
                
                # Try to get data by code first, then by label
                if 'indicator_code' in df_filtered.columns:
                    table_data = df_filtered[df_filtered['indicator_code'].astype(str).str.strip() == unodc_indicator_code].copy()
                else:
                    table_data = df_filtered[df_filtered['indicator_label'] == unodc_indicator_label].copy()
                
                if table_data.empty:
                    table_data = df_filtered[df_filtered['indicator_label'] == unodc_indicator_label].copy()
                
                if selected_year:
                    table_data = table_data[table_data['year'] == selected_year]
                if selected_countries:
                    table_data = table_data[table_data['country_or_area'].isin(selected_countries)]
                if selected_regions:
                    region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                    table_data = table_data[table_data['country_or_area'].isin(region_countries)]
                
                if not table_data.empty:
                    display_table = table_data[['country_or_area', 'year', 'value']].rename(columns={
                        'country_or_area': 'Country',
                        'year': 'Year',
                        'value': 'Estimated IFF Value (USD Millions)'
                    })
                    st.dataframe(display_table, use_container_width=True)
                    
                    csv = display_table.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="criminal_activities_iff.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            st.markdown("---")
            
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
Monetary losses (in USD) to drug sales. This indicator is calculated as the amount of drugs seized in kilograms multiplied by the drug price per kilogram. All seizures not measured in grams or kilograms are excluded from the calculation. Proxied by UNODC Crime Flow Data.
                    """)
                with tab_rel:
                    st.markdown("""
**Efficiency:** How well law enforcement intercepts and monitors criminal financial flows. Low values may reflect limited data or enforcement capacity.

**Effectiveness:** High values signal strong criminal IFF pressures that erode fiscal sovereignty and require cross-border cooperation and asset recovery measures.
                    """)
                with tab_proxy:
                    st.markdown("""
This indicator uses UNODC drug seizure and price data, which are internationally recognized and reported by national authorities. The methodology ensures comparability and reliability by standardizing units and excluding ambiguous measurements.
                    """)
                with tab_pillar:
                    st.markdown("""
This indicator quantifies the financial magnitude of criminally generated IFFs using drug-trade seizure values. It helps identify how crime-related financial leakages erode domestic revenues and signal institutional enforcement capacity.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
**How to Read This Graph:**  
Use the filters to explore how much money leaves each country through criminal activity (proxied by drug-trade values). Select a country to see its trend or a year to compare across countries. Higher values = larger criminal economies or better detection.

**How to Apply Analytical Lens:**  
- **Efficiency:** Trends showing stable or falling IFFs suggest improving interception systems.
- **Effectiveness:** Compare IFF intensity across countries to assess where enforcement coordination or financial-intelligence reforms yield results.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicator for this sub-tab
            unodc_indicator_label = "Monetary losses (in USD) to drug sales. Amount of drugs seized in kilograms multiplied by the drug price in kilograms. Excludes all seizures not measured in grams or kilograms."
            unodc_indicator_code = "UNODC.DPS.losses"
            
            subtab_indicators_442_3 = {}
            # Check if indicator exists in data
            if unodc_indicator_label in df_filtered['indicator_label'].unique():
                subtab_indicators_442_3["Criminal Activities (Drug Sales)"] = unodc_indicator_label
            elif 'indicator_code' in df_filtered.columns and unodc_indicator_code in df_filtered['indicator_code'].astype(str).values:
                subtab_indicators_442_3["Criminal Activities (Drug Sales)"] = unodc_indicator_label
            
            if subtab_indicators_442_3:
                africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
                df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
                
                # Calculate coverage summary
                countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_442_3.values())]['country_or_area'].nunique()
                total_africa_countries = len(africa_countries)
                coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
                
                st.markdown(f"""
                <div class="data-availability-box">
                  <div class="left">
                    <h4>Data Availability in Africa</h4>
                    <p>
                      Data availability determines how confidently we can interpret criminal activities trends across Africa. 
                      This view highlights which countries report recent data and where gaps persist — often due to differences in statistical capacity, reporting cycles, or institutional coverage.
                    </p>
                    <p><strong>Use the heatmap below to explore:</strong></p>
                    <ul>
                      <li><strong>Countries with up-to-date reporting</strong> (strong coverage)</li>
                      <li><strong>Countries with partial or outdated data</strong></li>
                      <li><strong>Indicators missing post-2021 updates</strong></li>
                    </ul>
                    <p style="margin-top: 1rem;"><em>Current data coverage: {coverage}% of African countries</em></p>
                  </div>
                  <div class="right">
                    <p><strong>Legend:</strong></p>
                    <ul style="text-align: left;">
                      <li><strong>Dark cells:</strong> Recent, consistent reporting (post-2020)</li>
                      <li><strong>Light cells:</strong> Partial or outdated reporting</li>
                      <li><strong>Empty cells:</strong> Missing or unreported values</li>
                    </ul>
                    <p><em>Hover over a cell in the heatmap below to view country-year coverage.</em></p>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View data availability heatmap", expanded=False):
                    selected_gap_indicator = st.selectbox(
                        "Select indicator to view data availability:",
                        options=list(subtab_indicators_442_3.keys()),
                        key="ind_4_4_2_3_gap_indicator_select"
                    )
                    uv.render_data_availability_heatmap(
                        df=df_africa,
                        indicator_label=subtab_indicators_442_3[selected_gap_indicator],
                        title=f"Data Availability for {selected_gap_indicator} (Africa)",
                        container_key="ind_4_4_2_3_gap"
                    )
    
    # ========================================
    # SUB-TAB 4: Indicator 4.4.2.4 - Corruption and Bribery
    # ========================================
    with subtab_442_4:
        with st.container():
            # A. Indicator Header
            st.markdown("""
        <div class='indicator-card'>
                <h4>
                    Indicator 4.4.2.4: Corruption and Bribery
                    <button type="button" class="info-icon-btn" data-tooltip="Measures corruption levels using World Bank Governance Indicators. Estimated annual corruption losses are allocated from $148B based on inverted control of corruption scores." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> How does corruption risk, as measured by governance quality, contribute to the estimated share of IFF vulnerability across African countries?
            </p>
        </div>
        """, unsafe_allow_html=True)
        
            # B. Local Filter Row
            col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([2, 2, 2, 1])
            
            with col_filter1:
                available_years = sorted(df_filtered['year'].dropna().unique()) if not df_filtered.empty else []
                if available_years:
                    default_year_idx = len(available_years) - 1 if available_years else 0
                    if 'ind_4_4_2_4_year_filter' not in st.session_state:
                        st.session_state.ind_4_4_2_4_year_filter = available_years[default_year_idx] if available_years else None
                    selected_year = st.selectbox(
                        "Select Year(s)",
                        options=available_years,
                        index=available_years.index(st.session_state.ind_4_4_2_4_year_filter) if st.session_state.ind_4_4_2_4_year_filter in available_years else default_year_idx,
                        key="ind_4_4_2_4_year_filter"
                    )
                else:
                    selected_year = None
            
            with col_filter2:
                africa_countries_list = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
                available_countries = sorted([c for c in df_filtered['country_or_area'].unique() if c in africa_countries_list]) if not df_filtered.empty else []
                if 'ind_4_4_2_4_country_filter' not in st.session_state:
                    st.session_state.ind_4_4_2_4_country_filter = []
                selected_countries = st.multiselect(
                    "Select Country",
                    options=available_countries,
                    default=st.session_state.ind_4_4_2_4_country_filter,
                    key="ind_4_4_2_4_country_filter"
                )
            
            with col_filter3:
                available_regions = sorted(ref_data[ref_data['Region Name'] == 'Africa']['Intermediate Region Name'].dropna().unique())
                if 'ind_4_4_2_4_region_filter' not in st.session_state:
                    st.session_state.ind_4_4_2_4_region_filter = []
                selected_regions = st.multiselect(
                    "Select Region",
                    options=available_regions,
                    default=st.session_state.ind_4_4_2_4_region_filter,
                    key="ind_4_4_2_4_region_filter"
                )
            
            with col_filter4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_4_2_4_reset"):
                    if 'ind_4_4_2_4_year_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_4_year_filter
                    if 'ind_4_4_2_4_country_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_4_country_filter
                    if 'ind_4_4_2_4_region_filter' in st.session_state:
                        del st.session_state.ind_4_4_2_4_region_filter
                    st.rerun()
            
            # C. Multi-View Tabs
            tab_graph_442_4, tab_map_442_4, tab_table_442_4 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_442_4:
                # Get corruption data
                corruption_indicator = "Control of Corruption"
                corruption_data = df_filtered[df_filtered['indicator_label'] == corruption_indicator].copy()
                
                if not corruption_data.empty:
                    # Calculate corruption losses using the function
                    latest_corruption = cim.calculate_corruption_losses(corruption_data)
                    
                    if selected_countries:
                        latest_corruption = latest_corruption[latest_corruption['country_or_area'].isin(selected_countries)]
                    if selected_regions:
                        region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                        latest_corruption = latest_corruption[latest_corruption['country_or_area'].isin(region_countries)]
                    
                    # Sort by corruption loss (descending)
                    latest_corruption_sorted = latest_corruption.sort_values('corruption_loss_billion_usd', ascending=False)
                    
                    # Use Altair bar chart
                    bar_chart = alt.Chart(latest_corruption_sorted).mark_bar().encode(
                        x=alt.X('country_or_area', sort='-y', title='Country'),
                        y=alt.Y('corruption_loss_billion_usd', title='Estimated Corruption Loss (Billion USD, out of 148)'),
                        tooltip=['country_or_area', 'corruption_loss_billion_usd', 'value', 'normalized_score', 'inverted_score'],
                        color=alt.Color('corruption_loss_billion_usd', scale=alt.Scale(scheme='redyellowgreen', reverse=True))
                    ).properties(
                        title='Estimated Annual Corruption Loss by Country (Allocated from $148B, WGI-based, Inverted)',
                        width=700,
                        height=500
                    )
                    
                    st.altair_chart(bar_chart, use_container_width=True)
                    
                    # Show calculated losses table in expander
                    with st.expander("View Calculated Losses Table"):
                        display_table = latest_corruption_sorted[['country_or_area', 'year', 'value', 'normalized_score', 'inverted_score', 'corruption_loss_billion_usd']].copy()
                        st.dataframe(
                            display_table.style.format({
                                'value': '{:.2f}',
                                'normalized_score': '{:.3f}',
                                'inverted_score': '{:.3f}',
                                'corruption_loss_billion_usd': '{:.2f}'
                            })
                        )
                        
                        st.write(f"**Sum of all country losses: {latest_corruption['corruption_loss_billion_usd'].sum():.2f} billion USD**")
                else:
                    st.info("No data available for Control of Corruption")
            
            with tab_map_442_4:
                corruption_indicator = "Control of Corruption"
                corruption_data = df_filtered[df_filtered['indicator_label'] == corruption_indicator].copy()
                
                if not corruption_data.empty:
                    # Filter to 2023 data specifically (or latest available if 2023 not available)
                    corruption_data['year'] = pd.to_numeric(corruption_data['year'], errors='coerce')
                    
                    # Try to get 2023 data first
                    if 2023 in corruption_data['year'].values:
                        map_year_data = corruption_data[corruption_data['year'] == 2023].copy()
                    else:
                        # Use latest available year
                        latest_year = corruption_data['year'].max()
                        map_year_data = corruption_data[corruption_data['year'] == latest_year].copy()
                    
                    if not map_year_data.empty:
                        # Calculate corruption losses for the specific year
                        latest_corruption = cim.calculate_corruption_losses(map_year_data)
                        
                        if selected_countries:
                            latest_corruption = latest_corruption[latest_corruption['country_or_area'].isin(selected_countries)]
                        if selected_regions:
                            region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                            latest_corruption = latest_corruption[latest_corruption['country_or_area'].isin(region_countries)]
                        
                        # Merge with reference data for ISO codes using inner join
                        africa_ref = ref_data[ref_data['Region Name'] == 'Africa'].copy()
                        if not africa_ref.empty and 'Country or Area' in africa_ref.columns:
                            map_data_merged = latest_corruption.merge(
                                africa_ref[['Country or Area', 'iso3']],
                                left_on='country_or_area',
                                right_on='Country or Area',
                                how='inner'
                            )
                            
                            if not map_data_merged.empty:
                                # Determine the correct ISO column name after merge
                                iso_col = 'iso3_y' if 'iso3_y' in map_data_merged.columns else ('iso3_x' if 'iso3_x' in map_data_merged.columns else 'iso3')
                                if iso_col != 'iso3' and iso_col in map_data_merged.columns:
                                    map_data_merged['iso3'] = map_data_merged[iso_col]
                                
                                # Filter out rows with missing ISO codes
                                map_data_merged = map_data_merged[map_data_merged['iso3'].notna()]
                                
                                if not map_data_merged.empty:
                                    map_year = int(map_data_merged['year'].iloc[0]) if 'year' in map_data_merged.columns else (2023 if 2023 in corruption_data['year'].values else int(corruption_data['year'].max()))
                                    fig = px.choropleth(
                                        map_data_merged,
                                        locations='iso3',
                                        color='corruption_loss_billion_usd',
                                        hover_name='country_or_area',
                                        hover_data={
                                            'corruption_loss_billion_usd': ':.2f',
                                            'normalized_score': ':.3f',
                                            'inverted_score': ':.3f',
                                            'year': True
                                        },
                                        color_continuous_scale='RdYlGn_r',
                                        title=f"Geographical Distribution: Corruption-Linked IFF Risk ({map_year})"
                                    )
                                    fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="lightgray")
                                    fig.update_layout(height=600, margin=dict(l=0, r=0, t=40, b=0))
                                    st.plotly_chart(fig, use_container_width=True, key="plot_442_4_map")
                                else:
                                    st.info("No geographic data available for mapping after filtering ISO codes.")
                            else:
                                st.info("No matching countries found between data and reference data.")
                        else:
                            st.info("No reference data available for mapping.")
                    else:
                        st.info("No data available for the selected year.")
                else:
                    st.info("No data available for Control of Corruption indicator.")
            
            with tab_table_442_4:
                corruption_indicator = "Control of Corruption"
                corruption_data = df_filtered[df_filtered['indicator_label'] == corruption_indicator].copy()
                
                if not corruption_data.empty:
                    latest_corruption = cim.calculate_corruption_losses(corruption_data)
                    
                    if selected_countries:
                        latest_corruption = latest_corruption[latest_corruption['country_or_area'].isin(selected_countries)]
                    if selected_regions:
                        region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions)]['Country or Area'].unique()
                        latest_corruption = latest_corruption[latest_corruption['country_or_area'].isin(region_countries)]
                    
                    display_table = latest_corruption[['country_or_area', 'year', 'value', 'normalized_score', 'inverted_score', 'corruption_loss_billion_usd']].rename(columns={
                        'country_or_area': 'Country',
                        'year': 'Year',
                        'value': 'Control of Corruption Score',
                        'normalized_score': 'Normalized Score (0-1)',
                        'inverted_score': 'Inverted Score',
                        'corruption_loss_billion_usd': 'Weighted IFF Risk Share (%)'
                    }).sort_values('Weighted IFF Risk Share (%)', ascending=False)
                    
                    st.dataframe(display_table, use_container_width=True)
                    
                    csv = display_table.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="corruption_bribery_iff.csv",
                        mime="text/csv"
                    )
                    
                    st.markdown(f"**Sum of all country losses: {latest_corruption['corruption_loss_billion_usd'].sum():.2f} billion USD**")
                else:
                    st.info("No data available for Control of Corruption indicator.")
            
            # D. Supporting Information Layers
            st.markdown("---")
            
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
**Calculation Methodology:**

1. **Normalization and Inversion:**
   - Original scores (range: -2.5 to 2.5) are normalized to 0-1 scale
   - Formula: Normalized Score = (Original Score + 2.5) / 5.0
   - **Inversion:** Inverted Score = 1 - Normalized Score (so higher corruption = higher loss)

2. **Weight Assignment:**
   - Each country's inverted score becomes its weight
   - Total weight is calculated as sum of all country weights

3. **Share Calculation:**
   - Country Loss = (Country Weight / Total Weight) × 148
   - 148 is a scaling factor for standardized comparison (billion USD)

**Data Source:** Worldwide Governance Indicators (WGI) from World Bank
                    """)
                with tab_rel:
                    st.markdown("""
**Efficiency:** Measures how well institutional and financial governance systems reduce leakage through corruption.

**Effectiveness:** Reflects a government's long-term ability to deter IFFs via integrity, transparency, and accountability frameworks.
                    """)
                with tab_proxy:
                    st.markdown("""
**Proxy Justification:**
- WGI's Control of Corruption index aggregates data from 30+ sources
- Includes surveys, expert assessments, and NGO reports
- Uses Unobserved Components Model (UCM) for robust aggregation
- Provides comprehensive view of governance quality
                    """)
                with tab_pillar:
                    st.markdown("""
Under Theme 4: DRM Systems and Institutions, this indicator estimates the potential contribution of corruption and bribery to Illicit Financial Flows. It uses governance quality as a proxy for leakage risk — recognizing that weak institutions and rent-seeking behaviors often enable large unrecorded outflows.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
**How to Read This Graph:**  
Each bar shows the estimated share of corruption-driven IFF vulnerability in Africa, derived from normalized governance scores. Countries with lower control of corruption contribute disproportionately to total potential IFFs.

**How to Apply Analytical Lens:**  
- **Efficiency:** Assess how institutional integrity systems (anti-corruption agencies, financial disclosure laws) limit leakages.
- **Effectiveness:** Track improvements in governance scores as indicators of progress in preventing corruption-linked IFFs.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicator for this sub-tab
            corruption_indicator = "Control of Corruption"
            subtab_indicators_442_4 = {}
            if corruption_indicator in df_filtered['indicator_label'].unique():
                subtab_indicators_442_4["Control of Corruption"] = corruption_indicator
            
            if subtab_indicators_442_4:
                africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
                df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
                
                # Calculate coverage summary
                countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_442_4.values())]['country_or_area'].nunique()
                total_africa_countries = len(africa_countries)
                coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
                
                st.markdown(f"""
                <div class="data-availability-box">
                  <div class="left">
                    <h4>Data Availability in Africa</h4>
                    <p>
                      Data availability determines how confidently we can interpret corruption and bribery trends across Africa. 
                      This view highlights which countries report recent data and where gaps persist — often due to differences in statistical capacity, reporting cycles, or institutional coverage.
                    </p>
                    <p><strong>Use the heatmap below to explore:</strong></p>
                    <ul>
                      <li><strong>Countries with up-to-date reporting</strong> (strong coverage)</li>
                      <li><strong>Countries with partial or outdated data</strong></li>
                      <li><strong>Indicators missing post-2021 updates</strong></li>
                    </ul>
                    <p style="margin-top: 1rem;"><em>Current data coverage: {coverage}% of African countries</em></p>
                  </div>
                  <div class="right">
                    <p><strong>Legend:</strong></p>
                    <ul style="text-align: left;">
                      <li><strong>Dark cells:</strong> Recent, consistent reporting (post-2020)</li>
                      <li><strong>Light cells:</strong> Partial or outdated reporting</li>
                      <li><strong>Empty cells:</strong> Missing or unreported values</li>
                    </ul>
                    <p><em>Hover over a cell in the heatmap below to view country-year coverage.</em></p>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View data availability heatmap", expanded=False):
                    selected_gap_indicator = st.selectbox(
                        "Select indicator to view data availability:",
                        options=list(subtab_indicators_442_4.keys()),
                        key="ind_4_4_2_4_gap_indicator_select"
                    )
                    uv.render_data_availability_heatmap(
                        df=df_africa,
                        indicator_label=subtab_indicators_442_4[selected_gap_indicator],
                        title=f"Data Availability for {selected_gap_indicator} (Africa)",
                        container_key="ind_4_4_2_4_gap"
                    )

# ========================================
# SUB-TOPIC 4.4.3 – Detection and Enforcement
# ========================================
with tab_subtopic_3:
    # Create sub-tabs for the four indicators under 4.4.3
    subtab_443_1, subtab_443_2a, subtab_443_2b, subtab_443_2c = st.tabs([
        "4.4.3.1 – Efficacy of Anti-IFF Measures",
        "4.4.3.2.a – Operating Metrics Audit",
        "4.4.3.2.b – Resources and ICT Infrastructure",
        "4.4.3.2.c – Staff Metrics"
    ])
    
    # ========================================
    # INDICATOR 4.4.3.1: Efficacy of Anti-IFF Measures
    # ========================================
    with subtab_443_1:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class="indicator-card">
                <h4>Indicator 4.4.3.1: Efficacy of Anti-IFF Measures
                    <button type="button" class="info-icon-btn" data-tooltip="Proxied by enablers framework suggested by Coherent policies for combating Illicit Financial Flows. Measures how strong and coherent national systems are for preventing, detecting, and enforcing measures against IFFs." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p><strong>Analytical Focus Question:</strong> How strong and coherent are national systems for preventing, detecting, and enforcing measures against illicit financial flows?</p>
        </div>
        """, unsafe_allow_html=True)
        
            # B. Local Filter Row
            col_year, col_country, col_region, col_reset = st.columns([2, 3, 3, 1])
            
            with col_year:
                available_years = sorted(df_filtered['year'].dropna().unique(), reverse=True)
                selected_year_443_1 = st.selectbox(
                    "Select Year(s)",
                    options=["All Years"] + [str(int(y)) for y in available_years],
                    key="ind_4_4_3_1_year_filter",
                    index=0
                )
            
            with col_country:
                available_countries = sorted(df_filtered['country_or_area'].dropna().unique())
                selected_countries_443_1 = st.multiselect(
                    "Select Country",
                    options=available_countries,
                    key="ind_4_4_3_1_country_filter",
                    default=[]
                )
            
            with col_region:
                africa_regions = sorted(ref_data[ref_data['Region Name'] == 'Africa']['Intermediate Region Name'].dropna().unique())
                selected_regions_443_1 = st.multiselect(
                    "Select Region",
                    options=africa_regions,
                    key="ind_4_4_3_1_region_filter",
                    default=[]
                )
            
            with col_reset:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_4_3_1_reset"):
                    for key in ["ind_4_4_3_1_year_filter", "ind_4_4_3_1_country_filter", "ind_4_4_3_1_region_filter"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            
            # Filter data
            indicator_data_443_1 = df_filtered.copy()
            
            # Define available governance indicators
            governance_indicators = {
                "Rule of Law": {
                    "label": "Rule of Law",
                    "code": None,
                    "color": "#0072BC",
                    "source": "WJP Factor 6: Regulatory Enforcement"
                },
                "Control of Corruption: Estimate": {
                    "label": "Control of Corruption: Estimate",
                    "code": None,
                    "color": "#F26C2B",
                    "source": "World Bank WGI"
                },
                "CPIA Transparency, Accountability, and Corruption in the Public Sector Rating": {
                    "label": "CPIA transparency, accountability, and corruption in the public sector rating",
                    "code": "IQ.CPA.PUBS.XQ",
                    "color": "#FFD34E",
                    "source": "World Bank CPIA"
                },
                "CPIA Quality of Public Administration Rating": {
                    "label": "CPIA quality of public administration rating",
                    "code": "IQ.CPA.PADM.XQ",
                    "color": "#009D8C",
                    "source": "World Bank CPIA"
                },
                "ID Ownership, 15 to 24 years old": {
                    "label": "ID ownership, 15 to 24 years old",
                    "code": "FX.OWN.TOTL.YG.ZS",
                    "color": "#7C4DFF",
                    "source": "World Bank"
                },
                "ID Ownership, 25 and older": {
                    "label": "ID ownership, 25 and older",
                    "code": "FX.OWN.TOTL.OL.ZS",
                    "color": "#B6E1DC",
                    "source": "World Bank"
                }
            }
            
            # Get data for available indicators from FULL dataset (before filtering) - match by both label and code
            # This ensures all indicators appear in all views regardless of current filters
            available_indicator_labels = []
            for ind_key, ind_info in governance_indicators.items():
                # Try matching by label first
                if ind_info["label"] in indicator_data_443_1['indicator_label'].unique():
                    available_indicator_labels.append(ind_key)
                # If code is available, also try matching by code
                elif ind_info.get("code") and 'indicator_code' in indicator_data_443_1.columns:
                    if ind_info["code"] in indicator_data_443_1['indicator_code'].astype(str).values:
                        available_indicator_labels.append(ind_key)
            
            # Filter by selections (after determining available indicators)
            if selected_year_443_1 != "All Years":
                indicator_data_443_1 = indicator_data_443_1[indicator_data_443_1['year'] == int(selected_year_443_1)]
            if selected_countries_443_1:
                indicator_data_443_1 = indicator_data_443_1[indicator_data_443_1['country_or_area'].isin(selected_countries_443_1)]
            if selected_regions_443_1:
                region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions_443_1)]['Country or Area'].unique()
                indicator_data_443_1 = indicator_data_443_1[indicator_data_443_1['country_or_area'].isin(region_countries)]
            
            # C. Multi-View Tabs
            tab_graph_443_1, tab_map_443_1, tab_table_443_1 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_443_1:
                # Display all indicators in a grid layout with small charts (Gradient View)
                if available_indicator_labels:
                    num_indicators = len(available_indicator_labels)
                    
                    # Determine grid layout: 3 columns for 6 indicators, 2 columns for fewer
                    if num_indicators <= 2:
                        num_cols = num_indicators
                    elif num_indicators <= 4:
                        num_cols = 2
                    else:
                        num_cols = 3
                    
                    # Process indicators in rows
                    for row_start in range(0, num_indicators, num_cols):
                        # Create columns for this row
                        row_indicators = available_indicator_labels[row_start:row_start + num_cols]
                        cols = st.columns(len(row_indicators), gap="medium")
                        
                        for col_idx, ind_key in enumerate(row_indicators):
                            ind_info = governance_indicators[ind_key]
                            
                            with cols[col_idx]:
                                # Get data for this indicator
                                ind_data = indicator_data_443_1[indicator_data_443_1['indicator_label'] == ind_info["label"]].copy()
                                # If no data found and code exists, try matching by code
                                if ind_data.empty and ind_info.get("code") and 'indicator_code' in indicator_data_443_1.columns:
                                    ind_data = indicator_data_443_1[indicator_data_443_1['indicator_code'].astype(str).str.strip() == ind_info["code"]].copy()
                                
                                if not ind_data.empty:
                                    # Get latest year if "All Years" selected
                                    if selected_year_443_1 == "All Years":
                                        latest_year = ind_data['year'].max()
                                        ind_data = ind_data[ind_data['year'] == latest_year]
                                    
                                    # Sort and get top countries
                                    ind_data_sorted = ind_data.sort_values('value', ascending=False).head(10)
                                    
                                    # Create small chart
                                    fig = go.Figure()
                                    fig.add_trace(go.Bar(
                                        x=ind_data_sorted['country_or_area'],
                                        y=ind_data_sorted['value'],
                                        marker_color=ind_info["color"],
                                        hovertemplate="<b>%{x}</b><br>Year: " + str(ind_data_sorted['year'].iloc[0] if not ind_data_sorted.empty else "") + "<br>Score: %{y:.3f}<br><extra></extra>"
                                    ))
                                    
                                    # Compact layout for small charts
                                    fig.update_layout(
                                        title=dict(
                                            text=f"<b>{ind_key}</b><br><span style='font-size:0.7em; color:#666;'>{ind_info['source']}</span>",
                                            font=dict(size=12),
                                            x=0.5,
                                            xanchor='center'
                                        ),
                                        xaxis_title="",
                                        yaxis_title="Score",
                                        height=350,
                                        margin=dict(l=40, r=20, t=60, b=40),
                                        xaxis={'categoryorder': 'total descending', 'tickangle': -45, 'tickfont': dict(size=8)},
                                        yaxis={'tickfont': dict(size=9)},
                                        showlegend=False
                                    )
                                    
                                    st.plotly_chart(fig, use_container_width=True, key=f"plot_443_1_gradient_{row_start}_{col_idx}")
                                else:
                                    st.info(f"No data for {ind_key}", icon="ℹ️")
                else:
                    st.info("No governance indicator data available. Available indicators: Rule of Law, Control of Corruption: Estimate")
            
            with tab_map_443_1:
                # Map view
                selected_map_indicator_443_1 = st.selectbox(
                    "Select Indicator for Map:",
                    options=available_indicator_labels if available_indicator_labels else ["Rule of Law", "Control of Corruption: Estimate"],
                    key="ind_4_4_3_1_map_indicator"
                )
                
                # Get the indicator info to match by label or code
                if selected_map_indicator_443_1 in governance_indicators:
                    ind_info = governance_indicators[selected_map_indicator_443_1]
                    # Try matching by label first
                    map_data = indicator_data_443_1[indicator_data_443_1['indicator_label'] == ind_info["label"]].copy()
                    # If no data found and code exists, try matching by code
                    if map_data.empty and ind_info.get("code") and 'indicator_code' in indicator_data_443_1.columns:
                        map_data = indicator_data_443_1[indicator_data_443_1['indicator_code'].astype(str).str.strip() == ind_info["code"]].copy()
                    
                    if not map_data.empty:
                        if selected_year_443_1 != "All Years":
                            map_data = map_data[map_data['year'] == int(selected_year_443_1)]
                        else:
                            latest_year = map_data['year'].max()
                            map_data = map_data[map_data['year'] == latest_year]
                        
                        if not map_data.empty:
                            # Merge with reference data for ISO codes
                            map_data_merged = map_data.merge(
                                ref_data[['Country or Area', 'iso3']],
                                left_on='country_or_area',
                                right_on='Country or Area',
                                how='left'
                            )
                            
                            if 'iso3' in map_data_merged.columns and not map_data_merged['iso3'].isna().all():
                                fig = px.choropleth(
                                    map_data_merged,
                                    locations='iso3',
                                    color='value',
                                    hover_name='country_or_area',
                                    hover_data={'year': True, 'value': ':.3f'},
                                    color_continuous_scale='Blues',
                                    title=f"{selected_map_indicator_443_1} - Geographic Distribution"
                                )
                                fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="lightgray")
                                fig.update_layout(height=500, margin=dict(l=0, r=0, t=30, b=0))
                                st.plotly_chart(fig, use_container_width=True, key="plot_443_1_map")
                            else:
                                st.info("No geographic data available for mapping.")
                        else:
                            st.info("No data available for the selected filters.")
                    else:
                        st.info("No data available for the selected indicator.")
                else:
                    st.info(f"No data available for {selected_map_indicator_443_1}")
            
            with tab_table_443_1:
                # Data table - filter by matching labels or codes
                table_data = pd.DataFrame()
                for ind_key in available_indicator_labels:
                    ind_info = governance_indicators[ind_key]
                    # Try matching by label
                    ind_data = indicator_data_443_1[indicator_data_443_1['indicator_label'] == ind_info["label"]].copy()
                    # If no data and code exists, try matching by code
                    if ind_data.empty and ind_info.get("code") and 'indicator_code' in indicator_data_443_1.columns:
                        ind_data = indicator_data_443_1[indicator_data_443_1['indicator_code'].astype(str).str.strip() == ind_info["code"]].copy()
                    if not ind_data.empty:
                        table_data = pd.concat([table_data, ind_data], ignore_index=True)
                
                if not table_data.empty:
                    display_table = table_data[['country_or_area', 'year', 'indicator_label', 'value']].copy()
                    display_table = display_table.rename(columns={
                        'country_or_area': 'Country',
                        'year': 'Year',
                        'indicator_label': 'Indicator',
                        'value': 'Score'
                    })
                    display_table = display_table.sort_values(['Country', 'Year', 'Indicator'])
                    
                    st.dataframe(display_table, use_container_width=True)
                    
                    # CSV download
                    csv = display_table.to_csv(index=False)
                    st.download_button(
                        label="Download Data as CSV",
                        data=csv,
                        file_name=f"indicator_4_4_3_1_data.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
    
            # D. Supporting Information Layers
            with st.expander("Learn more about Indicator 4.4.3.1: Efficacy of Anti-IFF Measures", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
This indicator assesses the efficacy of efforts to combat illicit financial flows (IFFs) by measuring successful prosecutions for IFF-related offenses. Given the challenges in obtaining direct prosecution data across jurisdictions, this study proxies effectiveness using the enablers framework outlined in Coherent Policies for Combatting Illicit Financial Flows (UNODC-OECD, 2016).
                    """)
                with tab_rel:
                    st.markdown("""
The effectiveness of anti-IFF measures is assessed using multiple governance, regulatory, and institutional indicators that influence the ability to combat IFFs effectively. These proxies include Rule of Law (Regulatory Enforcement), Control of Corruption, Sound Institutions, and Identity Documentation.
                    """)
                with tab_proxy:
                    st.markdown("""
**Proxy Justification:**
- The UNODC-OECD framework identifies governance and institutional quality as key determinants of anti-IFF effectiveness.
- The World Justice Project, World Bank, and Mo Ibrahim Index provide validated, cross-country governance data relevant to financial crime control.
- Transparency and identity documentation are essential enablers for tracking and prosecuting illicit financial flows.
                    """)
                with tab_pillar:
                    st.markdown("""
This composite indicator measures how capable a country is in implementing coherent policies to combat IFFs. It integrates multiple governance and institutional metrics to reflect the "effectiveness architecture" behind detection and enforcement.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
**How to Read This Graph:**  
Each sub-indicator represents a key enabler of anti-IFF enforcement. Use the selector to explore performance on rule of law, justice systems, corruption control, institutional quality, and identity documentation. Higher scores = stronger foundations for combating IFFs.

**How to Apply Analytical Lens:**  
- **Efficiency:** Focus on how effectively administrative systems (tax, justice, customs) coordinate enforcement.
- **Effectiveness:** Assess whether strong institutional and governance scores align with actual reductions in IFFs or improved detection/reporting.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicators for this sub-tab
            subtab_indicators_443_1 = {}
            for ind_key, ind_info in governance_indicators.items():
                # Check if indicator exists in data
                if ind_info["label"] in df_filtered['indicator_label'].unique():
                    subtab_indicators_443_1[ind_key] = ind_info["label"]
                elif ind_info.get("code") and 'indicator_code' in df_filtered.columns:
                    if ind_info["code"] in df_filtered['indicator_code'].astype(str).values:
                        subtab_indicators_443_1[ind_key] = ind_info["label"]
            
            if subtab_indicators_443_1:
                africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
                df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
                
                # Calculate coverage summary
                countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_443_1.values())]['country_or_area'].nunique()
                total_africa_countries = len(africa_countries)
                coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
                
                st.markdown(f"""
                <div class="data-availability-box">
                  <div class="left">
                    <h4>Data Availability in Africa</h4>
                    <p>
                      Data availability determines how confidently we can interpret anti-IFF measures trends across Africa. 
                      This view highlights which countries report recent data and where gaps persist — often due to differences in statistical capacity, reporting cycles, or institutional coverage.
                    </p>
                    <p><strong>Use the heatmap below to explore:</strong></p>
                    <ul>
                      <li><strong>Countries with up-to-date reporting</strong> (strong coverage)</li>
                      <li><strong>Countries with partial or outdated data</strong></li>
                      <li><strong>Indicators missing post-2021 updates</strong></li>
                    </ul>
                    <p style="margin-top: 1rem;"><em>Current data coverage: {coverage}% of African countries</em></p>
                  </div>
                  <div class="right">
                    <p><strong>Legend:</strong></p>
                    <ul style="text-align: left;">
                      <li><strong>Dark cells:</strong> Recent, consistent reporting (post-2020)</li>
                      <li><strong>Light cells:</strong> Partial or outdated reporting</li>
                      <li><strong>Empty cells:</strong> Missing or unreported values</li>
                    </ul>
                    <p><em>Hover over a cell in the heatmap below to view country-year coverage.</em></p>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View data availability heatmap", expanded=False):
                    selected_gap_indicator = st.selectbox(
                        "Select indicator to view data availability:",
                        options=list(subtab_indicators_443_1.keys()),
                        key="ind_4_4_3_1_gap_indicator_select"
                    )
                    uv.render_data_availability_heatmap(
                        df=df_africa,
                        indicator_label=subtab_indicators_443_1[selected_gap_indicator],
                        title=f"Data Availability for {selected_gap_indicator} (Africa)",
                        container_key="ind_4_4_3_1_gap"
                    )
    
    # ========================================
    # INDICATOR 4.4.3.2.a: Operating Metrics Audit
    # ========================================
    with subtab_443_2a:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class="indicator-card">
                <h4>Indicator 4.4.3.2.a: Operating Metrics Audit
                    <button type="button" class="info-icon-btn" data-tooltip="Measures operational effectiveness of tax administrations in detecting non-compliance and converting audits into additional assessed revenue. Includes number of audits completed, % of audits leading to adjustment, and additional assessments raised." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p><strong>Analytical Focus Question:</strong> How effective are tax administrations in detecting non-compliance and converting audits into additional assessed revenue?</p>
        </div>
        """, unsafe_allow_html=True)
        
            # B. Local Filter Row
            col_year, col_country, col_region, col_reset = st.columns([2, 3, 3, 1])
            
            with col_year:
                available_years = sorted(df_filtered['year'].dropna().unique(), reverse=True)
                selected_year_443_2a = st.selectbox(
                    "Select Year(s)",
                    options=["All Years"] + [str(int(y)) for y in available_years],
                    key="ind_4_4_3_2a_year_filter",
                    index=0
                )
            
            with col_country:
                available_countries = sorted(df_filtered['country_or_area'].dropna().unique())
                selected_countries_443_2a = st.multiselect(
                    "Select Country",
                    options=available_countries,
                    key="ind_4_4_3_2a_country_filter",
                    default=[]
                )
            
            with col_region:
                africa_regions = sorted(ref_data[ref_data['Region Name'] == 'Africa']['Intermediate Region Name'].dropna().unique())
                selected_regions_443_2a = st.multiselect(
                    "Select Region",
                    options=africa_regions,
                    key="ind_4_4_3_2a_region_filter",
                    default=[]
                )
            
            with col_reset:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_4_3_2a_reset"):
                    for key in ["ind_4_4_3_2a_year_filter", "ind_4_4_3_2a_country_filter", "ind_4_4_3_2a_region_filter"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            
            # Filter data
            indicator_data_443_2a = df_filtered.copy()
            
            # Define operational indicators (from old implementation)
            operational_indicators = {
                "Number of criminal investigations": "Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency",
                "Number of tax dispute resolutions": "FTEs by function of the tax administration-Audit, investigation and other verification",
                "Number of audits / tax crime investigations": "FTEs by function of the tax administration-Audit, investigation and other verification"
            }
            
            # Filter by selections
            if selected_year_443_2a != "All Years":
                indicator_data_443_2a = indicator_data_443_2a[indicator_data_443_2a['year'] == int(selected_year_443_2a)]
            if selected_countries_443_2a:
                indicator_data_443_2a = indicator_data_443_2a[indicator_data_443_2a['country_or_area'].isin(selected_countries_443_2a)]
            if selected_regions_443_2a:
                region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions_443_2a)]['Country or Area'].unique()
                indicator_data_443_2a = indicator_data_443_2a[indicator_data_443_2a['country_or_area'].isin(region_countries)]
            
            # C. Multi-View Tabs
            tab_graph_443_2a, tab_map_443_2a, tab_table_443_2a = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_443_2a:
                # Select operational indicator
                selected_ops_display = st.selectbox(
                    "Select Operational Capacity Indicator:",
                options=list(operational_indicators.keys()),
                    key="ind_4_4_3_2a_ops_select"
            )
                
                ops_label = operational_indicators[selected_ops_display]
                chart_data = indicator_data_443_2a[indicator_data_443_2a['indicator_label'] == ops_label].copy()
                
                if not chart_data.empty:
                    # Get latest year if "All Years" selected
                    if selected_year_443_2a == "All Years":
                        # Show trend over time
                        chart_data_sorted = chart_data.sort_values('year')
                        countries = sorted(chart_data['country_or_area'].unique())
                        
                        fig = go.Figure()
                        for country in countries[:5]:  # Limit to 5 countries
                            country_data = chart_data_sorted[chart_data_sorted['country_or_area'] == country]
                            if not country_data.empty:
                                fig.add_trace(go.Scatter(
                                    x=country_data['year'],
                                    y=country_data['value'],
                                    mode='lines+markers',
                                    name=country,
                                    hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>Value: %{{y:,.0f}}<br><extra></extra>"
                                ))
                        
                        fig.update_layout(
                            title=f"{selected_ops_display} Over Time",
                            xaxis_title="Year",
                            yaxis_title="Value",
                            height=500,
                            hovermode='closest'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True, key=f"plot_443_2a_trend_{selected_ops_display}")
                    else:
                        # Bar chart for single year
                        chart_data_sorted = chart_data.sort_values('value', ascending=False).head(15)
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=chart_data_sorted['country_or_area'],
                            y=chart_data_sorted['value'],
                            marker_color='#0072BC',
                            hovertemplate="<b>%{x}</b><br>Year: " + str(selected_year_443_2a) + "<br>Value: %{y:,.0f}<br><extra></extra>"
                        ))
                        
                        fig.update_layout(
                            title=f"{selected_ops_display} ({selected_year_443_2a})",
                            xaxis_title="Country",
                            yaxis_title="Value",
                            height=500,
                            xaxis={'categoryorder': 'total descending'}
                        )
                        
                        st.plotly_chart(fig, use_container_width=True, key=f"plot_443_2a_bar_{selected_ops_display}")
                else:
                    st.info(f"No data available for {selected_ops_display}.")
            
            with tab_map_443_2a:
                selected_map_indicator_443_2a = st.selectbox(
                    "Select Indicator for Map:",
                    options=list(operational_indicators.keys()),
                    key="ind_4_4_3_2a_map_indicator"
                )
                
                ops_label_map = operational_indicators[selected_map_indicator_443_2a]
                map_data = indicator_data_443_2a[indicator_data_443_2a['indicator_label'] == ops_label_map].copy()
                
                if selected_year_443_2a != "All Years":
                    map_data = map_data[map_data['year'] == int(selected_year_443_2a)]
                else:
                    latest_year = map_data['year'].max()
                    map_data = map_data[map_data['year'] == latest_year]
                
                if not map_data.empty:
                    map_data_merged = map_data.merge(
                        ref_data[['Country or Area', 'iso3']],
                        left_on='country_or_area',
                        right_on='Country or Area',
                        how='left'
                    )
                    
                    if 'iso3' in map_data_merged.columns and not map_data_merged['iso3'].isna().all():
                        fig = px.choropleth(
                            map_data_merged,
                            locations='iso3',
                            color='value',
                            hover_name='country_or_area',
                            hover_data={'year': True, 'value': ':,.0f'},
                            color_continuous_scale='Blues',
                            title=f"{selected_map_indicator_443_2a} - Geographic Distribution"
                        )
                        fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="lightgray")
                        fig.update_layout(height=500, margin=dict(l=0, r=0, t=30, b=0))
                        st.plotly_chart(fig, use_container_width=True, key="plot_443_2a_map")
                    else:
                        st.info("No geographic data available for mapping.")
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_table_443_2a:
                table_data = indicator_data_443_2a[indicator_data_443_2a['indicator_label'].isin(operational_indicators.values())].copy()
                
                if not table_data.empty:
                    display_table = table_data[['country_or_area', 'year', 'indicator_label', 'value']].copy()
                    display_table = display_table.rename(columns={
                        'country_or_area': 'Country',
                        'year': 'Year',
                        'indicator_label': 'Indicator',
                        'value': 'Value'
                    })
                    display_table = display_table.sort_values(['Country', 'Year', 'Indicator'])
                    
                    st.dataframe(display_table, use_container_width=True)
                    
                    csv = display_table.to_csv(index=False)
                    st.download_button(
                        label="Download Data as CSV",
                        data=csv,
                        file_name=f"indicator_4_4_3_2a_data.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            with st.expander("Learn more about Indicator 4.4.3.2.a: Operating Metrics Audit", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
This indicator measures operational effectiveness of tax administrations in detecting non-compliance and converting audits into additional assessed revenue. It includes number of audits completed, percentage of audits leading to adjustment, and additional assessments raised (total and by tax type).
                    """)
                with tab_rel:
                    st.markdown("""
Operating metrics reflect the capacity of tax and customs authorities to detect and prevent IFFs. Higher audit completion rates and additional assessments indicate stronger enforcement capacity.
                    """)
                with tab_proxy:
                    st.markdown("""
**Proxy Justification:**
- IMF ISORA survey provides comprehensive, cross-country data on tax and customs administration operations.
- Resource allocation, staff capacity, and operational effectiveness are key determinants of the ability to detect and prevent IFFs.
                    """)
                with tab_pillar:
                    st.markdown("""
Under Theme 4: DRM Systems and Institutions, this indicator captures a country's operational strength in tax enforcement. It links to Detection and Enforcement by showing how institutional processes translate into real fiscal discipline.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
**How to Read This Graph:**  
Bars show how many audits were completed by each country or year. The line shows the total value of additional assessments raised from those audits. The darker the bar, the more effective audits are at finding discrepancies (higher % of adjustments).

**How to Apply Analytical Lens:**  
- **Efficiency:** A high percentage of audits resulting in adjustments means audit selection is well-targeted and resources are efficiently used.
- **Effectiveness:** High additional assessments reflect strong institutional capacity for enforcement and revenue recovery.
                """)
    
    # ========================================
    # INDICATOR 4.4.3.2.b: Resources and ICT Infrastructure
    # ========================================
    with subtab_443_2b:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class="indicator-card">
                <h4>Indicator 4.4.3.2.b: Resources and ICT Infrastructure
                    <button type="button" class="info-icon-btn" data-tooltip="Measures investment in digital systems and resources for efficient, modern revenue collection. Includes ICT expenditure (% of total), ICT operating cost (% of total operating expenditure), and % staff in ICT support." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p><strong>Analytical Focus Question:</strong> Are tax and customs administrations investing enough in digital systems and resources to enable efficient, modern revenue collection?</p>
        </div>
        """, unsafe_allow_html=True)
        
            # B. Local Filter Row
            col_year, col_country, col_region, col_reset = st.columns([2, 3, 3, 1])
            
            with col_year:
                available_years = sorted(df_filtered['year'].dropna().unique(), reverse=True)
                selected_year_443_2b = st.selectbox(
                    "Select Year(s)",
                    options=["All Years"] + [str(int(y)) for y in available_years],
                    key="ind_4_4_3_2b_year_filter",
                    index=0
                )
            
            with col_country:
                available_countries = sorted(df_filtered['country_or_area'].dropna().unique())
                selected_countries_443_2b = st.multiselect(
                    "Select Country",
                    options=available_countries,
                    key="ind_4_4_3_2b_country_filter",
                    default=[]
                )
            
            with col_region:
                africa_regions = sorted(ref_data[ref_data['Region Name'] == 'Africa']['Intermediate Region Name'].dropna().unique())
                selected_regions_443_2b = st.multiselect(
                    "Select Region",
                    options=africa_regions,
                    key="ind_4_4_3_2b_region_filter",
                    default=[]
                )
            
            with col_reset:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_4_3_2b_reset"):
                    for key in ["ind_4_4_3_2b_year_filter", "ind_4_4_3_2b_country_filter", "ind_4_4_3_2b_region_filter"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            
            # Filter data
            indicator_data_443_2b = df_filtered.copy()
            
            # Define ICT indicators (from old implementation)
            ict_indicators = {
                "Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax": "Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax",
                "Salary expenditure - Derived": "Salary expenditure - Derived",
                "Operating expenditure - Derived": "Operating expenditure - Derived",
                "Operational ICT solutions of the administration are…-Custom built": "Operational ICT solutions of the administration are…-Custom built",
                "Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)": "Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)",
                "Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)": "Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)",
                "Total tax administration FTEs - Derived": "Total tax administration FTEs - Derived"
            }
            
            # Filter by selections
            if selected_year_443_2b != "All Years":
                indicator_data_443_2b = indicator_data_443_2b[indicator_data_443_2b['year'] == int(selected_year_443_2b)]
            if selected_countries_443_2b:
                indicator_data_443_2b = indicator_data_443_2b[indicator_data_443_2b['country_or_area'].isin(selected_countries_443_2b)]
            if selected_regions_443_2b:
                region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions_443_2b)]['Country or Area'].unique()
                indicator_data_443_2b = indicator_data_443_2b[indicator_data_443_2b['country_or_area'].isin(region_countries)]
            
            # C. Multi-View Tabs
            tab_graph_443_2b, tab_map_443_2b, tab_table_443_2b = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_443_2b:
                # Select ICT indicator
                selected_ict_display = st.selectbox(
                    "Select Financial & ICT Resource Indicator:",
                    options=list(ict_indicators.keys()),
                    key="ind_4_4_3_2b_ict_select"
                )
                
                ict_label = ict_indicators[selected_ict_display]
                chart_data = indicator_data_443_2b[indicator_data_443_2b['indicator_label'] == ict_label].copy()
                
                if not chart_data.empty:
                    # Get latest year if "All Years" selected
                    if selected_year_443_2b == "All Years":
                        # Show trend over time
                        chart_data_sorted = chart_data.sort_values('year')
                        countries = sorted(chart_data['country_or_area'].unique())
                        
                        fig = go.Figure()
                        for country in countries[:5]:  # Limit to 5 countries
                            country_data = chart_data_sorted[chart_data_sorted['country_or_area'] == country]
                            if not country_data.empty:
                                fig.add_trace(go.Scatter(
                                    x=country_data['year'],
                                    y=country_data['value'],
                                    mode='lines+markers',
                                    name=country,
                                    hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>Value: %{{y:,.0f}}<br><extra></extra>"
                                ))
                        
                        fig.update_layout(
                            title=f"{selected_ict_display} Over Time",
                            xaxis_title="Year",
                            yaxis_title="Value",
                            height=500,
                            hovermode='closest'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True, key=f"plot_443_2b_trend_{selected_ict_display}")
                    else:
                        # Bar chart for single year
                        chart_data_sorted = chart_data.sort_values('value', ascending=False).head(15)
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=chart_data_sorted['country_or_area'],
                            y=chart_data_sorted['value'],
                            marker_color='#009D8C',
                            hovertemplate="<b>%{x}</b><br>Year: " + str(selected_year_443_2b) + "<br>Value: %{y:,.0f}<br><extra></extra>"
                        ))
                        
                        fig.update_layout(
                            title=f"{selected_ict_display} ({selected_year_443_2b})",
                            xaxis_title="Country",
                            yaxis_title="Value",
                            height=500,
                            xaxis={'categoryorder': 'total descending'}
                        )
                        
                        st.plotly_chart(fig, use_container_width=True, key=f"plot_443_2b_bar_{selected_ict_display}")
                else:
                    st.info(f"No data available for {selected_ict_display}.")
            
            with tab_map_443_2b:
                selected_map_indicator_443_2b = st.selectbox(
                    "Select Indicator for Map:",
                    options=list(ict_indicators.keys()),
                    key="ind_4_4_3_2b_map_indicator"
                )
                
                ict_label_map = ict_indicators[selected_map_indicator_443_2b]
                map_data = indicator_data_443_2b[indicator_data_443_2b['indicator_label'] == ict_label_map].copy()
                
                if selected_year_443_2b != "All Years":
                    map_data = map_data[map_data['year'] == int(selected_year_443_2b)]
                else:
                    latest_year = map_data['year'].max()
                    map_data = map_data[map_data['year'] == latest_year]
                
                if not map_data.empty:
                    map_data_merged = map_data.merge(
                        ref_data[['Country or Area', 'iso3']],
                        left_on='country_or_area',
                        right_on='Country or Area',
                        how='left'
                    )
                    
                    if 'iso3' in map_data_merged.columns and not map_data_merged['iso3'].isna().all():
                        fig = px.choropleth(
                            map_data_merged,
                            locations='iso3',
                            color='value',
                            hover_name='country_or_area',
                            hover_data={'year': True, 'value': ':,.0f'},
                            color_continuous_scale='Blues',
                            title=f"{selected_map_indicator_443_2b} - Geographic Distribution"
                        )
                        fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="lightgray")
                        fig.update_layout(height=500, margin=dict(l=0, r=0, t=30, b=0))
                        st.plotly_chart(fig, use_container_width=True, key="plot_443_2b_map")
                    else:
                        st.info("No geographic data available for mapping.")
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_table_443_2b:
                table_data = indicator_data_443_2b[indicator_data_443_2b['indicator_label'].isin(ict_indicators.values())].copy()
                
                if not table_data.empty:
                    display_table = table_data[['country_or_area', 'year', 'indicator_label', 'value']].copy()
                    display_table = display_table.rename(columns={
                        'country_or_area': 'Country',
                        'year': 'Year',
                        'indicator_label': 'Indicator',
                        'value': 'Value'
                    })
                    display_table = display_table.sort_values(['Country', 'Year', 'Indicator'])
                    
                    st.dataframe(display_table, use_container_width=True)
                    
                    csv = display_table.to_csv(index=False)
                    st.download_button(
                        label="Download Data as CSV",
                        data=csv,
                        file_name=f"indicator_4_4_3_2b_data.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            with st.expander("Learn more about Indicator 4.4.3.2.b: Resources and ICT Infrastructure", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
This indicator measures investment in digital systems and resources for efficient, modern revenue collection. It includes ICT expenditure (% of total), ICT operating cost (% of total operating expenditure), and % staff in ICT support.
                    """)
                with tab_rel:
                    st.markdown("""
Digital infrastructure is essential for modern tax administration. Adequate ICT investment enables efficient data processing, risk assessment, and enforcement capabilities.
                    """)
                with tab_proxy:
                    st.markdown("""
**Proxy Justification:**
- IMF ISORA survey provides comprehensive data on ICT infrastructure and resource allocation in tax administrations.
- ICT investment reflects a country's commitment to modernizing revenue collection systems.
                    """)
                with tab_pillar:
                    st.markdown("""
Under Theme 4: DRM Systems and Institutions, this indicator shows how resource allocation and digital infrastructure support effective tax administration and IFF detection.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
**How to Read This Graph:**  
The scatterplot shows the relationship between ICT staffing and ICT expenditure. Countries in the upper right quadrant have both high ICT staffing and high ICT investment, indicating strong digital capacity.

**How to Apply Analytical Lens:**  
- **Efficiency:** Higher ICT investment relative to staffing suggests efficient use of technology resources.
- **Effectiveness:** Countries with balanced ICT investment and staffing demonstrate stronger capacity for modern revenue collection and IFF detection.
                """)
    
    # ========================================
    # INDICATOR 4.4.3.2.c: Staff Metrics
    # ========================================
    with subtab_443_2c:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class="indicator-card">
                <h4>Indicator 4.4.3.2.c: Staff Metrics
                    <button type="button" class="info-icon-btn" data-tooltip="Measures human capital strength of tax and customs authorities. Includes staff strength levels, academic qualifications, and length of service." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p><strong>Analytical Focus Question:</strong> How strong is the human capital capacity of tax and customs authorities in detecting and preventing IFFs?</p>
        </div>
        """, unsafe_allow_html=True)
        
            # B. Local Filter Row
            col_year, col_country, col_region, col_reset = st.columns([2, 3, 3, 1])
            
            with col_year:
                available_years = sorted(df_filtered['year'].dropna().unique(), reverse=True)
                selected_year_443_2c = st.selectbox(
                    "Select Year(s)",
                    options=["All Years"] + [str(int(y)) for y in available_years],
                    key="ind_4_4_3_2c_year_filter",
                    index=0
                )
            
            with col_country:
                available_countries = sorted(df_filtered['country_or_area'].dropna().unique())
                selected_countries_443_2c = st.multiselect(
                    "Select Country",
                    options=available_countries,
                    key="ind_4_4_3_2c_country_filter",
                    default=[]
                )
            
            with col_region:
                africa_regions = sorted(ref_data[ref_data['Region Name'] == 'Africa']['Intermediate Region Name'].dropna().unique())
                selected_regions_443_2c = st.multiselect(
                    "Select Region",
                    options=africa_regions,
                    key="ind_4_4_3_2c_region_filter",
                    default=[]
                )
            
            with col_reset:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_4_3_2c_reset"):
                    for key in ["ind_4_4_3_2c_year_filter", "ind_4_4_3_2c_country_filter", "ind_4_4_3_2c_region_filter"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            
            # Filter data
            indicator_data_443_2c = df_filtered.copy()
            
            # Define staff metrics indicators (from old implementation)
            staff_indicators = {
                "Staff Strength - Departures in FY": "Staff strength levels -Departures in FY",
                "Staff Strength - No. at end of FY": "Staff strength levels -No. at end of FY",
                "Staff Strength - No. at start of FY": "Staff strength levels -No. at start of FY",
                "Staff Strength - Recruitments in FY": "Staff strength levels -Recruitments in FY",
                "Academic Qualifications - Bachelors degree": "Academic qualifications (No. of staff at the end of FY)-Bachelors degree",
                "Academic Qualifications - Masters degree (or above)": "Academic qualifications (No. of staff at the end of FY)-Masters degree (or above)",
                "Length of Service - 10-19 years": "Length of service (No. of staff at the end of FY)-10-19 years",
                "Length of Service - 5-9 years": "Length of service (No. of staff at the end of FY)-5-9 years",
                "Length of Service - Over 19 years": "Length of service (No. of staff at the end of FY)-Over 19 years",
                "Length of Service - Under 5 years": "Length of service (No. of staff at the end of FY)-Under 5 years"
            }
            
            # Filter by selections
            if selected_year_443_2c != "All Years":
                indicator_data_443_2c = indicator_data_443_2c[indicator_data_443_2c['year'] == int(selected_year_443_2c)]
            if selected_countries_443_2c:
                indicator_data_443_2c = indicator_data_443_2c[indicator_data_443_2c['country_or_area'].isin(selected_countries_443_2c)]
            if selected_regions_443_2c:
                region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions_443_2c)]['Country or Area'].unique()
                indicator_data_443_2c = indicator_data_443_2c[indicator_data_443_2c['country_or_area'].isin(region_countries)]
            
            # C. Multi-View Tabs
            tab_graph_443_2c, tab_map_443_2c, tab_table_443_2c = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_443_2c:
                # Select staff indicator
                selected_staff_display = st.selectbox(
                    "Select Human Capital Strength Indicator:",
                    options=list(staff_indicators.keys()),
                    key="ind_4_4_3_2c_staff_select"
                )
                
                staff_label = staff_indicators[selected_staff_display]
                chart_data = indicator_data_443_2c[indicator_data_443_2c['indicator_label'] == staff_label].copy()
                
                if not chart_data.empty:
                    # Line chart for trends (as per specification)
                    chart_data_sorted = chart_data.sort_values('year')
                    countries = sorted(chart_data['country_or_area'].unique())
                    
                    fig = go.Figure()
                    for country in countries[:5]:  # Limit to 5 countries
                        country_data = chart_data_sorted[chart_data_sorted['country_or_area'] == country]
                        if not country_data.empty:
                            fig.add_trace(go.Scatter(
                                x=country_data['year'],
                                y=country_data['value'],
                                mode='lines+markers',
                                name=country,
                                hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>Number of Staff: %{{y:,.0f}}<br><extra></extra>"
                            ))
                    
                    fig.update_layout(
                        title=f"{selected_staff_display} Over Time",
                        xaxis_title="Year",
                        yaxis_title="Number of Staff",
                        height=500,
                        hovermode='closest',
                        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key=f"plot_443_2c_graph_{selected_staff_display}")
                else:
                    st.info(f"No data available for {selected_staff_display}.")
            
            with tab_map_443_2c:
                selected_map_indicator_443_2c = st.selectbox(
                    "Select Indicator for Map:",
                    options=list(staff_indicators.keys()),
                    key="ind_4_4_3_2c_map_indicator"
                )
                
                staff_label_map = staff_indicators[selected_map_indicator_443_2c]
                map_data = indicator_data_443_2c[indicator_data_443_2c['indicator_label'] == staff_label_map].copy()
                
                if selected_year_443_2c != "All Years":
                    map_data = map_data[map_data['year'] == int(selected_year_443_2c)]
                else:
                    latest_year = map_data['year'].max()
                    map_data = map_data[map_data['year'] == latest_year]
                
                if not map_data.empty:
                    map_data_merged = map_data.merge(
                        ref_data[['Country or Area', 'iso3']],
                        left_on='country_or_area',
                        right_on='Country or Area',
                        how='left'
                    )
                    
                    if 'iso3' in map_data_merged.columns and not map_data_merged['iso3'].isna().all():
                        fig = px.choropleth(
                            map_data_merged,
                            locations='iso3',
                            color='value',
                            hover_name='country_or_area',
                            hover_data={'year': True, 'value': ':,.0f'},
                            color_continuous_scale='Blues',
                            title=f"{selected_map_indicator_443_2c} - Geographic Distribution"
                        )
                        fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="lightgray")
                        fig.update_layout(height=500, margin=dict(l=0, r=0, t=30, b=0))
                        st.plotly_chart(fig, use_container_width=True, key="plot_443_2c_map")
                    else:
                        st.info("No geographic data available for mapping.")
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_table_443_2c:
                table_data = indicator_data_443_2c[indicator_data_443_2c['indicator_label'].isin(staff_indicators.values())].copy()
                
                if not table_data.empty:
                    display_table = table_data[['country_or_area', 'year', 'indicator_label', 'value']].copy()
                    display_table = display_table.rename(columns={
                        'country_or_area': 'Country',
                        'year': 'Year',
                        'indicator_label': 'Indicator',
                        'value': 'Number of Staff'
                    })
                    display_table = display_table.sort_values(['Country', 'Year', 'Indicator'])
                    
                    st.dataframe(display_table, use_container_width=True)
                    
                    csv = display_table.to_csv(index=False)
                    st.download_button(
                        label="Download Data as CSV",
                        data=csv,
                        file_name=f"indicator_4_4_3_2c_data.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            with st.expander("Learn more about Indicator 4.4.3.2.c: Staff Metrics", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
This indicator measures human capital strength of tax and customs authorities. It includes staff strength levels (at start, end, recruitments, departures), academic qualifications (Bachelors, Masters or above), and length of service (Under 5 years, 5-9 years, 10-19 years, Over 19 years).
                    """)
                with tab_rel:
                    st.markdown("""
Staff capacity is a key determinant of tax administration effectiveness. Well-qualified, experienced staff are essential for detecting and preventing IFFs.
                    """)
                with tab_proxy:
                    st.markdown("""
**Proxy Justification:**
- IMF ISORA survey provides comprehensive data on staff metrics, qualifications, and experience in tax administrations.
- Staff capacity reflects a country's ability to effectively implement tax enforcement and IFF detection measures.
                    """)
                with tab_pillar:
                    st.markdown("""
Under Theme 4: DRM Systems and Institutions, this indicator shows how human capital capacity supports effective tax administration and IFF detection capabilities.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
**How to Read This Graph:**  
The line chart shows trends in staff metrics over time. Higher values indicate stronger human capital capacity. Academic qualifications and length of service reflect staff quality and experience.

**How to Apply Analytical Lens:**  
- **Efficiency:** Higher ratios of qualified staff relative to total staff suggest efficient use of human resources.
- **Effectiveness:** Countries with experienced, well-qualified staff demonstrate stronger capacity for complex tax enforcement and IFF detection.
                """)

# ========================================
# SUB-TOPIC 4.4.4 – Transparency and Accountability
# ========================================
with tab_subtopic_4:
    # Create sub-tab for the indicator under 4.4.4
    subtab_444_1, = st.tabs(["4.4.4.1 – Financial Secrecy Index"])
    
    # ========================================
    # INDICATOR 4.4.4.1: Financial Secrecy Index
    # ========================================
    with subtab_444_1:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class="indicator-card">
                <h4>Indicator 4.4.4.1: Financial Secrecy Index
                    <button type="button" class="info-icon-btn" data-tooltip="Measures the volume and value of funds held in offshore accounts by residents. The index combines the volume of financial services provided to non-residents with the secrecy of jurisdictions. Higher scores indicate greater financial secrecy." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p><strong>Analytical Focus Question:</strong> How does a country's financial secrecy level affect its vulnerability to Illicit Financial Flows and its alignment with global transparency standards?</p>
            </div>
            """, unsafe_allow_html=True)
            
            # B. Local Filter Row
            col_year, col_country, col_region, col_reset = st.columns([2, 3, 3, 1])
            
            with col_year:
                available_years = sorted(df_filtered['year'].dropna().unique(), reverse=True)
                selected_year_444_1 = st.selectbox(
                    "Select Year(s)",
                    options=["All Years"] + [str(int(y)) for y in available_years],
                    key="ind_4_4_4_1_year_filter",
                    index=0
                )
            
            with col_country:
                available_countries = sorted(df_filtered['country_or_area'].dropna().unique())
                selected_countries_444_1 = st.multiselect(
                    "Select Country",
                    options=available_countries,
                    key="ind_4_4_4_1_country_filter",
                    default=[]
                )
            
            with col_region:
                africa_regions = sorted(ref_data[ref_data['Region Name'] == 'Africa']['Intermediate Region Name'].dropna().unique())
                selected_regions_444_1 = st.multiselect(
                    "Select Region",
                    options=africa_regions,
                    key="ind_4_4_4_1_region_filter",
                    default=[]
                )
            
            with col_reset:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_4_4_1_reset"):
                    for key in ["ind_4_4_4_1_year_filter", "ind_4_4_4_1_country_filter", "ind_4_4_4_1_region_filter"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
            
            # Filter data - Get FSI indicators (format: fsi_YYYY_value)
            indicator_data_444_1 = df_filtered[
                df_filtered['indicator_label'].str.startswith('fsi_', na=False) & 
                df_filtered['indicator_label'].str.endswith('_value', na=False)
            ].copy()
            
            # Extract year from indicator label and add as a column for easier filtering
            if not indicator_data_444_1.empty:
                indicator_data_444_1['fsi_year'] = indicator_data_444_1['indicator_label'].str.extract(r'fsi_(\d{4})_value')[0].astype(float)
            
            # Normalize FSI values to 0-100 scale per year
            def minmax_0_100(s):
                """Normalize values to 0-100 scale per year"""
                lo, hi = s.min(), s.max()
                if hi > lo:
                    return 100 * (s - lo) / (hi - lo)
                else:
                    return pd.Series([float('nan')] * len(s), index=s.index)
            
            if not indicator_data_444_1.empty:
                # Store original values
                indicator_data_444_1['value_original'] = indicator_data_444_1['value']
                # Apply normalization per year
                indicator_data_444_1['value'] = (
                    indicator_data_444_1.groupby('fsi_year', group_keys=False)['value_original']
                    .apply(minmax_0_100)
                    .round(1)
                )
            
            # Filter by selections
            if selected_year_444_1 != "All Years":
                indicator_data_444_1 = indicator_data_444_1[indicator_data_444_1['fsi_year'] == float(selected_year_444_1)]
            if selected_countries_444_1:
                indicator_data_444_1 = indicator_data_444_1[indicator_data_444_1['country_or_area'].isin(selected_countries_444_1)]
            if selected_regions_444_1:
                region_countries = ref_data[ref_data['Intermediate Region Name'].isin(selected_regions_444_1)]['Country or Area'].unique()
                indicator_data_444_1 = indicator_data_444_1[indicator_data_444_1['country_or_area'].isin(region_countries)]
            
            # C. Multi-View Tabs
            tab_graph_444_1, tab_map_444_1, tab_table_444_1 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_444_1:
                if not indicator_data_444_1.empty:
                    # Prepare data for line chart - aggregate by country and year
                    fsi_chart_data = indicator_data_444_1.groupby(['country_or_area', 'fsi_year'])['value'].first().reset_index()
                    fsi_chart_data = fsi_chart_data.sort_values(['country_or_area', 'fsi_year'])
                    
                    # Limit to top 10 countries by default if no selection
                    if not selected_countries_444_1 and not selected_regions_444_1:
                        latest_values = fsi_chart_data.groupby('country_or_area')['value'].last().reset_index()
                        top_countries = latest_values.nlargest(10, 'value')['country_or_area'].tolist()
                        fsi_chart_data = fsi_chart_data[fsi_chart_data['country_or_area'].isin(top_countries)]
                    
                    # Create line chart
                    fig = go.Figure()
                    
                    # Add shaded areas for risk zones
                    # Low Secrecy (0-40): Transparent jurisdictions - Light Blue
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, x1=1, y0=0, y1=40,
                        fillcolor="#1B75BB",
                        opacity=0.15,
                        layer="below",
                        line_width=0,
                    )
                    # Moderate Secrecy (40-70): Moderate risk - Light Amber
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, x1=1, y0=40, y1=70,
                        fillcolor="#F4B183",
                        opacity=0.15,
                        layer="below",
                        line_width=0,
                    )
                    # High Secrecy (70-100): High risk zone - Light Orange
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, x1=1, y0=70, y1=100,
                        fillcolor="#E87722",
                        opacity=0.15,
                        layer="below",
                        line_width=0,
                    )
                    
                    # Add reference lines at zone boundaries
                    fig.add_hline(
                        y=40,
                        line_dash="dash",
                        line_color="#1B75BB",
                        line_width=1,
                        opacity=0.5,
                        annotation_text="40",
                        annotation_position="right",
                        annotation_font_size=9
                    )
                    fig.add_hline(
                        y=70,
                        line_dash="dash",
                        line_color="#E87722",
                        line_width=1,
                        opacity=0.5,
                        annotation_text="70",
                        annotation_position="right",
                        annotation_font_size=9
                    )
                    
                    # Add annotations for risk zones
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.02, y=20,
                        text="Low Secrecy<br>(0-40)<br>Transparent",
                        showarrow=False,
                        font=dict(size=10, color="#1B75BB"),
                        bgcolor="rgba(255,255,255,0.7)",
                        bordercolor="#1B75BB",
                        borderwidth=1,
                        align="left"
                    )
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.02, y=55,
                        text="Moderate Secrecy<br>(40-70)<br>Moderate Risk",
                        showarrow=False,
                        font=dict(size=10, color="#F4B183"),
                        bgcolor="rgba(255,255,255,0.7)",
                        bordercolor="#F4B183",
                        borderwidth=1,
                        align="left"
                    )
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.02, y=85,
                        text="High Secrecy<br>(70-100)<br>High Risk Zone",
                        showarrow=False,
                        font=dict(size=10, color="#E87722"),
                        bgcolor="rgba(255,255,255,0.7)",
                        bordercolor="#E87722",
                        borderwidth=1,
                        align="left"
                    )
                    
                    # Use distinct colors for each country
                    # OSAA color palette with distinct colors
                    country_colors = [
                        '#003366',  # Deep Blue
                        '#0072BC',  # Medium Blue
                        '#66A7DC',  # Light Blue
                        '#1B75BB',  # Blue
                        '#009D8C',  # Teal
                        '#7C4DFF',  # Purple
                        '#F26C2B',  # Orange
                        '#FFD34E',  # Yellow
                        '#B6E1DC',  # Light Teal
                        '#A7C6ED',  # Light Blue
                        '#B30000',  # Dark Red
                        '#007B33',  # Green
                    ]
                    
                    countries = sorted(fsi_chart_data['country_or_area'].unique())
                    for idx, country in enumerate(countries):
                        country_data = fsi_chart_data[fsi_chart_data['country_or_area'] == country].sort_values('fsi_year')
                        # Use distinct color for each country, cycling through palette
                        country_color = country_colors[idx % len(country_colors)]
                        
                        # Calculate change since first available year
                        first_year = country_data['fsi_year'].min()
                        if pd.notna(first_year) and first_year in country_data['fsi_year'].values:
                            value_first = country_data[country_data['fsi_year'] == first_year]['value'].iloc[0]
                            latest_value = country_data['value'].iloc[-1]
                            change_since_first = latest_value - value_first
                        else:
                            change_since_first = None
                        
                        hover_text = f"<b>{country}</b><br>Year: %{{x}}<br>Normalized Secrecy Score (0-100): %{{y:.1f}}"
                        if change_since_first is not None and pd.notna(change_since_first):
                            hover_text += f"<br>Change since {int(first_year)}: {change_since_first:+.1f}"
                        hover_text += "<extra></extra>"
                        
                        fig.add_trace(go.Scatter(
                            x=country_data['fsi_year'],
                            y=country_data['value'],
                            mode='lines+markers',
                            name=country,
                            line=dict(color=country_color, width=2.5),
                            marker=dict(size=7, color=country_color),
                            hovertemplate=hover_text,
                            showlegend=True
                        ))
                    
                    fig.update_layout(
                        title="Financial Secrecy Index - Multi-Year Trend (Normalized 0-100 per Year)",
                        xaxis_title="Year",
                        yaxis_title="Normalized Financial Secrecy Score (0-100)",
                        height=500,
                        hovermode='closest',
                        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
                        xaxis=dict(tickmode='linear', dtick=2),  # Show every 2 years
                        yaxis=dict(range=[0, 100])  # Ensure y-axis shows 0-100 range
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, key="plot_444_1_graph")
                    
                    # Add color legend
                    st.markdown("""
                    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                        <h5 style="color: #002B7F; margin-bottom: 0.5rem;">Financial Secrecy Score Interpretation</h5>
                        <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
                            <div><span style="color: #1B75BB; font-weight: bold;">●</span> Low Secrecy (0-40): Transparent jurisdictions</div>
                            <div><span style="color: #F4B183; font-weight: bold;">●</span> Moderate Secrecy (40-70): Moderate risk</div>
                            <div><span style="color: #E87722; font-weight: bold;">●</span> High Secrecy (70-100): High risk zone</div>
  </div>
</div>
""", unsafe_allow_html=True)
                else:
                    st.info("No Financial Secrecy Index data available. Data format: fsi_YYYY_value (e.g., fsi_2011_value)")
            
            with tab_map_444_1:
                # Map view - show latest available year
                if not indicator_data_444_1.empty:
                    # Get latest year data
                    latest_fsi_year = indicator_data_444_1['fsi_year'].max()
                    map_data = indicator_data_444_1[indicator_data_444_1['fsi_year'] == latest_fsi_year].copy()
                    
                    if not map_data.empty:
                        # Merge with reference data for ISO codes
                        map_data_merged = map_data.merge(
                            ref_data[['Country or Area', 'iso3']],
                            left_on='country_or_area',
                            right_on='Country or Area',
                            how='left'
                        )
                        
                        if 'iso3' in map_data_merged.columns and not map_data_merged['iso3'].isna().all():
                            # Use custom colorscale matching the line chart
                            # Values are now normalized to 0-100
                            fig = px.choropleth(
                                map_data_merged,
                                locations='iso3',
                                color='value',
                                hover_name='country_or_area',
                                hover_data={'fsi_year': True, 'value': ':.1f'},
                                color_continuous_scale=[[0, '#1B75BB'], [0.4, '#F4B183'], [0.7, '#E87722'], [1, '#E87722']],
                                range_color=[0, 100],
                                title=f"Financial Secrecy Index - Geographic Distribution ({int(latest_fsi_year)}) - Normalized 0-100"
                            )
                            fig.update_geos(visible=False, resolution=50, showcountries=True, countrycolor="lightgray")
                            fig.update_layout(height=500, margin=dict(l=0, r=0, t=30, b=0))
                            st.plotly_chart(fig, use_container_width=True, key="plot_444_1_map")
                        else:
                            st.info("No geographic data available for mapping.")
                    else:
                        st.info("No data available for the selected filters.")
                else:
                    st.info("No Financial Secrecy Index data available.")
            
            with tab_table_444_1:
                # Data table
                if not indicator_data_444_1.empty:
                    # Include both normalized and original values
                    table_cols = ['country_or_area', 'fsi_year', 'value']
                    if 'value_original' in indicator_data_444_1.columns:
                        table_cols.append('value_original')
                    display_table = indicator_data_444_1[table_cols].copy()
                    display_table = display_table.rename(columns={
                        'country_or_area': 'Country',
                        'fsi_year': 'Year',
                        'value': 'Normalized Secrecy Score (0-100)',
                        'value_original': 'Original FSI Value'
                    })
                    # Reorder columns to show normalized score first, then original
                    if 'Original FSI Value' in display_table.columns:
                        cols = ['Country', 'Year', 'Normalized Secrecy Score (0-100)', 'Original FSI Value']
                        display_table = display_table[cols]
                    display_table = display_table.sort_values(['Country', 'Year'])
                    display_table['Year'] = display_table['Year'].astype(int)
                    
                    st.dataframe(display_table, use_container_width=True)
                    
                    # CSV download
                    csv = display_table.to_csv(index=False)
                    st.download_button(
                        label="Download Data as CSV",
                        data=csv,
                        file_name=f"indicator_4_4_4_1_financial_secrecy_index.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            with st.expander("Learn more about Indicator 4.4.4.1: Financial Secrecy Index", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
**Definition:** The Financial Secrecy Index (FSI) measures the volume and value of funds held in offshore accounts by residents. The index combines the volume of financial services provided to non-residents with the secrecy of jurisdictions.

**Data Source:** Financial Secrecy Index (FSI)

**Methodology:**
- Measures the volume of financial services provided to non-residents
- Assesses the secrecy of jurisdictions
- Combines both factors to create a comprehensive index
- Higher scores indicate greater financial secrecy

**Indicator Format:** fsi_YYYY_value (e.g., fsi_2011_value, fsi_2013_value, fsi_2015_value, etc.)
                    """)
                with tab_rel:
                    st.markdown("""
Financial secrecy enables illicit financial flows by allowing individuals and corporations to hide assets and avoid taxation. Countries with high financial secrecy scores are more vulnerable to IFFs and less aligned with global transparency standards.
                    """)
                with tab_proxy:
                    st.markdown("""
**Proxy Justification:**
- The Financial Secrecy Index is a comprehensive measure developed by the Tax Justice Network
- It combines both the scale of financial services and the level of secrecy offered
- Provides standardized, cross-country data on financial transparency
- Regularly updated to reflect changes in financial secrecy regulations
                    """)
                with tab_pillar:
                    st.markdown("""
Under Theme 4: DRM Systems and Institutions, this indicator measures how financial secrecy affects a country's vulnerability to Illicit Financial Flows. Countries with lower secrecy scores demonstrate stronger alignment with global transparency standards and reduced IFF risk.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
**How to Read This Graph:**  
The line chart tracks each country's financial secrecy score over time (2011-2025). Higher scores indicate greater financial secrecy and higher IFF vulnerability. Countries with declining trends show progress toward transparency; rising trends signal increasing risk.

**How to Apply Analytical Lens:**  
- **Efficiency:** Lower secrecy scores reflect efficient implementation of transparency standards and reduced administrative burden from hidden financial flows.
- **Effectiveness:** Countries with consistently low or declining secrecy scores demonstrate effective alignment with global transparency standards and reduced IFF vulnerability.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicators for this sub-tab (FSI indicators start with 'fsi_' and end with '_value')
            africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
            df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
            
            fsi_indicators = df_africa[df_africa['indicator_label'].str.startswith('fsi_', na=False) & 
                                       df_africa['indicator_label'].str.endswith('_value', na=False)]['indicator_label'].unique()
            
            if len(fsi_indicators) > 0:
                subtab_indicators_444_1 = {"Financial Secrecy Index": fsi_indicators[0]}
                
                # Calculate coverage summary
                countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_444_1.values())]['country_or_area'].nunique()
                total_africa_countries = len(africa_countries)
                coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
                
                st.markdown(f"""
                <div class="data-availability-box">
                  <div class="left">
                    <h4>Data Availability in Africa</h4>
                    <p>
                      Data availability determines how confidently we can interpret financial secrecy trends across Africa. 
                      This view highlights which countries report recent data and where gaps persist — often due to differences in statistical capacity, reporting cycles, or institutional coverage.
                    </p>
                    <p><strong>Use the heatmap below to explore:</strong></p>
                    <ul>
                      <li><strong>Countries with up-to-date reporting</strong> (strong coverage)</li>
                      <li><strong>Countries with partial or outdated data</strong></li>
                      <li><strong>Indicators missing post-2021 updates</strong></li>
                    </ul>
                    <p style="margin-top: 1rem;"><em>Current data coverage: {coverage}% of African countries</em></p>
                  </div>
                  <div class="right">
                    <p><strong>Legend:</strong></p>
                    <ul style="text-align: left;">
                      <li><strong>Dark cells:</strong> Recent, consistent reporting (post-2020)</li>
                      <li><strong>Light cells:</strong> Partial or outdated reporting</li>
                      <li><strong>Empty cells:</strong> Missing or unreported values</li>
                    </ul>
                    <p><em>Hover over a cell in the heatmap below to view country-year coverage.</em></p>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View data availability heatmap", expanded=False):
                    selected_gap_indicator = st.selectbox(
                        "Select indicator to view data availability:",
                        options=list(subtab_indicators_444_1.keys()),
                        key="ind_4_4_4_1_gap_indicator_select"
                    )
                    uv.render_data_availability_heatmap(
                        df=df_africa,
                        indicator_label=subtab_indicators_444_1[selected_gap_indicator],
                        title=f"Data Availability for {selected_gap_indicator} (Africa)",
                        container_key="ind_4_4_4_1_gap"
                    )

# ========================================
# SUB-TOPIC 4.4.5 – Financing Resilience
# ========================================
with tab_subtopic_5:
    # Create sub-tabs for the two indicators under 4.4.5
    subtab_445_1, subtab_445_2 = st.tabs([
        "4.4.5.1 – Tax Buoyancy",
        "4.4.5.2 – Social Impact of Lost Tax"
    ])
    
    # Placeholder for each sub-tab - to be implemented
    with subtab_445_1:
        st.info("Indicator 4.4.5.1: Tax Buoyancy - To be implemented with unified dashboard structure")
    
    with subtab_445_2:
        st.info("Indicator 4.4.5.2: Social Impact of Lost Tax - To be implemented with unified dashboard structure")

# ========================================
# SUB-TOPIC 4.4.6 – Sector-Specific Analysis
# ========================================
with tab_subtopic_6:
    # Create sub-tabs for the two indicators under 4.4.6
    subtab_446_1a, subtab_446_1b = st.tabs([
        "4.4.6.1.a – Specific Sectors",
        "4.4.6.1.b – Rent Sharing"
    ])
    
    # Placeholder for each sub-tab - to be implemented
    with subtab_446_1a:
        st.info("Indicator 4.4.6.1.a: Specific Sectors - To be implemented with unified dashboard structure")
    
    with subtab_446_1b:
        st.info("Indicator 4.4.6.1.b: Rent Sharing - To be implemented with unified dashboard structure")
