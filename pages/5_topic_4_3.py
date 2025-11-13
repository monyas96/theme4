import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import streamlit as st
import pandas as pd
import composite_indicator_methods as cim
import universal_viz as uv

# Navigation - Home button and logo
try:
    from app_core.components.navigation import render_navigation_buttons, render_page_logo
    render_page_logo("top-right")
    render_navigation_buttons()
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
filters = uv.setup_sidebar_filters(ref_data, df_main, key_prefix="topic4_3")
df_filtered = uv.filter_dataframe_by_selections(df_main, filters, ref_data)

# Country flag mapping (for Tab 4.3.3)
country_flags = {
    "South Africa": "🇿🇦",
    "Nigeria": "🇳🇬",
    "Kenya": "🇰🇪",
    "Rwanda": "🇷🇼",
    "Ghana": "🇬🇭"
}

# ========================================
# SECTION: Topic Header
# ========================================
with st.container():
    st.markdown("""
    <div class="section-header">
        <h1>Topic 4.3: Capital Markets</h1>
        <p>Capital markets are essential for mobilizing domestic financial resources and channeling savings into productive investments. A well-developed capital market reduces reliance on foreign financing, supports sustainable economic growth, and strengthens financial stability. Effective management of capital markets ensures that resources are directed toward areas that maximize national development.</p>
    </div>
    """, unsafe_allow_html=True)

# Use filtered data directly (no global filters)
df_display = df_filtered.copy()

# ========================================
# SECTION: Key Indicators (Tabs)
# ========================================
# Add orange divider before indicators
st.markdown("""
<div style="border-top: 2px solid #F26C2B; margin: 0.75rem 0; clear: both;"></div>
""", unsafe_allow_html=True)

st.markdown("### Key Indicators Overview")

# Create tabs for each sub-topic
tab_subtopic_1, tab_subtopic_2, tab_subtopic_3 = st.tabs([
    "Sub-topic 4.3.1 – Market Capitalization",
    "Sub-topic 4.3.2 – Financial Intermediation",
    "Sub-topic 4.3.3 – Investment from Institutional Investors"
])

# Add CSS to remove white space
st.markdown("""
<style>
    /* Remove excessive margins and padding globally */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Remove excessive margins and padding */
    .element-container {
        margin-bottom: 0.15rem !important;
        padding-bottom: 0.15rem !important;
        padding-top: 0.15rem !important;
    }
    
    /* Remove white space between markdown elements */
    .stMarkdown {
        margin-bottom: 0.1rem !important;
        margin-top: 0.1rem !important;
    }
    
    /* Reduce section header spacing */
    .section-header {
        margin-bottom: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    .section-header h1 {
        margin-bottom: 0.25rem !important;
    }
    
    .section-header p {
        margin-bottom: 0.25rem !important;
        margin-top: 0.25rem !important;
    }
    
    /* Ensure indicator cards have minimal spacing */
    .indicator-card {
        margin-bottom: 0.25rem !important;
        padding-bottom: 0.15rem !important;
        margin-top: 0.25rem !important;
    }
    
    .indicator-card h4 {
        margin-bottom: 0.25rem !important;
        margin-top: 0.25rem !important;
    }
    
    .indicator-card p {
        margin-bottom: 0.5rem !important;
        margin-top: 0.25rem !important;
    }
    
    /* Ensure tabs have minimal spacing */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        margin-bottom: 0.25rem !important;
        margin-top: 0.25rem !important;
    }
    
    /* Reduce spacing in expanders */
    .streamlit-expanderHeader {
        margin-bottom: 0.15rem !important;
        padding: 0.5rem !important;
    }
    
    .streamlit-expanderContent {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* Make charts fill available space */
    .js-plotly-plot {
        margin: 0 !important;
    }
    
    /* Reduce divider spacing */
    hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Reduce column spacing */
    [data-testid="column"] {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    
    /* Reduce container spacing */
    [data-testid="stContainer"] {
        padding-top: 0.25rem !important;
        padding-bottom: 0.25rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# SUB-TOPIC 4.3.1 – Market Capitalization
# ========================================
with tab_subtopic_1:
    # Create sub-tabs for the three indicators under 4.3.1
    subtab_431_1, subtab_431_2, subtab_431_3 = st.tabs([
        "4.3.1.1 – Market Capitalization (% of GDP)",
        "4.3.1.2 – Bond Market Development",
        "4.3.1.3 – Adequacy of International Reserves"
    ])
    
    # ========================================
    # SUB-TAB 1: Indicator 4.3.1.1 - Market Capitalization to GDP
    # ========================================
    with subtab_431_1:
        with st.container():
            # A. Indicator Header
            st.markdown("""
        <div class='indicator-card'>
            <h4>
                Indicator 4.3.1.1: Market Capitalization to GDP
                <button type="button" class="info-icon-btn" data-tooltip="Measures total value of listed companies as a percentage of GDP. Shows capital mobilization capacity and links to sectoral investment. Higher values indicate deeper, more liquid capital markets relative to the economy." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
            </h4>
            <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                <strong>Analytical Focus Question:</strong> How deep and mature are domestic financial markets relative to the size of the economy — and what does this say about financial sovereignty and resilience?
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
        
        # B. Local Filter Row
        # Calculate Stock Market Capitalization to GDP
        required_labels_stock_cap = [
            'Market capitalization of listed domestic companies (current US$)',
            'GDP (current US$)'
        ]
        calculation_func_stock_cap = lambda df: pd.DataFrame({
            'Stock Market Cap to GDP (%)': (df['Market capitalization of listed domestic companies (current US$)'] / df['GDP (current US$)']) * 100
        }).reset_index()
        df_stock_cap, missing_stock_cap = cim.calculate_indicator_with_gap(
            df_display, required_labels_stock_cap, calculation_func_stock_cap
        )
        df_stock_cap['indicator_label'] = 'Stock Market Cap to GDP (%)'
        df_stock_cap = df_stock_cap.rename(columns={'Stock Market Cap to GDP (%)': 'value'})
        
        # Get filter options
        africa_ref_data_431 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        africa_countries_431 = sorted(africa_ref_data_431['Country or Area'].unique()) if not africa_ref_data_431.empty else []
        available_years_431 = sorted(df_stock_cap['year'].dropna().unique()) if not df_stock_cap.empty else []
        available_regions_431 = sorted(africa_ref_data_431['Intermediate Region Name'].dropna().unique()) if not africa_ref_data_431.empty else []
        
        # Filter row
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 0.7])
        
        with filter_col1:
            selected_year_431 = st.selectbox(
                "Select Year(s)",
                options=["All Years"] + available_years_431,
                index=0,
                key="ind_4_3_1_1_year_filter"
            )
        
        with filter_col2:
            # Add "Select All" option
            country_options_with_all = ["Select All"] + africa_countries_431
            
            # Get current selection from session state
            current_selection = st.session_state.get('ind_4_3_1_1_country_filter', [])
            
            # If current selection contains all countries (but not "Select All"), keep it
            # Otherwise use empty list as default
            default_selection = current_selection if current_selection and current_selection != africa_countries_431 else []
            
            selected_countries_431_raw = st.multiselect(
                "Select Country",
                options=country_options_with_all,
                default=default_selection,
                key="ind_4_3_1_1_country_filter"
            )
            
            # Process "Select All" logic
            if "Select All" in selected_countries_431_raw:
                if len(selected_countries_431_raw) == 1:
                    # Only "Select All" selected - select all countries
                    selected_countries_431 = africa_countries_431.copy()
                    # Update session state to reflect all countries selected (without "Select All")
                    current_state = st.session_state.get('ind_4_3_1_1_country_filter', [])
                    if set(current_state) != set(africa_countries_431):
                        st.session_state.ind_4_3_1_1_country_filter = africa_countries_431.copy()
                        st.rerun()
                else:
                    # "Select All" + others selected - remove "Select All" and keep others
                    selected_countries_431 = [c for c in selected_countries_431_raw if c != "Select All"]
                    # Update session state
                    current_state = st.session_state.get('ind_4_3_1_1_country_filter', [])
                    if set(current_state) != set(selected_countries_431):
                        st.session_state.ind_4_3_1_1_country_filter = selected_countries_431
                        st.rerun()
            else:
                selected_countries_431 = selected_countries_431_raw
        
        with filter_col3:
            selected_regions_431 = st.multiselect(
                "Select Region",
                options=available_regions_431,
                default=[],
                key="ind_4_3_1_1_region_filter"
            )
        
        with filter_col4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Reset", key="ind_4_3_1_1_reset", use_container_width=True):
                if 'ind_4_3_1_1_year_filter' in st.session_state:
                    del st.session_state.ind_4_3_1_1_year_filter
                if 'ind_4_3_1_1_country_filter' in st.session_state:
                    del st.session_state.ind_4_3_1_1_country_filter
                if 'ind_4_3_1_1_region_filter' in st.session_state:
                    del st.session_state.ind_4_3_1_1_region_filter
                st.rerun()
        
        # Prepare filtered data
        filtered_stock_cap = df_stock_cap.copy()
        if selected_year_431 != "All Years":
            filtered_stock_cap = filtered_stock_cap[filtered_stock_cap['year'] == selected_year_431]
        if selected_countries_431:
            filtered_stock_cap = filtered_stock_cap[filtered_stock_cap['country_or_area'].isin(selected_countries_431)]
        if selected_regions_431:
            region_countries_431 = africa_ref_data_431[
                africa_ref_data_431['Intermediate Region Name'].isin(selected_regions_431)
            ]['Country or Area'].unique()
            filtered_stock_cap = filtered_stock_cap[filtered_stock_cap['country_or_area'].isin(region_countries_431)]
        
        # C. Visualization Panel with Multi-View Tabs
        tab_graph_431, tab_map_431, tab_data_431 = st.tabs(["Graph View", "Map View", "Data Table"])
        
        with tab_graph_431:
            # Add "How to Read This Graph" hover button
            st.markdown("""
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <button type="button" class="how-to-read-btn" data-tooltip="The line shows the ratio of stock market capitalization to GDP. Higher values mean larger, more liquid capital markets relative to the economy — a signal of financial depth and domestic investor confidence. Reference bands indicate market depth tiers: below 20% (shallow), 20-60% (developing), and above 60% (deep markets)." style="background: none; border: none; cursor: help; font-size: 0.9em; color: #666; padding: 0.25rem 0.5rem; margin-left: auto;">
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
            
            # View toggle (Line chart vs Scatter plot)
            view_toggle_col1, view_toggle_col2 = st.columns([1, 4])
            with view_toggle_col1:
                chart_view = st.radio(
                    "View:",
                    options=["Line Chart", "Scatter Plot"],
                    index=0,
                    key="ind_4_3_1_1_view_toggle",
                    horizontal=True
                )
            
            # Render chart
            if not filtered_stock_cap.empty:
                import plotly.graph_objects as go
                import numpy as np
                
                # Get GDP per capita data for tooltips and scatter plot
                gdp_pc_label = "GDP per Capita Constant USD - USD - value"
                gdp_pc_data = df_display[df_display['indicator_label'] == gdp_pc_label].copy()
                
                if chart_view == "Scatter Plot":
                    # Scatter plot: Market Cap vs GDP per capita
                    # Merge with GDP per capita data
                    scatter_data = filtered_stock_cap.merge(
                        gdp_pc_data[['country_or_area', 'year', 'value']],
                        on=['country_or_area', 'year'],
                        how='left',
                        suffixes=('_mcap', '_gdppc')
                    )
                    scatter_data = scatter_data.dropna(subset=['value_mcap', 'value_gdppc'])
                    
                    if not scatter_data.empty:
                        fig = go.Figure()
                        
                        # Color encoding by market cap tier
                        for idx, row in scatter_data.iterrows():
                            mcap_pct = row['value_mcap']
                            if mcap_pct > 60:
                                color = '#0072BC'  # Deep markets
                            elif mcap_pct >= 20:
                                color = '#F26C2B'  # Developing
                            else:
                                color = '#FFD34E'  # Shallow
                            
                            fig.add_trace(go.Scatter(
                                x=[row['value_gdppc']],
                                y=[row['value_mcap']],
                                mode='markers',
                                name=row['country_or_area'],
                                marker=dict(
                                    color=color,
                                    size=8,
                                    line=dict(width=1, color='white')
                                ),
                                hovertemplate=(
                                    f"<b>{row['country_or_area']}</b><br>" +
                                    f"Year: {row['year']}<br>" +
                                    f"Market Cap (% of GDP): {row['value_mcap']:.2f}%<br>" +
                                    f"GDP per Capita: ${row['value_gdppc']:,.0f}<br>" +
                                    "<extra></extra>"
                                ),
                                showlegend=False
                            ))
                        
                        fig.update_layout(
                            height=500,
                            xaxis_title="GDP per Capita (Constant USD)",
                            yaxis_title="Market Capitalization (% of GDP)",
                            hovermode='closest',
                            margin=dict(l=50, r=50, t=20, b=50)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Insufficient data for scatter plot. GDP per capita data may be missing.")
                else:
                    # Line chart with reference bands
                    fig = go.Figure()
                    
                    # Identify outliers (countries with values > 200% - like Seychelles)
                    outlier_threshold = 200
                    outlier_countries = filtered_stock_cap.groupby('country_or_area')['value'].max()
                    outlier_countries = outlier_countries[outlier_countries > outlier_threshold].index.tolist()
                    
                    # Get selected countries
                    selected_countries_list = selected_countries_431 if selected_countries_431 else []
                    
                    # Filter out outliers for main chart and regional average calculation
                    # But keep selected countries even if they are outliers
                    filtered_main = filtered_stock_cap[
                        (~filtered_stock_cap['country_or_area'].isin(outlier_countries)) | 
                        (filtered_stock_cap['country_or_area'].isin(selected_countries_list))
                    ].copy()
                    
                    # Calculate regional average (excluding outliers, but including selected countries if they are outliers)
                    # For regional average, always exclude outliers to get accurate average
                    filtered_for_avg = filtered_stock_cap[~filtered_stock_cap['country_or_area'].isin(outlier_countries)].copy()
                    regional_avg = pd.DataFrame()
                    if not filtered_for_avg.empty:
                        regional_avg = filtered_for_avg.groupby('year')['value'].mean().reset_index()
                        regional_avg.columns = ['year', 'regional_avg']
                    
                    # Determine y-axis range
                    # If outliers are selected, include them in range calculation
                    if selected_countries_list and any(c in outlier_countries for c in selected_countries_list):
                        # If outliers are selected, use a wider range
                        y_max = min(filtered_stock_cap['value'].max() * 1.1, 500)  # Allow up to 500% if outliers selected
                    elif not filtered_main.empty:
                        # Otherwise, limit to reasonable range
                        y_max = min(filtered_main['value'].max() * 1.1, 200)  # Cap at 200% or 10% above max
                        y_max = max(y_max, 100)  # At least show up to 100%
                    else:
                        y_max = 200
                    
                    # Add reference bands (shaded areas) with labels
                    # Shallow markets (0-20%)
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=0, x1=1, y1=20,
                        fillcolor="#FFD34E",
                        opacity=0.15,
                        layer="below",
                        line_width=0,
                    )
                    # Developing markets (20-60%)
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=20, x1=1, y1=60,
                        fillcolor="#F26C2B",
                        opacity=0.15,
                        layer="below",
                        line_width=0,
                    )
                    # Deep markets (60%+)
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=60, x1=1, y1=y_max,
                        fillcolor="#0072BC",
                        opacity=0.15,
                        layer="below",
                        line_width=0,
                    )
                    
                    # Add reference line annotations with labels
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.01, y=10,
                        text="Shallow<br>Markets<br>(0-20%)",
                        showarrow=False,
                        font=dict(size=9, color="#666"),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#FFD34E",
                        borderwidth=1,
                        align="left"
                    )
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.01, y=40,
                        text="Developing<br>(20-60%)",
                        showarrow=False,
                        font=dict(size=9, color="#666"),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#F26C2B",
                        borderwidth=1,
                        align="left"
                    )
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.01, y=80,
                        text="Deep<br>Markets<br>(>60%)",
                        showarrow=False,
                        font=dict(size=9, color="#666"),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#0072BC",
                        borderwidth=1,
                        align="left"
                    )
                    
                    # Add regional average line FIRST (so it appears at top of legend)
                    if not regional_avg.empty:
                        # Filter regional avg to match chart data years
                        available_years = filtered_main['year'].unique() if not filtered_main.empty else regional_avg['year'].unique()
                        regional_avg_filtered = regional_avg[regional_avg['year'].isin(available_years)]
                        if not regional_avg_filtered.empty:
                            fig.add_trace(go.Scatter(
                                x=regional_avg_filtered['year'],
                                y=regional_avg_filtered['regional_avg'],
                                mode='lines+markers',
                                name='Africa (Region Average)',
                                line=dict(color='#F26C2B', width=3, dash='dash'),
                                marker=dict(color='#F26C2B', size=8),
                                hovertemplate="<b>Africa (Region Average)</b><br>Year: %{x}<br>Market Cap (% of GDP): %{y:.2f}%<extra></extra>",
                                showlegend=True,
                                legendrank=1  # Ensure it appears first in legend
                            ))
                    
                    # If no countries selected, show top 10 countries by latest value (excluding outliers)
                    if not selected_countries_list and not filtered_main.empty:
                        latest_values = filtered_main.groupby('country_or_area')['value'].last().sort_values(ascending=False)
                        top_countries = latest_values.head(10).index.tolist()
                        countries_to_show = top_countries
                    elif selected_countries_list:
                        # Show selected countries (including outliers if selected)
                        countries_to_show = selected_countries_list
                    else:
                        countries_to_show = []
                    
                    # Add country lines (only for selected/top countries)
                    for country in countries_to_show:
                        # Use full data if country is an outlier (they're in filtered_stock_cap but may not be in filtered_main)
                        if country in outlier_countries:
                            country_data = filtered_stock_cap[filtered_stock_cap['country_or_area'] == country].sort_values('year')
                        else:
                            country_data = filtered_main[filtered_main['country_or_area'] == country].sort_values('year')
                        
                        if not country_data.empty:
                            # Color by latest value tier
                            latest_value = country_data['value'].iloc[-1]
                            if latest_value > 60:
                                line_color = '#0072BC'  # Deep markets
                            elif latest_value >= 20:
                                line_color = '#F26C2B'  # Developing
                            else:
                                line_color = '#FFD34E'  # Shallow
                            
                            # Highlight selected countries
                            if country in selected_countries_list:
                                line_color = '#003366'  # Deep blue for selected
                                line_width = 3
                            else:
                                line_width = 2
                            
                            # Merge with GDP per capita for tooltip
                            country_data_merged = country_data.merge(
                                gdp_pc_data[['country_or_area', 'year', 'value']],
                                on=['country_or_area', 'year'],
                                how='left',
                                suffixes=('_mcap', '_gdppc')
                            )
                            
                            hovertemplate = (
                                f"<b>{country}</b><br>" +
                                "Year: %{x}<br>" +
                                "Market Cap (% of GDP): %{y:.2f}%<br>" +
                                "GDP per Capita: %{customdata:,.0f} USD<br>" +
                                "<extra></extra>"
                            )
                            
                            fig.add_trace(go.Scatter(
                                x=country_data_merged['year'],
                                y=country_data_merged['value_mcap'],
                                mode='lines+markers',
                                name=country,
                                line=dict(color=line_color, width=line_width),
                                marker=dict(color=line_color, size=6 if country in selected_countries_list else 4),
                                hovertemplate=hovertemplate,
                                customdata=country_data_merged['value_gdppc'].fillna(0),
                                showlegend=True
                            ))
                    
                    # Show warning if outliers are excluded
                    if outlier_countries:
                        st.info(f"⚠️ Note: Countries with extreme values (>200% of GDP) are excluded from the main chart for clarity: {', '.join(outlier_countries)}. Select them individually to view their data.")
                    
                    # Add annotations for structural breaks (2014-2016, 2020)
                    if not filtered_stock_cap.empty:
                        years = filtered_stock_cap['year'].unique()
                        if 2014 in years or 2015 in years or 2016 in years:
                            fig.add_vline(
                                x=2015,
                                line_dash="dash",
                                line_color="gray",
                                opacity=0.5,
                                annotation_text="Commodity Shock (2014-2016)",
                                annotation_position="top",
                                annotation_font_size=9
                            )
                        if 2020 in years:
                            fig.add_vline(
                                x=2020,
                                line_dash="dash",
                                line_color="gray",
                                opacity=0.5,
                                annotation_text="COVID-19 (2020)",
                                annotation_position="top",
                                annotation_font_size=9
                            )
                    
                    fig.update_layout(
                        height=500,
                        xaxis_title="Year",
                        yaxis_title="Market Capitalization (% of GDP)",
                        yaxis=dict(range=[0, y_max]),  # Limit y-axis to reasonable range
                        hovermode='closest',
                        legend=dict(
                            orientation="v",
                            yanchor="top",
                            y=1,
                            xanchor="left",
                            x=1.02,
                            font=dict(size=10),
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="rgba(0,0,0,0.2)",
                            borderwidth=1
                        ),
                        margin=dict(l=50, r=180, t=20, b=50)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters.")
        
        with tab_map_431:
            # Map View
            if not filtered_stock_cap.empty:
                map_data_431 = filtered_stock_cap.copy()
                
                # Use the latest year if multiple years, or selected year
                if selected_year_431 != "All Years":
                    map_data_431 = map_data_431[map_data_431['year'] == selected_year_431]
                else:
                    map_data_431 = map_data_431.loc[map_data_431.groupby('country_or_area')['year'].idxmax()]
                
                map_data_431['value'] = pd.to_numeric(map_data_431['value'], errors='coerce')
                map_data_431 = map_data_431.dropna(subset=['value'])
                
                if not map_data_431.empty:
                    africa_ref_431 = ref_data[ref_data['Region Name'] == 'Africa'].copy()
                    if not africa_ref_431.empty and 'Country or Area' in africa_ref_431.columns:
                        map_data_merged_431 = map_data_431.merge(
                            africa_ref_431[['Country or Area', 'iso3']],
                            left_on='country_or_area',
                            right_on='Country or Area',
                            how='inner'
                        )
                        
                        if not map_data_merged_431.empty:
                            iso_col_431 = 'iso3_y' if 'iso3_y' in map_data_merged_431.columns else ('iso3_x' if 'iso3_x' in map_data_merged_431.columns else 'iso3')
                            if iso_col_431 != 'iso3' and iso_col_431 in map_data_merged_431.columns:
                                map_data_merged_431['iso3'] = map_data_merged_431[iso_col_431]
                            
                            fig_map_431 = go.Figure(data=go.Choropleth(
                                locations=map_data_merged_431['iso3'],
                                z=map_data_merged_431['value'],
                                locationmode='ISO-3',
                                colorscale='Blues',
                                showscale=True,
                                text=map_data_merged_431.apply(
                                    lambda row: f"{row['country_or_area']}<br>Market Cap (% of GDP): {row['value']:.2f}%<br>Year: {row['year']}",
                                    axis=1
                                ),
                                hovertemplate='%{text}<extra></extra>',
                                colorbar=dict(title="Market Cap (% of GDP)")
                            ))
                            
                            fig_map_431.update_layout(
                                height=500,
                                geo=dict(
                                    bgcolor='rgba(0,0,0,0)',
                                    lakecolor='rgba(0,0,0,0)',
                                    landcolor='rgba(217, 217, 217, 1)',
                                    subunitcolor='white',
                                    scope='africa',
                                    showframe=False,
                                    showcoastlines=True,
                                    projection_type='natural earth'
                                ),
                                margin={"r":0,"t":0,"l":0,"b":0}
                            )
                            
                            st.plotly_chart(fig_map_431, use_container_width=True)
            else:
                st.info("No data available for the selected filters.")
        
        with tab_data_431:
            # Data Table
            if not filtered_stock_cap.empty:
                display_df_431 = filtered_stock_cap[['country_or_area', 'year', 'value']].copy()
                display_df_431 = display_df_431.rename(columns={'value': 'Market Capitalization (% of GDP)'})
                st.dataframe(display_df_431, use_container_width=True)
                
                csv_431 = display_df_431.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_431,
                    file_name=f"indicator_4_3_1_1_{selected_year_431 if selected_year_431 != 'All Years' else 'all_years'}.csv",
                    mime="text/csv",
                    key="ind_4_3_1_1_download_csv"
                )
            else:
                st.info("No data available for the selected filters.")
        
        # D. Supporting Information Layers
        with st.expander("Learn more about this indicator", expanded=False):
            tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
            with tab_def:
                st.markdown("""
                Measures total value of listed companies as a percentage of GDP. This indicator shows capital mobilization capacity and links to sectoral investment.
                
                **Source:** World Bank - Calculated from Market Capitalization and GDP data
                """)
            with tab_rel:
                st.markdown("""
                - **Efficiency**: Capital mobilization — how effectively savings are channeled into productive investments.
                - **Effectiveness**: Links to sectoral investment — deeper markets support broader economic development.
                """)
            with tab_proxy:
                st.markdown("""
                No proxy needed. This is a calculated indicator derived from World Bank data on market capitalization and GDP.
                """)
            with tab_pillar:
                st.markdown("""
                Under Theme 4: Ownership and Financial Sovereignty, this indicator reveals how domestic capital markets contribute to national financing capacity. Deep, well-capitalized markets empower governments and firms to fund growth from within rather than rely on external debt.
                """)
        
        with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
            st.markdown("""
            **Efficiency:** A growing market cap/GDP ratio suggests that savings are being mobilized and allocated effectively through capital markets. Countries with efficient capital markets can channel domestic savings into productive investments without excessive intermediation costs.
            
            **Effectiveness:** Sustained depth signals institutional confidence, access to finance, and reduced external vulnerability. Effective capital markets support long-term development by providing stable financing for infrastructure, businesses, and government projects.
            """)
        
        # Data Availability Section for this indicator
        st.markdown("""
        <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
        """, unsafe_allow_html=True)
        
        # Get indicator for this sub-tab
        subtab_indicators_431_1 = {"Market Capitalization to GDP": "Stock Market Cap to GDP (%)"}
        africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
        df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
        
        # Calculate coverage summary
        countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_431_1.values())]['country_or_area'].nunique()
        total_africa_countries = len(africa_countries)
        coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
        
        st.markdown(f"""
        <div class="data-availability-box">
          <div class="left">
            <h4>Data Availability in Africa</h4>
            <p>
              Data availability determines how confidently we can interpret market capitalization trends across Africa. 
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
                options=list(subtab_indicators_431_1.keys()),
                key="ind_4_3_1_1_gap_indicator_select"
            )
            uv.render_data_availability_heatmap(
                df=df_africa,
                indicator_label=subtab_indicators_431_1[selected_gap_indicator],
                title=f"Data Availability for {selected_gap_indicator} (Africa)",
                container_key="ind_4_3_1_1_gap"
            )
    
    # ========================================
    # SUB-TAB 2: Indicator 4.3.1.2 - Portfolio Investment Bonds
    # ========================================
    with subtab_431_2:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class='indicator-card'>
                <h4>
                    Indicator 4.3.1.2: Portfolio Investment Bonds
                    <button type="button" class="info-icon-btn" data-tooltip="Measures portfolio investment in bonds (public and private) in current US dollars. Shows how much African economies rely on external bond markets for financing and the volatility of these flows over time." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> How much do African economies rely on external bond markets for financing, and how volatile or sustainable are these flows over time?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # B. Local Filter Row
            # Load Portfolio Investment Bonds data
            bond_indicator_label = "Portfolio investment, bonds (PPG + PNG) (NFL, current US$)"
            df_bonds = df_display[df_display['indicator_label'] == bond_indicator_label].copy()
            
            # Calculate % of GDP for metric toggle
            if not df_bonds.empty:
                # Get GDP data
                gdp_data = df_display[df_display['indicator_label'] == 'GDP (current US$)'].copy()
                if not gdp_data.empty:
                    # Merge with GDP to calculate % of GDP
                    df_bonds_merged = df_bonds.merge(
                        gdp_data[['country_or_area', 'year', 'value']],
                        on=['country_or_area', 'year'],
                        how='left',
                        suffixes=('_bonds', '_gdp')
                    )
                    df_bonds_merged['value_pct_gdp'] = (df_bonds_merged['value_bonds'] / df_bonds_merged['value_gdp']) * 100
                    df_bonds_merged = df_bonds_merged.dropna(subset=['value_bonds'])
                    # Keep both absolute and % of GDP values
                    df_bonds = df_bonds_merged.copy()
            
            # Get filter options
            africa_ref_data_432 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
            africa_countries_432 = sorted(africa_ref_data_432['Country or Area'].unique()) if not africa_ref_data_432.empty else []
            available_years_432 = sorted(df_bonds['year'].dropna().unique()) if not df_bonds.empty else []
            available_regions_432 = sorted(africa_ref_data_432['Intermediate Region Name'].dropna().unique()) if not africa_ref_data_432.empty else []
            
            # Filter row
            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 0.7])
            
            with filter_col1:
                selected_year_432 = st.selectbox(
                    "Select Year(s)",
                    options=["All Years"] + available_years_432,
                    index=0,
                    key="ind_4_3_1_2_year_filter"
                )
            
            with filter_col2:
                # Add "Select All" option
                country_options_with_all_432 = ["Select All"] + africa_countries_432
                
                # Get current selection from session state
                current_selection_432 = st.session_state.get('ind_4_3_1_2_country_filter', [])
                
                # If current selection contains all countries (but not "Select All"), keep it
                # Otherwise use empty list as default
                default_selection_432 = current_selection_432 if current_selection_432 and current_selection_432 != africa_countries_432 else []
                
                selected_countries_432_raw = st.multiselect(
                    "Select Country",
                    options=country_options_with_all_432,
                    default=default_selection_432,
                    key="ind_4_3_1_2_country_filter"
                )
                
                # Process "Select All" logic
                if "Select All" in selected_countries_432_raw:
                    if len(selected_countries_432_raw) == 1:
                        # Only "Select All" selected - select all countries
                        selected_countries_432 = africa_countries_432.copy()
                        # Update session state to reflect all countries selected (without "Select All")
                        current_state_432 = st.session_state.get('ind_4_3_1_2_country_filter', [])
                        if set(current_state_432) != set(africa_countries_432):
                            st.session_state.ind_4_3_1_2_country_filter = africa_countries_432.copy()
                            st.rerun()
                    else:
                        # "Select All" + others selected - remove "Select All" and keep others
                        selected_countries_432 = [c for c in selected_countries_432_raw if c != "Select All"]
                        # Update session state
                        current_state_432 = st.session_state.get('ind_4_3_1_2_country_filter', [])
                        if set(current_state_432) != set(selected_countries_432):
                            st.session_state.ind_4_3_1_2_country_filter = selected_countries_432
                            st.rerun()
                else:
                    selected_countries_432 = selected_countries_432_raw
            
            with filter_col3:
                selected_regions_432 = st.multiselect(
                    "Select Region",
                    options=available_regions_432,
                    default=[],
                    key="ind_4_3_1_2_region_filter"
                )
            
            with filter_col4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_3_1_2_reset", use_container_width=True):
                    if 'ind_4_3_1_2_year_filter' in st.session_state:
                        del st.session_state.ind_4_3_1_2_year_filter
                    if 'ind_4_3_1_2_country_filter' in st.session_state:
                        del st.session_state.ind_4_3_1_2_country_filter
                    if 'ind_4_3_1_2_region_filter' in st.session_state:
                        del st.session_state.ind_4_3_1_2_region_filter
                    st.rerun()
            
            # Prepare filtered data
            filtered_bonds = df_bonds.copy()
            if selected_year_432 != "All Years":
                filtered_bonds = filtered_bonds[filtered_bonds['year'] == selected_year_432]
            if selected_countries_432:
                filtered_bonds = filtered_bonds[filtered_bonds['country_or_area'].isin(selected_countries_432)]
            if selected_regions_432:
                region_countries_432 = africa_ref_data_432[
                    africa_ref_data_432['Intermediate Region Name'].isin(selected_regions_432)
                ]['Country or Area'].unique()
                filtered_bonds = filtered_bonds[filtered_bonds['country_or_area'].isin(region_countries_432)]
            
            # C. Visualization Panel with Multi-View Tabs
            tab_graph_432, tab_map_432, tab_data_432 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_432:
                # Add "How to Read This Graph" hover button
                st.markdown("""
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <button type="button" class="how-to-read-btn" data-tooltip="This heatmap shows portfolio investment bond inflows (% of GDP) across African countries and years. Each cell represents the share of external bond inflows for a specific country and year, normalized between 0 and 1% of GDP to enable comparison across different-sized economies. Rows represent countries, and columns represent years (1970–2022). Color intensity shows reliance on external bond markets — darker blue indicates higher bond inflows as a share of GDP, while white cells indicate minimal or no inflows. The normalization was applied because the original data (in current US$) contained extreme variations between large and small economies. Expressing values as a share of GDP allows users to see relative participation in bond markets rather than absolute scale. How to interpret patterns: – Light or blank cells: little or no access to bond markets. – Dark patches: periods of higher borrowing or market entry. – Gaps: missing data or inactive bond markets." style="background: none; border: none; cursor: help; font-size: 0.9em; color: #666; padding: 0.25rem 0.5rem; margin-left: auto;">
                        How to Read This Graph <span style="font-size: 0.8em;">ℹ️</span>
                    </button>
                </div>
                """, unsafe_allow_html=True)
                
                # View toggle: Normalized Heatmap vs Original Data Line Chart
                view_mode = st.radio(
                    "View:",
                    options=["Normalized Heatmap (0-1% of GDP)", "Original Data (Line Chart)"],
                    index=0,
                    key="ind_4_3_1_2_view_mode",
                    horizontal=True
                )
                
                # Render chart based on view mode
                if not filtered_bonds.empty:
                    import plotly.graph_objects as go
                    import numpy as np
                    
                    if view_mode == "Normalized Heatmap (0-1% of GDP)":
                        # Use only % of GDP for normalized heatmap
                        value_col = 'value_pct_gdp'
                        colorbar_title = "% of GDP"
                        
                        # Fixed scale: 0% to 1% of GDP
                        zmin = 0.0
                        zmax = 1.0
                        
                        # Filter out negative values
                        filtered_bonds_display = filtered_bonds[filtered_bonds[value_col].notna()].copy()
                        if value_col in filtered_bonds_display.columns:
                            # Remove negative values
                            filtered_bonds_display = filtered_bonds_display[filtered_bonds_display[value_col] >= 0]
                    else:
                        # Use original % of GDP data (not normalized) for line chart
                        value_col = 'value_pct_gdp'
                        filtered_bonds_display = filtered_bonds[filtered_bonds[value_col].notna()].copy()
                        if value_col in filtered_bonds_display.columns:
                            # Keep all values including negatives for original view
                            filtered_bonds_display = filtered_bonds_display[filtered_bonds_display[value_col] >= 0]
                    
                    if view_mode == "Normalized Heatmap (0-1% of GDP)":
                        # Prepare heatmap data
                        heatmap_df = filtered_bonds_display[['country_or_area', 'year', value_col]].copy()
                        
                        # Fix Cause 3: Ensure year is properly formatted as integer then string for categorical axis
                        heatmap_df['year'] = pd.to_numeric(heatmap_df['year'], errors='coerce')
                        heatmap_df = heatmap_df.dropna(subset=['year'])  # Remove rows with invalid years
                        
                        # Filter out invalid years (should be between 1970 and 2030 for reasonable data)
                        heatmap_df = heatmap_df[(heatmap_df['year'] >= 1970) & (heatmap_df['year'] <= 2030)]
                        
                        # Convert to int, then to string for categorical axis
                        heatmap_df['year'] = heatmap_df['year'].round().astype(int).astype(str)
                        
                        # Fix Cause 2: Ensure value column is numeric (not string/object)
                        heatmap_df[value_col] = pd.to_numeric(heatmap_df[value_col], errors='coerce')
                        
                        # Remove rows where value is NaN after conversion
                        heatmap_df = heatmap_df.dropna(subset=[value_col])
                        
                        # Filter out negative values (already done above, but ensure)
                        heatmap_df = heatmap_df[heatmap_df[value_col] >= 0]
                        
                        # Normalize values to 0-1% range: cap values above 1% to 1%
                        heatmap_df.loc[heatmap_df[value_col] > zmax, value_col] = zmax
                    
                        # Filter countries with less than 3 non-null data points (optional decluttering)
                        # But only if we have many countries - if few countries, show all
                        # After numeric conversion, check for valid (non-NaN) values
                        country_data_counts = heatmap_df.groupby('country_or_area')[value_col].apply(lambda x: (~pd.isna(x)).sum())
                        if len(country_data_counts) > 20:
                            # Only filter if we have many countries
                            countries_with_sufficient_data = country_data_counts[country_data_counts >= 3].index.tolist()
                            heatmap_df = heatmap_df[heatmap_df['country_or_area'].isin(countries_with_sufficient_data)]
                        else:
                            # Show all countries if we have few
                            countries_with_sufficient_data = country_data_counts.index.tolist()
                        
                        if heatmap_df.empty:
                            st.warning(f"⚠️ No data available for heatmap visualization. Check filters: Year={selected_year_432}, Countries={len(selected_countries_432)}, Regions={len(selected_regions_432)}")
                        else:
                            # Sort countries by number of non-null data points (descending)
                            country_data_counts_filtered = heatmap_df.groupby('country_or_area')[value_col].apply(lambda x: (~pd.isna(x)).sum()).sort_values(ascending=False)
                            sorted_countries = country_data_counts_filtered.index.tolist()
                            
                            # Get sorted years (as strings, since we converted to string)
                            sorted_years = sorted(heatmap_df['year'].unique())
                            
                            # Fix Cause 1: Create pivot table with proper data validation
                            # First, ensure we have valid data before pivoting
                            if heatmap_df.empty or value_col not in heatmap_df.columns:
                                st.warning("⚠️ No valid data available for heatmap after filtering.")
                                heatmap_pivot = pd.DataFrame()
                            else:
                                # Create pivot table for heatmap
                                heatmap_pivot = heatmap_df.pivot_table(
                                    index='country_or_area',
                                    columns='year',
                                    values=value_col,
                                    aggfunc='first'
                                )
                                
                                # Reindex to ensure consistent ordering
                                heatmap_pivot = heatmap_pivot.reindex(sorted_countries)
                                heatmap_pivot = heatmap_pivot.reindex(columns=sorted_years)
                                
                                # Debug: Check if pivot has data
                                if heatmap_pivot.empty:
                                    st.warning(f"⚠️ Pivot table is empty. Original data shape: {heatmap_df.shape}, Countries: {len(sorted_countries)}, Years: {len(sorted_years)}")
                                else:
                                    # Check for NaN values in pivot
                                    nan_count = heatmap_pivot.isna().sum().sum()
                                    total_cells = heatmap_pivot.size
                                    if nan_count == total_cells:
                                        st.warning(f"⚠️ All values in pivot table are NaN. This suggests data alignment issues between countries and years.")
                                    elif nan_count > total_cells * 0.9:
                                        st.info(f"ℹ️ {nan_count}/{total_cells} cells are NaN ({(nan_count/total_cells*100):.1f}%). This is normal for sparse data.")
                            
                            # Debug: Check if pivot table has data
                            if heatmap_pivot.empty or heatmap_pivot.shape[1] == 0:
                                st.warning(f"⚠️ Heatmap data issue: Pivot table is empty or has no columns. Data shape: {heatmap_pivot.shape}, Years: {sorted_years[:10] if len(sorted_years) > 10 else sorted_years}")
                            elif heatmap_pivot.shape[1] == 1:
                                st.info(f"ℹ️ Only one year of data available: {sorted_years[0]}. Consider selecting 'All Years' to see the full time series.")
                            
                            # Prepare customdata for hover (unit label) - only if pivot has data
                            if not heatmap_pivot.empty:
                                customdata_unit = "%"
                                customdata_array = np.full(heatmap_pivot.shape, customdata_unit)
                            else:
                                customdata_array = None
                            
                            # Initialize variables for scope
                            fig = None
                            x_tickvals = None
                            x_values_all = None
                            
                            # Create heatmap (fixed scale 0-1% of GDP)
                            if not heatmap_pivot.empty and heatmap_pivot.shape[1] > 0:
                                # Years are already strings from earlier conversion - keep them as strings
                                x_values_all = heatmap_pivot.columns.tolist()
                                y_values = heatmap_pivot.index.tolist()
                                
                                # Convert to numpy array and ensure proper types
                                # Get values from pivot table
                                z_values = heatmap_pivot.values
                                
                                # Ensure z_values are numeric (float)
                                # Convert any non-numeric values to NaN, then Plotly will handle them as missing
                                z_values = pd.DataFrame(z_values).apply(pd.to_numeric, errors='coerce').values
                                
                                # Verify we have numeric data
                                if z_values.dtype == 'object':
                                    # Last resort: manual conversion
                                    z_values = np.array([[float(val) if pd.notna(val) and val is not None and not (isinstance(val, float) and np.isnan(val)) else np.nan for val in row] for row in z_values], dtype=float)
                                
                                # Check if we have any valid (non-NaN) values
                                valid_count = np.sum(~np.isnan(z_values))
                                if valid_count == 0:
                                    st.warning(f"⚠️ No valid numeric values found in heatmap data. All values are NaN or invalid.")
                                elif valid_count < z_values.size * 0.1:
                                    st.info(f"ℹ️ Only {valid_count}/{z_values.size} cells have valid data ({(valid_count/z_values.size*100):.1f}%). This is normal for sparse datasets.")
                                
                                # Determine which years to show on x-axis (every Nth year to avoid crowding)
                                if len(x_values_all) > 20:
                                    # Show every Nth year if more than 20 years (limit to ~20 labels)
                                    step = max(1, len(x_values_all) // 20)
                                    tick_indices = list(range(0, len(x_values_all), step))
                                    # Always include first and last year
                                    if tick_indices[-1] != len(x_values_all) - 1:
                                        tick_indices.append(len(x_values_all) - 1)
                                    x_tickvals = [x_values_all[i] for i in sorted(set(tick_indices))]
                                else:
                                    # Show all years if 20 or fewer
                                    x_tickvals = x_values_all
                                
                                # Create heatmap figure
                                heatmap_data = {
                                    "z": z_values,
                                    "x": x_values_all,  # All years as strings for category axis
                                    "y": y_values,  # Countries as strings
                                    "colorscale": "Blues",
                                    "showscale": True,
                                    "zmin": zmin,  # Fixed at 0%
                                    "zmax": zmax,  # Fixed at 1%
                                    "xgap": 1,
                                    "ygap": 1,
                                    "hoverongaps": False,
                                    "text": None,  # Hide inline text
                                    "texttemplate": "",  # Ensure no text is shown
                                    "hovertemplate": (
                                        "Country: %{y}<br>" +
                                        "Year: %{x}<br>" +
                                        f"Value: %{{z:.2f}}%<br>" +
                                        "<extra></extra>"
                                    ),
                                    "colorbar": dict(
                                        title=dict(
                                            text=colorbar_title,
                                            font=dict(size=11)
                                        ),
                                        tickfont=dict(size=10)
                                    )
                                }
                                
                                # Only add customdata if it's not None
                                if customdata_array is not None:
                                    heatmap_data['customdata'] = customdata_array
                                
                                fig = go.Figure(data=go.Heatmap(**heatmap_data))
                            else:
                                st.info("Unable to create heatmap: insufficient valid data.")
                            
                            # Add crisis band overlays and update layout (only if figure was created)
                            if fig is not None and x_tickvals is not None:
                                # Shaded region for 2008 Financial Crisis
                                if 2007 in sorted_years or 2008 in sorted_years or 2009 in sorted_years:
                                    fig.add_vrect(
                                        x0=2007.5, x1=2009.5,
                                        fillcolor="grey",
                                        opacity=0.2,
                                        layer="below",
                                        line_width=0
                                    )
                                
                                # Shaded region for 2014-2016 Commodity Shock
                                if 2013 in sorted_years or 2014 in sorted_years or 2015 in sorted_years or 2016 in sorted_years:
                                    fig.add_vrect(
                                        x0=2013.5, x1=2016.5,
                                        fillcolor="grey",
                                        opacity=0.2,
                                        layer="below",
                                        line_width=0
                                    )
                                
                                # Shaded region for COVID-19
                                if 2019 in sorted_years or 2020 in sorted_years or 2021 in sorted_years:
                                    fig.add_vrect(
                                        x0=2019.5, x1=2021.5,
                                        fillcolor="grey",
                                        opacity=0.2,
                                        layer="below",
                                        line_width=0
                                    )
                                
                                # Update layout
                                fig.update_layout(
                                    title=None,  # Remove title as requested
                                    height=600,
                                    xaxis=dict(
                                        title=dict(
                                            text="Year",
                                            font=dict(size=11)
                                        ),
                                        type="category",
                                        tickangle=-45,  # Angle labels for better readability
                                        tickmode='array',
                                        tickvals=x_tickvals,  # Show only selected years
                                        ticktext=x_tickvals,  # Use same values as labels
                                        showticklabels=True,
                                        tickfont=dict(size=9)  # Smaller font for years
                                    ),
                                    yaxis=dict(
                                        title=dict(
                                            text="Country",
                                            font=dict(size=11)
                                        ),
                                        categoryorder="array",
                                        categoryarray=sorted_countries
                                    ),
                                    plot_bgcolor="white",
                                    paper_bgcolor="white",
                                    margin=dict(l=100, r=100, t=60, b=50),
                                    font=dict(size=11)
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Original Data Line Chart View
                        line_df = filtered_bonds_display[['country_or_area', 'year', value_col]].copy()
                        
                        # Ensure year is numeric
                        line_df['year'] = pd.to_numeric(line_df['year'], errors='coerce')
                        line_df = line_df.dropna(subset=['year'])
                        line_df = line_df[(line_df['year'] >= 1970) & (line_df['year'] <= 2030)]
                        line_df['year'] = line_df['year'].round().astype(int)
                        
                        # Ensure value is numeric
                        line_df[value_col] = pd.to_numeric(line_df[value_col], errors='coerce')
                        line_df = line_df.dropna(subset=[value_col])
                        line_df = line_df[line_df[value_col] >= 0]
                        
                        if line_df.empty:
                            st.warning(f"⚠️ No data available for line chart visualization. Check filters: Year={selected_year_432}, Countries={len(selected_countries_432)}, Regions={len(selected_regions_432)}")
                        else:
                            # Sort countries by latest value for better visualization
                            latest_values = line_df.groupby('country_or_area').apply(
                                lambda x: x.loc[x['year'].idxmax(), value_col] if not x.empty else 0
                            ).sort_values(ascending=False)
                            sorted_countries_line = latest_values.index.tolist()
                            
                            # Limit to top 15 countries if too many
                            if len(sorted_countries_line) > 15:
                                top_countries = sorted_countries_line[:15]
                                line_df = line_df[line_df['country_or_area'].isin(top_countries)]
                                sorted_countries_line = top_countries
                                st.info(f"ℹ️ Showing top 15 countries by latest value. {len(sorted_countries_line)} countries displayed.")
                            
                            # Create line chart
                            fig_line = go.Figure()
                            
                            # Generate distinct colors for countries
                            import colorsys
                            n_countries = len(sorted_countries_line)
                            colors = []
                            for i in range(n_countries):
                                hue = i / n_countries
                                rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
                                colors.append(f'rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})')
                            
                            # Add line for each country
                            for idx, country in enumerate(sorted_countries_line):
                                country_data = line_df[line_df['country_or_area'] == country].sort_values('year')
                                if not country_data.empty:
                                    fig_line.add_trace(go.Scatter(
                                        x=country_data['year'],
                                        y=country_data[value_col],
                                        mode='lines+markers',
                                        name=country,
                                        line=dict(color=colors[idx], width=2),
                                        marker=dict(size=4),
                                        hovertemplate=(
                                            f"<b>{country}</b><br>" +
                                            "Year: %{x}<br>" +
                                            f"Value: %{{y:.2f}}%<br>" +
                                            "<extra></extra>"
                                        )
                                    ))
                            
                            # Add crisis band overlays
                            sorted_years_line = sorted(line_df['year'].unique())
                            if 2007 in sorted_years_line or 2008 in sorted_years_line or 2009 in sorted_years_line:
                                fig_line.add_vrect(
                                    x0=2007.5, x1=2009.5,
                                    fillcolor="grey",
                                    opacity=0.2,
                                    layer="below",
                                    line_width=0,
                                    annotation_text="2008 Financial Crisis",
                                    annotation_position="top left"
                                )
                            
                            if 2013 in sorted_years_line or 2014 in sorted_years_line or 2015 in sorted_years_line or 2016 in sorted_years_line:
                                fig_line.add_vrect(
                                    x0=2013.5, x1=2016.5,
                                    fillcolor="grey",
                                    opacity=0.2,
                                    layer="below",
                                    line_width=0,
                                    annotation_text="2014-2016 Commodity Shock",
                                    annotation_position="top left"
                                )
                            
                            if 2019 in sorted_years_line or 2020 in sorted_years_line or 2021 in sorted_years_line:
                                fig_line.add_vrect(
                                    x0=2019.5, x1=2021.5,
                                    fillcolor="grey",
                                    opacity=0.2,
                                    layer="below",
                                    line_width=0,
                                    annotation_text="COVID-19",
                                    annotation_position="top left"
                                )
                            
                            # Update layout
                            fig_line.update_layout(
                                title=None,
                                height=600,
                                xaxis=dict(
                                    title=dict(text="Year", font=dict(size=11)),
                                    tickfont=dict(size=10)
                                ),
                                yaxis=dict(
                                    title=dict(text="Portfolio Investment Bonds (% of GDP)", font=dict(size=11)),
                                    tickfont=dict(size=10)
                                ),
                                plot_bgcolor="white",
                                paper_bgcolor="white",
                                margin=dict(l=80, r=80, t=40, b=50),
                                font=dict(size=11),
                                legend=dict(
                                    orientation="v",
                                    yanchor="top",
                                    y=1,
                                    xanchor="left",
                                    x=1.02,
                                    font=dict(size=9)
                                ),
                                hovermode='closest'
                            )
                            
                            st.plotly_chart(fig_line, use_container_width=True)
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_map_432:
                # Map View
                if not filtered_bonds.empty:
                    map_data_432 = filtered_bonds.copy()
                    
                    # Use the latest year if multiple years, or selected year
                    if selected_year_432 != "All Years":
                        map_data_432 = map_data_432[map_data_432['year'] == selected_year_432]
                    else:
                        map_data_432 = map_data_432.loc[map_data_432.groupby('country_or_area')['year'].idxmax()]
                    
                    # Use absolute values for map
                    map_data_432['value'] = pd.to_numeric(map_data_432.get('value_bonds', map_data_432.get('value', 0)), errors='coerce')
                    map_data_432 = map_data_432.dropna(subset=['value'])
                    
                    if not map_data_432.empty:
                        africa_ref_432 = ref_data[ref_data['Region Name'] == 'Africa'].copy()
                        if not africa_ref_432.empty and 'Country or Area' in africa_ref_432.columns:
                            map_data_merged_432 = map_data_432.merge(
                                africa_ref_432[['Country or Area', 'iso3']],
                                left_on='country_or_area',
                                right_on='Country or Area',
                                how='inner'
                            )
                            
                            if not map_data_merged_432.empty:
                                iso_col_432 = 'iso3_y' if 'iso3_y' in map_data_merged_432.columns else ('iso3_x' if 'iso3_x' in map_data_merged_432.columns else 'iso3')
                                if iso_col_432 != 'iso3' and iso_col_432 in map_data_merged_432.columns:
                                    map_data_merged_432['iso3'] = map_data_merged_432[iso_col_432]
                                
                                fig_map_432 = go.Figure(data=go.Choropleth(
                                    locations=map_data_merged_432['iso3'],
                                    z=map_data_merged_432['value'],
                                    locationmode='ISO-3',
                                    colorscale='Blues',
                                    showscale=True,
                                    text=map_data_merged_432.apply(
                                        lambda row: f"{row['country_or_area']}<br>Bond Inflows: ${row['value']:,.0f} US$<br>Year: {row['year']}",
                                        axis=1
                                    ),
                                    hovertemplate='%{text}<extra></extra>',
                                    colorbar=dict(title="Bond Inflows (US$)")
                                ))
                                
                                fig_map_432.update_layout(
                                    height=500,
                                    geo=dict(
                                        bgcolor='rgba(0,0,0,0)',
                                        lakecolor='rgba(0,0,0,0)',
                                        landcolor='rgba(217, 217, 217, 1)',
                                        subunitcolor='white',
                                        scope='africa',
                                        showframe=False,
                                        showcoastlines=True,
                                        projection_type='natural earth'
                                    ),
                                    margin={"r":0,"t":0,"l":0,"b":0}
                                )
                                
                                st.plotly_chart(fig_map_432, use_container_width=True)
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_data_432:
                # Data Table
                if not filtered_bonds.empty:
                    display_df_432 = filtered_bonds[['country_or_area', 'year']].copy()
                    if 'value_bonds' in filtered_bonds.columns:
                        display_df_432['Portfolio Investment Bonds (US$)'] = filtered_bonds['value_bonds']
                    if 'value_pct_gdp' in filtered_bonds.columns:
                        display_df_432['Portfolio Investment Bonds (% of GDP)'] = filtered_bonds['value_pct_gdp']
                    st.dataframe(display_df_432, use_container_width=True)
                    
                    csv_432 = display_df_432.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_432,
                        file_name=f"indicator_4_3_1_2_{selected_year_432 if selected_year_432 != 'All Years' else 'all_years'}.csv",
                        mime="text/csv",
                        key="ind_4_3_1_2_download_csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
                    Bonds are securities issued with a fixed rate of interest for a period of more than one year. They include net flows through cross-border public and publicly guaranteed and private nonguaranteed bond issues. Data are in current U.S. dollars.
                    
                    **Source:** World Bank - [DT.NFL.BOND.CD](https://data.worldbank.org/indicator/DT.NFL.BOND.CD)
                    """)
                with tab_rel:
                    st.markdown("""
                    - **Efficiency**: Evaluates how well countries attract capital without excessive volatility or cost.
                    - **Effectiveness**: Assesses whether external bond flows contribute to productive financing (vs short-term vulnerability).
                    """)
                with tab_proxy:
                    st.markdown("""
                    Direct indicator from World Bank. No proxy needed.
                    """)
                with tab_pillar:
                    st.markdown("""
                    Under Theme 4: Ownership and Financial Sovereignty, this indicator measures how much African countries rely on external portfolio capital. Stable, moderate flows support development; volatile or excessive inflows can erode fiscal sovereignty and increase vulnerability to global shocks.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
                **Efficiency:** Sustainable portfolios show stable inflows tied to investment and growth. Countries that attract capital without excessive volatility demonstrate efficient financial market integration.
                
                **Effectiveness:** Overreliance or volatility signals vulnerability — external debt servicing risks and limited domestic absorption capacity. Effective bond market development requires balancing access to external financing with maintaining fiscal sovereignty.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicator for this sub-tab
            subtab_indicators_431_2 = {"Portfolio Investment Bonds": "Portfolio investment, bonds (PPG + PNG) (NFL, current US$)"}
            africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
            df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
            
            # Calculate coverage summary
            countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_431_2.values())]['country_or_area'].nunique()
            total_africa_countries = len(africa_countries)
            coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
            
            st.markdown(f"""
            <div class="data-availability-box">
              <div class="left">
                <h4>Data Availability in Africa</h4>
                <p>
                  Data availability determines how confidently we can interpret portfolio investment bonds trends across Africa. 
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
                    options=list(subtab_indicators_431_2.keys()),
                    key="ind_4_3_1_2_gap_indicator_select"
                )
                uv.render_data_availability_heatmap(
                    df=df_africa,
                    indicator_label=subtab_indicators_431_2[selected_gap_indicator],
                    title=f"Data Availability for {selected_gap_indicator} (Africa)",
                    container_key="ind_4_3_1_2_gap"
                )
    
    # ========================================
    # SUB-TAB 3: Indicator 4.3.1.3 - Adequacy of International Reserves
    # ========================================
    with subtab_431_3:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class='indicator-card'>
                <h4>
                    Indicator 4.3.1.3: Adequacy of International Reserves
                    <button type="button" class="info-icon-btn" data-tooltip="Measures the ratio of international reserves to short-term external debt. Ratios above 1.0 mean full coverage; lower values suggest vulnerability to external liquidity shocks." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> Do countries hold enough reserves to manage short-term debt obligations, ensuring macro-financial stability and policy autonomy?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # B. Local Filter Row
            # Calculate Adequacy of International Reserves
            df_reserves = cim.calculate_adequacy_of_international_reserves(df_display)
            if not df_reserves.empty:
                df_reserves = df_reserves.rename(columns={'Adequacy of International Reserves': 'value'})
                df_reserves['indicator_label'] = 'Adequacy of International Reserves'
            
            # Get filter options
            africa_ref_data_433 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
            africa_countries_433 = sorted(africa_ref_data_433['Country or Area'].unique()) if not africa_ref_data_433.empty else []
            available_years_433 = sorted(df_reserves['year'].dropna().unique()) if not df_reserves.empty else []
            available_regions_433 = sorted(africa_ref_data_433['Intermediate Region Name'].dropna().unique()) if not africa_ref_data_433.empty else []
            
            # Filter row
            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 0.7])
            
            with filter_col1:
                selected_year_433 = st.selectbox(
                    "Select Year(s)",
                    options=["All Years"] + available_years_433,
                    index=0,
                    key="ind_4_3_1_3_year_filter"
                )
            
            with filter_col2:
                selected_countries_433 = st.multiselect(
                    "Select Country",
                    options=africa_countries_433,
                    default=[],
                    key="ind_4_3_1_3_country_filter"
                )
            
            with filter_col3:
                selected_regions_433 = st.multiselect(
                    "Select Region",
                    options=available_regions_433,
                    default=[],
                    key="ind_4_3_1_3_region_filter"
                )
            
            with filter_col4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_3_1_3_reset", use_container_width=True):
                    if 'ind_4_3_1_3_year_filter' in st.session_state:
                        del st.session_state.ind_4_3_1_3_year_filter
                    if 'ind_4_3_1_3_country_filter' in st.session_state:
                        del st.session_state.ind_4_3_1_3_country_filter
                    if 'ind_4_3_1_3_region_filter' in st.session_state:
                        del st.session_state.ind_4_3_1_3_region_filter
                    st.rerun()
            
            # Prepare filtered data
            filtered_reserves = df_reserves.copy()
            if selected_year_433 != "All Years":
                filtered_reserves = filtered_reserves[filtered_reserves['year'] == selected_year_433]
            if selected_countries_433:
                filtered_reserves = filtered_reserves[filtered_reserves['country_or_area'].isin(selected_countries_433)]
            if selected_regions_433:
                region_countries_433 = africa_ref_data_433[
                    africa_ref_data_433['Intermediate Region Name'].isin(selected_regions_433)
                ]['Country or Area'].unique()
                filtered_reserves = filtered_reserves[filtered_reserves['country_or_area'].isin(region_countries_433)]
            
            # C. Visualization Panel with Multi-View Tabs
            tab_graph_433, tab_map_433, tab_data_433 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_433:
                # Add "How to Read This Graph" hover button
                st.markdown("""
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <button type="button" class="how-to-read-btn" data-tooltip="Each country's line shows how much of its short-term external debt could be covered by its reserves. Ratios above 1 mean full coverage; lower values suggest vulnerability to external liquidity shocks." style="background: none; border: none; cursor: help; font-size: 0.9em; color: #666; padding: 0.25rem 0.5rem; margin-left: auto;">
                        How to Read This Graph <span style="font-size: 0.8em;">ℹ️</span>
                    </button>
                </div>
                """, unsafe_allow_html=True)
                
                # View toggle (Snapshot View is now the default/main view)
                view_toggle_col1, view_toggle_col2 = st.columns([1, 4])
                with view_toggle_col1:
                    chart_view_433 = st.radio(
                        "View:",
                        options=["Snapshot View", "Trend View"],
                        index=0,  # Snapshot View is now first and default
                        key="ind_4_3_1_3_view_toggle",
                        horizontal=True
                    )
                
                # Render chart
                if not filtered_reserves.empty:
                    import plotly.graph_objects as go
                    import numpy as np
                    
                    fig = go.Figure()
                    
                    if chart_view_433 == "Snapshot View":
                        # Diverging bar chart (latest year) - MAIN VIEW
                        snapshot_year = selected_year_433 if selected_year_433 != "All Years" else filtered_reserves['year'].max()
                        snapshot_data = filtered_reserves[filtered_reserves['year'] == snapshot_year].copy()
                        
                        if not snapshot_data.empty:
                            # Remove any infinity, NaN, or invalid values
                            snapshot_data = snapshot_data[
                                snapshot_data['value'].notna() & 
                                (snapshot_data['value'] != float('inf')) & 
                                (snapshot_data['value'] != float('-inf'))
                            ].copy()
                            
                            if snapshot_data.empty:
                                st.warning("⚠️ No valid data available after filtering out invalid values (infinity, NaN).")
                            else:
                                # Normalize data to handle extreme outliers
                                original_values = snapshot_data['value'].copy()
                                
                                # Calculate percentiles to identify outliers
                                q1 = snapshot_data['value'].quantile(0.25)
                                q3 = snapshot_data['value'].quantile(0.75)
                                iqr = q3 - q1
                                
                                # Define reasonable bounds for visualization
                                # Cap extreme negative values at -10 and extreme positive values at 5
                                lower_bound = max(-10, q1 - 3 * iqr)  # Cap at -10 minimum
                                upper_bound = min(5, q3 + 3 * iqr)  # Cap at 5 maximum
                            
                                # Identify outliers
                                outliers = snapshot_data[
                                    (snapshot_data['value'] < lower_bound) | 
                                    (snapshot_data['value'] > upper_bound)
                                ].copy()
                                
                                # Create normalized values for display
                                snapshot_data['value_normalized'] = snapshot_data['value'].clip(lower=lower_bound, upper=upper_bound)
                                
                                # Show warning if outliers exist
                                if not outliers.empty:
                                    outlier_count = len(outliers)
                                    outlier_names = ', '.join(outliers['country_or_area'].head(3).tolist())
                                    if outlier_count > 3:
                                        outlier_names += f" and {outlier_count - 3} more"
                                    st.warning(
                                        f"⚠️ {outlier_count} country/ies with extreme values ({outlier_names}) have been normalized for better visualization. "
                                        f"Hover over bars to see actual values."
                                    )
                                
                                # Sort by original value for better visualization
                                snapshot_data = snapshot_data.sort_values('value')
                                
                                # Color encoding based on risk tiers (using original values for color)
                                colors = []
                                for val in snapshot_data['value']:
                                    if val >= 1.0:  # ≥100% (Adequate)
                                        colors.append('#007B33')
                                    elif val >= 0.5:  # 50-99% (Moderate)
                                        colors.append('#FFD34E')
                                    else:  # <50% (High risk)
                                        colors.append('#F26C2B')
                                
                                # Create bars with normalized values for display
                                fig.add_trace(go.Bar(
                                    x=snapshot_data['value_normalized'],
                                    y=snapshot_data['country_or_area'],
                                    orientation='h',
                                    marker=dict(color=colors),
                                    customdata=snapshot_data['value'],  # Store original values for hover
                                    hovertemplate=(
                                        "<b>%{y}</b><br>" +
                                        "Reserve Adequacy Ratio: %{customdata:.2f}<br>" +
                                        f"Year: {snapshot_year}<br>" +
                                        "<extra></extra>"
                                    ),
                                    showlegend=False
                                ))
                                
                                # Add reference line at ratio = 1.0
                                fig.add_vline(
                                    x=1.0,
                                    line_dash="solid",
                                    line_color="black",
                                    opacity=0.7,
                                    line_width=2,
                                    annotation_text="Full Coverage (1.0)",
                                    annotation_position="top",
                                    annotation_font_size=10
                                )
                                
                                # Add risk tier bands
                                # Critical Risk (Negative values): Reserves < Short-term debt
                                fig.add_shape(
                                    type="rect",
                                    xref="x", yref="paper",
                                    x0=-10, y0=0, x1=0, y1=1,  # Extend to cover negative values
                                    fillcolor="#B30000",  # Dark red for critical risk
                                    opacity=0.1,
                                    layer="below",
                                    line_width=0,
                                )
                                # High Risk: 0 to 0.5 (<50% coverage)
                                fig.add_shape(
                                    type="rect",
                                    xref="x", yref="paper",
                                    x0=0, y0=0, x1=0.5, y1=1,
                                    fillcolor="#F26C2B",  # Orange
                                    opacity=0.1,
                                    layer="below",
                                    line_width=0,
                                )
                                # Moderate Risk: 0.5 to 1.0 (50-99% coverage)
                                fig.add_shape(
                                    type="rect",
                                    xref="x", yref="paper",
                                    x0=0.5, y0=0, x1=1.0, y1=1,
                                    fillcolor="#FFD34E",  # Yellow
                                    opacity=0.1,
                                    layer="below",
                                    line_width=0,
                                )
                                # Adequate Coverage: 1.0+ (≥100% coverage)
                                fig.add_shape(
                                    type="rect",
                                    xref="x", yref="paper",
                                    x0=1.0, y0=0, x1=5.0, y1=1,
                                    fillcolor="#007B33",  # Green
                                    opacity=0.1,
                                    layer="below",
                                    line_width=0,
                                )
                                
                                # Determine x-axis range based on normalized data
                                x_min = min(snapshot_data['value_normalized'].min(), -1.0)  # Show at least -1 to 2 range
                                x_max = max(snapshot_data['value_normalized'].max(), 2.0)
                                
                                fig.update_layout(
                                    height=500,
                                    xaxis_title="Reserve Adequacy Ratio (Reserves / Short-Term Debt)",
                                    yaxis_title="Country",
                                    hovermode='closest',
                                    margin=dict(l=150, r=50, t=20, b=50),
                                    xaxis=dict(
                                        range=[x_min - 0.5, x_max + 0.5]  # Add padding
                                    )
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info(f"No data available for year {snapshot_year}.")
                    else:
                        # Trend View - Multi-country line chart (secondary view)
                        # Normalize data to handle extreme outliers
                        trend_data = filtered_reserves.copy()
                        
                        # Remove infinity and invalid values
                        trend_data = trend_data[
                            trend_data['value'].notna() & 
                            (trend_data['value'] != float('inf')) & 
                            (trend_data['value'] != float('-inf'))
                        ].copy()
                        
                        if trend_data.empty:
                            st.warning("⚠️ No valid data available for trend view after filtering out invalid values (infinity, NaN).")
                        else:
                            # Calculate normalization bounds
                            q1 = trend_data['value'].quantile(0.25)
                            q3 = trend_data['value'].quantile(0.75)
                            iqr = q3 - q1
                            
                            # Define reasonable bounds for visualization
                            lower_bound = max(-10, q1 - 3 * iqr)  # Cap at -10 minimum
                            upper_bound = min(5, q3 + 3 * iqr)  # Cap at 5 maximum
                            
                            # Create normalized values for display (but keep originals for hover)
                            trend_data['value_normalized'] = trend_data['value'].clip(lower=lower_bound, upper=upper_bound)
                            
                            # Identify outliers
                            outliers = trend_data[
                                (trend_data['value'] < lower_bound) | 
                                (trend_data['value'] > upper_bound)
                            ]
                            
                            if not outliers.empty:
                                outlier_countries = outliers['country_or_area'].unique()
                                st.info(f"ℹ️ {len(outlier_countries)} country/ies with extreme values have been normalized for better visualization. Hover over lines to see actual values.")
                            
                            # Determine y-axis range based on normalized data
                            y_min = min(trend_data['value_normalized'].min(), -2.0)  # Show at least -2 to 3 range
                            y_max = max(trend_data['value_normalized'].max(), 3.0)
                            
                            # Add risk tier bands (shaded areas) with labels
                            # Critical Risk (< 0): Dark red
                            fig.add_shape(
                                type="rect",
                                xref="paper", yref="y",
                                x0=0, y0=y_min, x1=1, y1=0,
                                fillcolor="#B30000",
                                opacity=0.15,
                                layer="below",
                                line_width=0,
                            )
                            # High Risk (0-0.5): Orange - Increased opacity for better readability
                            fig.add_shape(
                                type="rect",
                                xref="paper", yref="y",
                                x0=0, y0=0, x1=1, y1=0.5,
                                fillcolor="#F26C2B",
                                opacity=0.25,
                                layer="below",
                                line_width=0,
                            )
                            # Moderate Risk (0.5-1.0): Yellow
                            fig.add_shape(
                                type="rect",
                                xref="paper", yref="y",
                                x0=0, y0=0.5, x1=1, y1=1.0,
                                fillcolor="#FFD34E",
                                opacity=0.15,
                                layer="below",
                                line_width=0,
                            )
                            # Adequate Coverage (≥1.0): Green
                            fig.add_shape(
                                type="rect",
                                xref="paper", yref="y",
                                x0=0, y0=1.0, x1=1, y1=y_max,
                                fillcolor="#007B33",
                                opacity=0.15,
                                layer="below",
                                line_width=0,
                            )
                            
                            # Add labeled annotations for risk tiers (similar to 4.3.1.1 style)
                            fig.add_annotation(
                                xref="paper", yref="y",
                                x=0.01, y=(y_min + 0) / 2,  # Middle of critical risk zone
                                text="Critical<br>Risk<br>(< 0)",
                                showarrow=False,
                                font=dict(size=9, color="#666"),
                                bgcolor="rgba(255,255,255,0.8)",
                                bordercolor="#B30000",
                                borderwidth=1,
                                align="left"
                            )
                            fig.add_annotation(
                                xref="paper", yref="y",
                                x=0.01, y=0.25,  # Middle of high risk zone
                                text="High Risk<br>(0-0.5)",
                                showarrow=False,
                                font=dict(size=9, color="#666"),
                                bgcolor="rgba(255,255,255,0.8)",
                                bordercolor="#F26C2B",
                                borderwidth=1,
                                align="left"
                            )
                            fig.add_annotation(
                                xref="paper", yref="y",
                                x=0.01, y=0.75,  # Middle of moderate risk zone
                                text="Moderate<br>Risk<br>(0.5-1.0)",
                                showarrow=False,
                                font=dict(size=9, color="#666"),
                                bgcolor="rgba(255,255,255,0.8)",
                                bordercolor="#FFD34E",
                                borderwidth=1,
                                align="left"
                            )
                            fig.add_annotation(
                                xref="paper", yref="y",
                                x=0.01, y=(1.0 + y_max) / 2,  # Middle of adequate zone
                                text="Adequate<br>Coverage<br>(≥1.0)",
                                showarrow=False,
                                font=dict(size=9, color="#666"),
                                bgcolor="rgba(255,255,255,0.8)",
                                bordercolor="#007B33",
                                borderwidth=1,
                                align="left"
                            )
                            
                            # Add reference line at ratio = 1.0
                            fig.add_hline(
                                y=1.0,
                                line_dash="solid",
                                line_color="black",
                                opacity=0.7,
                                line_width=2,
                                annotation_text="Full Coverage (1.0)",
                                annotation_position="right",
                                annotation_font_size=10
                            )
                            
                            # Get selected countries
                            selected_countries_list_433 = selected_countries_433 if selected_countries_433 else []
                            
                            # If no countries selected, choose representative countries for each risk tier
                            if not selected_countries_list_433:
                                # Get latest values for each country
                                latest_values = trend_data.groupby('country_or_area').apply(
                                    lambda x: x.loc[x['year'].idxmax(), 'value'] if not x.empty else None
                                ).dropna()
                                
                                # Filter countries with sufficient data (at least 5 years of data)
                                countries_with_sufficient_data = trend_data.groupby('country_or_area').size()
                                countries_with_sufficient_data = countries_with_sufficient_data[countries_with_sufficient_data >= 5].index.tolist()
                                latest_values = latest_values[latest_values.index.isin(countries_with_sufficient_data)]
                                
                                # Categorize countries by risk tier
                                adequate_countries = latest_values[latest_values >= 1.0].sort_values(ascending=False)
                                moderate_countries = latest_values[(latest_values >= 0.5) & (latest_values < 1.0)].sort_values(ascending=False)
                                high_risk_countries = latest_values[(latest_values >= 0) & (latest_values < 0.5)].sort_values(ascending=False)
                                critical_countries = latest_values[latest_values < 0].sort_values(ascending=True)  # Most negative first
                                
                                # Select ONE clear representative from each tier (for maximum clarity)
                                # Prioritize countries with stable patterns and clear tier representation
                                default_countries = []
                                
                                # Helper function to find country with most stable pattern in a tier
                                def find_representative_country(country_list, tier_name):
                                    if len(country_list) == 0:
                                        return None
                                    # For each country, calculate how consistently it stays in its tier
                                    best_country = None
                                    best_score = -1
                                    
                                    for country in country_list.index[:5]:  # Check top 5 candidates
                                        country_data = trend_data[trend_data['country_or_area'] == country].sort_values('year')
                                        if len(country_data) < 5:  # Need at least 5 years
                                            continue
                                        
                                        # Count how many years the country stays in its tier
                                        if tier_name == "adequate":
                                            in_tier = (country_data['value'] >= 1.0).sum()
                                        elif tier_name == "moderate":
                                            in_tier = ((country_data['value'] >= 0.5) & (country_data['value'] < 1.0)).sum()
                                        elif tier_name == "high":
                                            in_tier = ((country_data['value'] >= 0) & (country_data['value'] < 0.5)).sum()
                                        else:  # critical
                                            in_tier = (country_data['value'] < 0).sum()
                                        
                                        score = in_tier / len(country_data)  # Percentage of time in tier
                                        
                                        if score > best_score:
                                            best_score = score
                                            best_country = country
                                    
                                    # If no good representative found, just use the first one
                                    return best_country if best_country else country_list.index[0]
                                
                                # Select only 3 countries for maximum clarity: one from each major tier
                                # 1. Adequate coverage: best country
                                if len(adequate_countries) > 0:
                                    rep = find_representative_country(adequate_countries, "adequate")
                                    if rep:
                                        default_countries.append(rep)
                                
                                # 2. Moderate risk: best country in this range (represents 0.5-1.0)
                                if len(moderate_countries) > 0:
                                    rep = find_representative_country(moderate_countries, "moderate")
                                    if rep:
                                        default_countries.append(rep)
                                
                                # 3. Critical risk: worst country (represents <0, most negative but not extreme)
                                if len(critical_countries) > 0:
                                    # Get the worst but not too extreme (avoid -20k type outliers)
                                    critical_filtered = critical_countries[critical_countries >= -10]  # Cap at -10
                                    if len(critical_filtered) > 0:
                                        rep = find_representative_country(critical_filtered, "critical")
                                        if rep:
                                            default_countries.append(rep)
                                    else:
                                        # If all are too extreme, take the least extreme
                                        default_countries.append(critical_countries.index[-1])  # Last = least negative
                                
                                # Use exactly 3 countries for maximum clarity (plus regional average = 4 lines total)
                                countries_to_display = default_countries[:3]
                            else:
                                # Use selected countries
                                countries_to_display = selected_countries_list_433
                            
                            # Add regional average line first (if available)
                            regional_avg = trend_data.groupby('year')['value'].mean().reset_index()
                            regional_avg = regional_avg.sort_values('year')
                            regional_avg['value_normalized'] = regional_avg['value'].clip(lower=lower_bound, upper=upper_bound)
                            
                            if not regional_avg.empty:
                                fig.add_trace(go.Scatter(
                                    x=regional_avg['year'],
                                    y=regional_avg['value_normalized'],
                                    customdata=regional_avg['value'],
                                    mode='lines+markers',
                                    name='Africa (Region Average)',
                                    line=dict(color='#F26C2B', width=3, dash='dash'),
                                    marker=dict(color='#F26C2B', size=8),
                                    hovertemplate=(
                                        "<b>Africa (Region Average)</b><br>" +
                                        "Year: %{x}<br>" +
                                        "Reserve Adequacy Ratio: %{customdata:.2f}<br>" +
                                        "<extra></extra>"
                                    ),
                                    showlegend=True,
                                    legendrank=1  # Ensure it appears first in legend
                                ))
                            
                            # Add country lines (using normalized values for display)
                            for country in countries_to_display:
                                if country not in trend_data['country_or_area'].values:
                                    continue
                                    
                                country_data = trend_data[trend_data['country_or_area'] == country].sort_values('year')
                                country_data = country_data.dropna(subset=['value', 'value_normalized'])
                                
                                if not country_data.empty:
                                    # Color encoding based on latest value tier (using original value)
                                    latest_value = country_data['value'].iloc[-1]
                                    if latest_value >= 1.0:
                                        line_color = '#007B33'  # Adequate
                                    elif latest_value >= 0.5:
                                        line_color = '#FFD34E'  # Moderate
                                    elif latest_value >= 0:
                                        line_color = '#F26C2B'  # High risk
                                    else:
                                        line_color = '#B30000'  # Critical risk
                                    
                                    # Make default countries more visible (thicker lines)
                                    if not selected_countries_list_433:
                                        # Default view: make all default countries prominent
                                        line_width = 3
                                    elif country in selected_countries_list_433:
                                        # Explicitly selected: highlight in deep blue
                                        line_color = '#003366'  # Deep blue for selected
                                        line_width = 3
                                    else:
                                        line_width = 2
                                    
                                    # Use normalized values for y-axis, original values in hover
                                    hovertemplate = (
                                        f"<b>{country}</b><br>" +
                                        "Year: %{x}<br>" +
                                        "Reserve Adequacy Ratio: %{customdata:.2f}<br>" +
                                        "<extra></extra>"
                                    )
                                    
                                    # Use different line styles for default countries to make them more distinct
                                    line_dash = None
                                    if not selected_countries_list_433:
                                        # In default view, use different dash styles for visual distinction
                                        dash_styles = ['solid', 'dash', 'dot']
                                        country_idx = countries_to_display.index(country) if country in countries_to_display else 0
                                        if country_idx < len(dash_styles):
                                            line_dash = dash_styles[country_idx]
                                    
                                    fig.add_trace(go.Scatter(
                                        x=country_data['year'],
                                        y=country_data['value_normalized'],  # Use normalized for display
                                        customdata=country_data['value'],  # Store original for hover
                                        mode='lines+markers',
                                        name=country,
                                        line=dict(
                                            color=line_color, 
                                            width=line_width,
                                            dash=line_dash if line_dash else 'solid'
                                        ),
                                        marker=dict(
                                            color=line_color, 
                                            size=8 if not selected_countries_list_433 else (6 if country in selected_countries_list_433 else 4)
                                        ),
                                        hovertemplate=hovertemplate,
                                        showlegend=True
                                    ))
                            
                            # Add annotations for crisis years (2008, 2014, 2020)
                            years_433 = trend_data['year'].unique()
                            if 2008 in years_433:
                                fig.add_vline(
                                    x=2008,
                                    line_dash="dash",
                                    line_color="gray",
                                    opacity=0.5,
                                    annotation_text="2008 Financial Crisis",
                                    annotation_position="top",
                                    annotation_font_size=9
                                )
                            if 2014 in years_433:
                                fig.add_vline(
                                    x=2014,
                                    line_dash="dash",
                                    line_color="gray",
                                    opacity=0.5,
                                    annotation_text="2014 Commodity Slump",
                                    annotation_position="top",
                                    annotation_font_size=9
                                )
                            if 2020 in years_433:
                                fig.add_vline(
                                    x=2020,
                                    line_dash="dash",
                                    line_color="gray",
                                    opacity=0.5,
                                    annotation_text="COVID-19 (2020)",
                                    annotation_position="top",
                                    annotation_font_size=9
                                )
                            
                            fig.update_layout(
                                height=500,
                                xaxis_title="Year",
                                yaxis_title="Reserve Adequacy Ratio (Reserves / Short-Term Debt)",
                                hovermode='closest',
                                yaxis=dict(
                                    range=[y_min - 0.5, y_max + 0.5]  # Set y-axis range based on normalized data
                                ),
                                legend=dict(
                                    orientation="v",
                                yanchor="top",
                                y=1,
                                xanchor="left",
                                x=1.02,
                                font=dict(size=10),
                                bgcolor="rgba(255,255,255,0.8)",
                                bordercolor="rgba(0,0,0,0.2)",
                                borderwidth=1
                            ),
                            margin=dict(l=50, r=180, t=20, b=50)
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_map_433:
                # Map View
                if not filtered_reserves.empty:
                    map_data_433 = filtered_reserves.copy()
                    
                    # Use the latest year if multiple years, or selected year
                    if selected_year_433 != "All Years":
                        map_data_433 = map_data_433[map_data_433['year'] == selected_year_433]
                    else:
                        map_data_433 = map_data_433.loc[map_data_433.groupby('country_or_area')['year'].idxmax()]
                    
                    map_data_433['value'] = pd.to_numeric(map_data_433['value'], errors='coerce')
                    map_data_433 = map_data_433.dropna(subset=['value'])
                    
                    if not map_data_433.empty:
                        africa_ref_433 = ref_data[ref_data['Region Name'] == 'Africa'].copy()
                        if not africa_ref_433.empty and 'Country or Area' in africa_ref_433.columns:
                            map_data_merged_433 = map_data_433.merge(
                                africa_ref_433[['Country or Area', 'iso3']],
                                left_on='country_or_area',
                                right_on='Country or Area',
                                how='inner'
                            )
                            
                            if not map_data_merged_433.empty:
                                iso_col_433 = 'iso3_y' if 'iso3_y' in map_data_merged_433.columns else ('iso3_x' if 'iso3_x' in map_data_merged_433.columns else 'iso3')
                                if iso_col_433 != 'iso3' and iso_col_433 in map_data_merged_433.columns:
                                    map_data_merged_433['iso3'] = map_data_merged_433[iso_col_433]
                                
                                fig_map_433 = go.Figure(data=go.Choropleth(
                                    locations=map_data_merged_433['iso3'],
                                    z=map_data_merged_433['value'],
                                    locationmode='ISO-3',
                                    colorscale='RdYlGn',  # Red-Yellow-Green for risk tiers
                                    showscale=True,
                                    text=map_data_merged_433.apply(
                                        lambda row: f"{row['country_or_area']}<br>Reserve Adequacy Ratio: {row['value']:.2f}<br>Year: {row['year']}",
                                        axis=1
                                    ),
                                    hovertemplate='%{text}<extra></extra>',
                                    colorbar=dict(title="Reserve Adequacy Ratio")
                                ))
                                
                                fig_map_433.update_layout(
                                    height=500,
                                    geo=dict(
                                        bgcolor='rgba(0,0,0,0)',
                                        lakecolor='rgba(0,0,0,0)',
                                        landcolor='rgba(217, 217, 217, 1)',
                                        subunitcolor='white',
                                        scope='africa',
                                        showframe=False,
                                        showcoastlines=True,
                                        projection_type='natural earth'
                                    ),
                                    margin={"r":0,"t":0,"l":0,"b":0}
                                )
                                
                                st.plotly_chart(fig_map_433, use_container_width=True)
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_data_433:
                # Data Table
                if not filtered_reserves.empty:
                    display_df_433 = filtered_reserves[['country_or_area', 'year', 'value']].copy()
                    display_df_433 = display_df_433.rename(columns={'value': 'Reserve Adequacy Ratio'})
                    st.dataframe(display_df_433, use_container_width=True)
                    
                    csv_433 = display_df_433.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_433,
                        file_name=f"indicator_4_3_1_3_{selected_year_433 if selected_year_433 != 'All Years' else 'all_years'}.csv",
                        mime="text/csv",
                        key="ind_4_3_1_3_download_csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
                    Ratio of International Reserves (BoP, current US$) to External Debt Stocks, Short-Term (DOD, Current US$).
                    
                    **Interpretation:**
                    - **>1 (≥100%)**: Full coverage (resilient)
                    - **0.5–1 (50–99%)**: Partial coverage (vulnerable)
                    - **<0.5 (<50%)**: High risk (liquidity constraint)
                    
                    **Source:** World Bank - Calculated from Reserves and Short-Term Debt data
                    """)
                with tab_rel:
                    st.markdown("""
                    - **Efficiency**: Evaluates prudent financial management — whether reserves are built sustainably without over-hoarding.
                    - **Effectiveness**: Measures policy capacity to respond to shocks, stabilize exchange rates, and manage liquidity crises.
                    """)
                with tab_proxy:
                    st.markdown("""
                    Calculated indicator. See methodology above.
                    """)
                with tab_pillar:
                    st.markdown("""
                    Under Theme 4 this indicator measures a country's ability to protect itself from external volatility. Adequate reserves mean greater control over national financial policy — a foundation for fiscal and monetary independence.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
                **Efficiency:** Stable or rising ratios reflect disciplined reserve accumulation without overburdening fiscal space. Countries that maintain adequate reserves without excessive hoarding demonstrate efficient financial management.
                
                **Effectiveness:** Adequate reserves enable governments to absorb external shocks — a sign of resilient and self-reliant financial governance. Effective reserve management supports policy autonomy and reduces vulnerability to global financial volatility.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicator for this sub-tab (calculated indicator)
            subtab_indicators_431_3 = {"Adequacy of International Reserves": "Adequacy of International Reserves"}
            africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
            df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
            
            # Calculate coverage summary
            countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_431_3.values())]['country_or_area'].nunique()
            total_africa_countries = len(africa_countries)
            coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
            
            st.markdown(f"""
            <div class="data-availability-box">
              <div class="left">
                <h4>Data Availability in Africa</h4>
                <p>
                  Data availability determines how confidently we can interpret international reserves adequacy trends across Africa. 
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
                    options=list(subtab_indicators_431_3.keys()),
                    key="ind_4_3_1_3_gap_indicator_select"
                )
                uv.render_data_availability_heatmap(
                    df=df_africa,
                    indicator_label=subtab_indicators_431_3[selected_gap_indicator],
                    title=f"Data Availability for {selected_gap_indicator} (Africa)",
                    container_key="ind_4_3_1_3_gap"
                )

# ========================================
# SUB-TOPIC 4.3.2 – Financial Intermediation
# ========================================
with tab_subtopic_2:
    # Create sub-tabs for the two indicators under 4.3.2
    subtab_432_1, subtab_432_2 = st.tabs([
        "4.3.2.1 – Banking Sector Development Index",
        "4.3.2.2 – Private Sector Credit to GDP"
    ])
    
    # ========================================
    # SUB-TAB 1: Indicator 4.3.2.1 - Banking Sector Development Index
    # ========================================
    with subtab_432_1:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class='indicator-card'>
                <h4>
                    Indicator 4.3.2.1: Banking Sector Development Index
                    <button type="button" class="info-icon-btn" data-tooltip="Composite index combining capital adequacy (40%), liquidity (30%), and credit depth (30%) to measure banking sector strength. Higher values indicate more resilient and efficient banking systems." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> How strong, stable, and effective are domestic banking systems in mobilizing and allocating capital?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # B. Local Filter Row
            # Calculate Banking Sector Development Index
            # Debug: Check what indicators are available
            required_indicators = [
                'Bank capital to assets ratio (%)',
                'Bank liquid reserves to bank assets ratio (%)',
                'Domestic credit provided by financial sector (% of GDP)'
            ]
            
            # Check if required indicators exist in data
            available_indicators = df_display['indicator_label'].unique() if 'indicator_label' in df_display.columns else []
            matching_indicators = [ind for ind in required_indicators if ind in available_indicators]
            
            # Debug: Check for similar indicator names (case-insensitive, partial match)
            similar_indicators = {}
            for req_ind in required_indicators:
                # Check for exact match
                if req_ind in available_indicators:
                    similar_indicators[req_ind] = req_ind
                else:
                    # Check for partial matches (case-insensitive)
                    req_lower = req_ind.lower()
                    matches = [ind for ind in available_indicators if req_lower in str(ind).lower() or str(ind).lower() in req_lower]
                    if matches:
                        similar_indicators[req_ind] = matches[0]
            
            # Calculate Banking Sector Development Index
            df_bsdi = cim.calculate_banking_sector_development_index(df_display)
            if not df_bsdi.empty:
                df_bsdi = df_bsdi.rename(columns={'Banking Sector Development Index': 'value'})
                df_bsdi['indicator_label'] = 'Banking Sector Development Index'
            else:
                # Debug: Show what's missing
                if len(matching_indicators) < len(required_indicators):
                    missing = [ind for ind in required_indicators if ind not in matching_indicators]
                    warning_msg = f"⚠️ Banking Sector Development Index cannot be calculated. Missing indicators: {', '.join(missing)}. Found {len(matching_indicators)}/{len(required_indicators)} required indicators."
                    
                    # Add similar indicator suggestions if found
                    if similar_indicators:
                        suggestions = [f"{req} → {sim}" for req, sim in similar_indicators.items() if req not in matching_indicators]
                        if suggestions:
                            warning_msg += f"\n\nSimilar indicators found: {', '.join(suggestions)}"
                    
                    # Check if indicators exist but no overlapping country-years
                    if len(matching_indicators) == len(required_indicators):
                        # All indicators exist, but maybe no overlapping data
                        st.info("ℹ️ All required indicators found, but no country-year combinations have all three indicators available. The index requires all three components to be present for the same country and year.")
                    else:
                        st.warning(warning_msg)
            
            # Get filter options
            africa_ref_data_4321 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
            africa_countries_4321 = sorted(africa_ref_data_4321['Country or Area'].unique()) if not africa_ref_data_4321.empty else []
            available_years_4321 = sorted(df_bsdi['year'].dropna().unique()) if not df_bsdi.empty else []
            available_regions_4321 = sorted(africa_ref_data_4321['Intermediate Region Name'].dropna().unique()) if not africa_ref_data_4321.empty else []
            
            # Filter row
            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 0.7])
            
            with filter_col1:
                selected_year_4321 = st.selectbox(
                    "Select Year(s)",
                    options=["All Years"] + available_years_4321,
                    index=0,
                    key="ind_4_3_2_1_year_filter"
                )
            
            with filter_col2:
                selected_countries_4321 = st.multiselect(
                    "Select Country",
                    options=africa_countries_4321,
                    default=[],
                    key="ind_4_3_2_1_country_filter"
                )
            
            with filter_col3:
                selected_regions_4321 = st.multiselect(
                    "Select Region",
                    options=available_regions_4321,
                    default=[],
                    key="ind_4_3_2_1_region_filter"
                )
            
            with filter_col4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_3_2_1_reset", use_container_width=True):
                    if 'ind_4_3_2_1_year_filter' in st.session_state:
                        del st.session_state.ind_4_3_2_1_year_filter
                    if 'ind_4_3_2_1_country_filter' in st.session_state:
                        del st.session_state.ind_4_3_2_1_country_filter
                    if 'ind_4_3_2_1_region_filter' in st.session_state:
                        del st.session_state.ind_4_3_2_1_region_filter
                    st.rerun()
            
            # Prepare filtered data
            filtered_bsdi = df_bsdi.copy()
            if selected_year_4321 != "All Years":
                filtered_bsdi = filtered_bsdi[filtered_bsdi['year'] == selected_year_4321]
            if selected_countries_4321:
                filtered_bsdi = filtered_bsdi[filtered_bsdi['country_or_area'].isin(selected_countries_4321)]
            if selected_regions_4321:
                region_countries_4321 = africa_ref_data_4321[
                    africa_ref_data_4321['Intermediate Region Name'].isin(selected_regions_4321)
                ]['Country or Area'].unique()
                filtered_bsdi = filtered_bsdi[filtered_bsdi['country_or_area'].isin(region_countries_4321)]
            
            # C. Visualization Panel with Multi-View Tabs
            tab_graph_4321, tab_map_4321, tab_data_4321 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_4321:
                # Add "How to Read This Graph" hover button
                st.markdown("""
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <button type="button" class="how-to-read-btn" data-tooltip="Each line shows the evolution of a country's banking sector strength — combining capital adequacy, liquidity, and credit depth into a single index. A higher index means more resilient and efficient banking systems. Reference bands indicate development tiers: below 0.4 (weak), 0.4-0.69 (moderate), and above 0.7 (high development)." style="background: none; border: none; cursor: help; font-size: 0.9em; color: #666; padding: 0.25rem 0.5rem; margin-left: auto;">
                        How to Read This Graph <span style="font-size: 0.8em;">ℹ️</span>
                    </button>
                </div>
                """, unsafe_allow_html=True)
                
                # Render chart
                if not filtered_bsdi.empty:
                    import plotly.graph_objects as go
                    import numpy as np
                    
                    fig = go.Figure()
                    
                    # Add reference bands (shaded areas) for development tiers
                    # Weak Development (0-0.4): Red/Orange
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=0, x1=1, y1=0.4,
                        fillcolor="#F26C2B",
                        opacity=0.2,
                        layer="below",
                        line_width=0,
                    )
                    # Moderate Development (0.4-0.7): Yellow
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=0.4, x1=1, y1=0.7,
                        fillcolor="#FFD34E",
                        opacity=0.2,
                        layer="below",
                        line_width=0,
                    )
                    # High Development (0.7-1.0): Blue
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=0.7, x1=1, y1=1.0,
                        fillcolor="#0072BC",
                        opacity=0.2,
                        layer="below",
                        line_width=0,
                    )
                    
                    # Add reference lines at boundaries
                    fig.add_hline(
                        y=0.4,
                        line_dash="dash",
                        line_color="#F26C2B",
                        line_width=1,
                        opacity=0.5,
                        annotation_text="0.4",
                        annotation_position="right",
                        annotation_font_size=9
                    )
                    fig.add_hline(
                        y=0.7,
                        line_dash="dash",
                        line_color="#0072BC",
                        line_width=1,
                        opacity=0.5,
                        annotation_text="0.7",
                        annotation_position="right",
                        annotation_font_size=9
                    )
                    
                    # Add zone annotations with explanations
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.02, y=0.2,
                        text="Weak Development<br>(0-0.4)<br>Fragile systems",
                        showarrow=False,
                        font=dict(size=9, color="#F26C2B"),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#F26C2B",
                        borderwidth=1,
                        align="left"
                    )
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.02, y=0.55,
                        text="Moderate Development<br>(0.4-0.7)<br>Moderate strength",
                        showarrow=False,
                        font=dict(size=9, color="#FFD34E"),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#FFD34E",
                        borderwidth=1,
                        align="left"
                    )
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.02, y=0.85,
                        text="High Development<br>(0.7-1.0)<br>Strong systems",
                        showarrow=False,
                        font=dict(size=9, color="#0072BC"),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#0072BC",
                        borderwidth=1,
                        align="left"
                    )
                    
                    # Get selected countries
                    selected_countries_list_4321 = selected_countries_4321 if selected_countries_4321 else []
                    
                    # Get component data for tooltips
                    capital_data = df_display[df_display['indicator_label'] == 'Bank capital to assets ratio (%)'].copy()
                    liquidity_data = df_display[df_display['indicator_label'] == 'Bank liquid reserves to bank assets ratio (%)'].copy()
                    credit_data = df_display[df_display['indicator_label'] == 'Domestic credit provided by financial sector (% of GDP)'].copy()
                    
                    # Add country lines
                    countries_list_4321 = sorted(filtered_bsdi['country_or_area'].dropna().unique())
                    for country in countries_list_4321:
                        country_data = filtered_bsdi[filtered_bsdi['country_or_area'] == country].sort_values('year')
                        country_data = country_data.dropna(subset=['value'])
                        
                        if not country_data.empty:
                            # Color encoding based on latest value tier
                            latest_value = country_data['value'].iloc[-1]
                            if latest_value >= 0.7:
                                line_color = '#0072BC'  # High development
                            elif latest_value >= 0.4:
                                line_color = '#FFD34E'  # Moderate development
                            else:
                                line_color = '#F26C2B'  # Weak development
                            
                            # Highlight selected countries
                            if country in selected_countries_list_4321:
                                line_color = '#003366'  # Deep blue for selected
                                line_width = 3
                            else:
                                line_width = 2
                            
                            # Merge with component data for tooltips
                            # Rename columns before merging to avoid suffix conflicts
                            capital_data_renamed = capital_data[['country_or_area', 'year', 'value']].rename(columns={'value': 'value_capital'})
                            liquidity_data_renamed = liquidity_data[['country_or_area', 'year', 'value']].rename(columns={'value': 'value_liquidity'})
                            credit_data_renamed = credit_data[['country_or_area', 'year', 'value']].rename(columns={'value': 'value_credit'})
                            
                            country_data_merged = country_data.merge(
                                capital_data_renamed,
                                on=['country_or_area', 'year'],
                                how='left'
                            )
                            country_data_merged = country_data_merged.merge(
                                liquidity_data_renamed,
                                on=['country_or_area', 'year'],
                                how='left'
                            )
                            country_data_merged = country_data_merged.merge(
                                credit_data_renamed,
                                on=['country_or_area', 'year'],
                                how='left'
                            )
                            
                            hovertemplate = (
                                f"<b>{country}</b><br>" +
                                "Year: %{x}<br>" +
                                "BSDI Value: %{y:.3f}<br>" +
                                "Capital Ratio: %{customdata[0]:.2f}%<br>" +
                                "Liquidity Ratio: %{customdata[1]:.2f}%<br>" +
                                "Credit Ratio: %{customdata[2]:.2f}%<br>" +
                                "<extra></extra>"
                            )
                            
                            fig.add_trace(go.Scatter(
                                x=country_data_merged['year'],
                                y=country_data_merged['value'],
                                mode='lines+markers',
                                name=country,
                                line=dict(color=line_color, width=line_width),
                                marker=dict(color=line_color, size=6 if country in selected_countries_list_4321 else 4),
                                hovertemplate=hovertemplate,
                                customdata=np.column_stack([
                                    country_data_merged['value_capital'].fillna(0),
                                    country_data_merged['value_liquidity'].fillna(0),
                                    country_data_merged['value_credit'].fillna(0)
                                ]),
                                showlegend=True
                            ))
                    
                    fig.update_layout(
                        height=500,
                        xaxis_title="Year",
                        yaxis_title="Banking Sector Development Index (0-1)",
                        hovermode='closest',
                        yaxis=dict(range=[0, 1]),
                        legend=dict(
                            orientation="v",
                            yanchor="top",
                            y=1,
                            xanchor="left",
                            x=1.02,
                            font=dict(size=10),
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="rgba(0,0,0,0.2)",
                            borderwidth=1
                        ),
                        margin=dict(l=50, r=180, t=20, b=50)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_map_4321:
                # Map View
                if not filtered_bsdi.empty:
                    map_data_4321 = filtered_bsdi.copy()
                    
                    # Use the latest year if multiple years, or selected year
                    if selected_year_4321 != "All Years":
                        map_data_4321 = map_data_4321[map_data_4321['year'] == selected_year_4321]
                    else:
                        map_data_4321 = map_data_4321.loc[map_data_4321.groupby('country_or_area')['year'].idxmax()]
                    
                    map_data_4321['value'] = pd.to_numeric(map_data_4321['value'], errors='coerce')
                    map_data_4321 = map_data_4321.dropna(subset=['value'])
                    
                    if not map_data_4321.empty:
                        africa_ref_4321 = ref_data[ref_data['Region Name'] == 'Africa'].copy()
                        if not africa_ref_4321.empty and 'Country or Area' in africa_ref_4321.columns:
                            map_data_merged_4321 = map_data_4321.merge(
                                africa_ref_4321[['Country or Area', 'iso3']],
                                left_on='country_or_area',
                                right_on='Country or Area',
                                how='inner'
                            )
                            
                            if not map_data_merged_4321.empty:
                                iso_col_4321 = 'iso3_y' if 'iso3_y' in map_data_merged_4321.columns else ('iso3_x' if 'iso3_x' in map_data_merged_4321.columns else 'iso3')
                                if iso_col_4321 != 'iso3' and iso_col_4321 in map_data_merged_4321.columns:
                                    map_data_merged_4321['iso3'] = map_data_merged_4321[iso_col_4321]
                                
                                fig_map_4321 = go.Figure(data=go.Choropleth(
                                    locations=map_data_merged_4321['iso3'],
                                    z=map_data_merged_4321['value'],
                                    locationmode='ISO-3',
                                    colorscale='Blues',
                                    showscale=True,
                                    text=map_data_merged_4321.apply(
                                        lambda row: f"{row['country_or_area']}<br>BSDI: {row['value']:.3f}<br>Year: {row['year']}",
                                        axis=1
                                    ),
                                    hovertemplate='%{text}<extra></extra>',
                                    colorbar=dict(title="Banking Sector Development Index")
                                ))
                                
                                fig_map_4321.update_layout(
                                    height=500,
                                    geo=dict(
                                        bgcolor='rgba(0,0,0,0)',
                                        lakecolor='rgba(0,0,0,0)',
                                        landcolor='rgba(217, 217, 217, 1)',
                                        subunitcolor='white',
                                        scope='africa',
                                        showframe=False,
                                        showcoastlines=True,
                                        projection_type='natural earth'
                                    ),
                                    margin={"r":0,"t":0,"l":0,"b":0}
                                )
                                
                                st.plotly_chart(fig_map_4321, use_container_width=True)
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_data_4321:
                # Data Table
                if not filtered_bsdi.empty:
                    display_df_4321 = filtered_bsdi[['country_or_area', 'year', 'value']].copy()
                    display_df_4321 = display_df_4321.rename(columns={'value': 'Banking Sector Development Index'})
                    st.dataframe(display_df_4321, use_container_width=True)
                    
                    csv_4321 = display_df_4321.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_4321,
                        file_name=f"indicator_4_3_2_1_{selected_year_4321 if selected_year_4321 != 'All Years' else 'all_years'}.csv",
                        mime="text/csv",
                        key="ind_4_3_2_1_download_csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
                    The Banking Sector Development Index (BSDI) is a composite index combining three key banking indicators:
                    - **Bank capital to assets ratio (40%)**: Measures capital adequacy
                    - **Bank liquid reserves to bank assets ratio (30%)**: Measures liquidity
                    - **Domestic credit provided by financial sector (% of GDP) (30%)**: Measures credit depth
                    
                    **Formula:** BSDI = 0.4 × Capital Ratio + 0.3 × Liquidity Ratio + 0.3 × Credit Ratio
                    
                    **Source:** World Bank - Calculated from component indicators
                    """)
                with tab_rel:
                    st.markdown("""
                    - **Efficiency**: Stable or improving BSDI values show well-capitalized banks using assets efficiently.
                    - **Effectiveness**: Growth in BSDI signals banks effectively channel savings into productive lending, supporting inclusive development.
                    """)
                with tab_proxy:
                    st.markdown("""
                    Calculated composite indicator. See methodology above.
                    """)
                with tab_pillar:
                    st.markdown("""
                    Within Theme 4, this indicator captures how domestic banking systems drive financial resilience. Strong, well-capitalized banks reduce reliance on external finance and improve resource allocation efficiency.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
                **Efficiency:** Stable or improving BSDI values show well-capitalized banks using assets efficiently. Countries with efficient banking systems can mobilize savings and allocate credit effectively without excessive risk.
                
                **Effectiveness:** Growth in BSDI signals banks effectively channel savings into productive lending, supporting inclusive development. Effective banking systems support real-sector activity and reduce dependence on external financing.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicator for this sub-tab (calculated indicator)
            subtab_indicators_432_1 = {"Banking Sector Development Index": "Banking Sector Development Index"}
            africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
            df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
            
            # Calculate coverage summary
            countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_432_1.values())]['country_or_area'].nunique()
            total_africa_countries = len(africa_countries)
            coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
            
            st.markdown(f"""
            <div class="data-availability-box">
              <div class="left">
                <h4>Data Availability in Africa</h4>
                <p>
                  Data availability determines how confidently we can interpret banking sector development trends across Africa. 
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
                    options=list(subtab_indicators_432_1.keys()),
                    key="ind_4_3_2_1_gap_indicator_select"
                )
                uv.render_data_availability_heatmap(
                    df=df_africa,
                    indicator_label=subtab_indicators_432_1[selected_gap_indicator],
                    title=f"Data Availability for {selected_gap_indicator} (Africa)",
                    container_key="ind_4_3_2_1_gap"
                )
    
    # ========================================
    # SUB-TAB 2: Indicator 4.3.2.2 - Private Sector Credit to GDP
    # ========================================
    with subtab_432_2:
        with st.container():
            # A. Indicator Header
            st.markdown("""
            <div class='indicator-card'>
                <h4>
                    Indicator 4.3.2.2: Private Sector Credit to GDP
                    <button type="button" class="info-icon-btn" data-tooltip="Measures the share of total GDP that flows through the domestic financial system. A higher value means the country's financial sector plays a larger role in funding businesses and households." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
                </h4>
                <p style="color: #555; line-height: 1.5; margin-bottom: 0.75rem;">
                    <strong>Analytical Focus Question:</strong> How much of a country's total economic output is financed through its domestic financial system — reflecting the role of banks and other financial institutions in supporting real-sector activity?
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # B. Local Filter Row
            # Load Domestic Credit to GDP data
            credit_indicator_label = "Domestic credit provided by financial sector (% of GDP)"
            df_credit = df_display[df_display['indicator_label'] == credit_indicator_label].copy()
            
            # Get filter options
            africa_ref_data_4322 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
            africa_countries_4322 = sorted(africa_ref_data_4322['Country or Area'].unique()) if not africa_ref_data_4322.empty else []
            available_years_4322 = sorted(df_credit['year'].dropna().unique()) if not df_credit.empty else []
            available_regions_4322 = sorted(africa_ref_data_4322['Intermediate Region Name'].dropna().unique()) if not africa_ref_data_4322.empty else []
            
            # Filter row
            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 0.7])
            
            with filter_col1:
                selected_year_4322 = st.selectbox(
                    "Select Year(s)",
                    options=["All Years"] + available_years_4322,
                    index=0,
                    key="ind_4_3_2_2_year_filter"
                )
            
            with filter_col2:
                selected_countries_4322 = st.multiselect(
                    "Select Country",
                    options=africa_countries_4322,
                    default=[],
                    key="ind_4_3_2_2_country_filter"
                )
            
            with filter_col3:
                selected_regions_4322 = st.multiselect(
                    "Select Region",
                    options=available_regions_4322,
                    default=[],
                    key="ind_4_3_2_2_region_filter"
                )
            
            with filter_col4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset", key="ind_4_3_2_2_reset", use_container_width=True):
                    if 'ind_4_3_2_2_year_filter' in st.session_state:
                        del st.session_state.ind_4_3_2_2_year_filter
                    if 'ind_4_3_2_2_country_filter' in st.session_state:
                        del st.session_state.ind_4_3_2_2_country_filter
                    if 'ind_4_3_2_2_region_filter' in st.session_state:
                        del st.session_state.ind_4_3_2_2_region_filter
                    st.rerun()
            
            # Prepare filtered data
            filtered_credit = df_credit.copy()
            if selected_year_4322 != "All Years":
                filtered_credit = filtered_credit[filtered_credit['year'] == selected_year_4322]
            if selected_countries_4322:
                filtered_credit = filtered_credit[filtered_credit['country_or_area'].isin(selected_countries_4322)]
            if selected_regions_4322:
                region_countries_4322 = africa_ref_data_4322[
                    africa_ref_data_4322['Intermediate Region Name'].isin(selected_regions_4322)
                ]['Country or Area'].unique()
                filtered_credit = filtered_credit[filtered_credit['country_or_area'].isin(region_countries_4322)]
            
            # C. Visualization Panel with Multi-View Tabs
            tab_graph_4322, tab_map_4322, tab_data_4322 = st.tabs(["Graph View", "Map View", "Data Table"])
            
            with tab_graph_4322:
                # Add "How to Read This Graph" hover button
                st.markdown("""
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <button type="button" class="how-to-read-btn" data-tooltip="Each line shows the share of total GDP that flows through the domestic financial system. A higher value means the country's financial sector plays a larger role in funding businesses and households. Reference bands indicate depth tiers: below 40% (shallow), 40-80% (moderate), and above 80% (deep financial systems)." style="background: none; border: none; cursor: help; font-size: 0.9em; color: #666; padding: 0.25rem 0.5rem; margin-left: auto;">
                        How to Read This Graph <span style="font-size: 0.8em;">ℹ️</span>
                    </button>
                </div>
                """, unsafe_allow_html=True)
                
                # Benchmark toggle
                benchmark_toggle_col1, benchmark_toggle_col2 = st.columns([1, 4])
                with benchmark_toggle_col1:
                    show_benchmark = st.checkbox(
                        "Show Sub-Regional Averages",
                        value=False,
                        key="ind_4_3_2_2_benchmark_toggle"
                    )
                
                # Render chart
                if not filtered_credit.empty:
                    import plotly.graph_objects as go
                    import numpy as np
                    
                    fig = go.Figure()
                    
                    # Add reference bands (shaded areas) for financial depth tiers
                    # Shallow Financial Systems (0-40%): Red/Orange
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=0, x1=1, y1=40,
                        fillcolor="#F26C2B",
                        opacity=0.2,
                        layer="below",
                        line_width=0,
                    )
                    # Moderate Depth (40-80%): Yellow
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=40, x1=1, y1=80,
                        fillcolor="#FFD34E",
                        opacity=0.2,
                        layer="below",
                        line_width=0,
                    )
                    # Deep Financial Systems (80%+): Blue
                    # Determine max value for y-axis
                    y_max = max(filtered_credit['value'].max() * 1.1, 200) if not filtered_credit.empty else 200
                    fig.add_shape(
                        type="rect",
                        xref="paper", yref="y",
                        x0=0, y0=80, x1=1, y1=y_max,
                        fillcolor="#0072BC",
                        opacity=0.2,
                        layer="below",
                        line_width=0,
                    )
                    
                    # Add reference lines at boundaries
                    fig.add_hline(
                        y=40,
                        line_dash="dash",
                        line_color="#F26C2B",
                        line_width=1,
                        opacity=0.5,
                        annotation_text="40%",
                        annotation_position="right",
                        annotation_font_size=9
                    )
                    fig.add_hline(
                        y=80,
                        line_dash="dash",
                        line_color="#0072BC",
                        line_width=1,
                        opacity=0.5,
                        annotation_text="80%",
                        annotation_position="right",
                        annotation_font_size=9
                    )
                    
                    # Add zone annotations with explanations
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.02, y=20,
                        text="Shallow Systems<br>(0-40%)<br>Limited depth",
                        showarrow=False,
                        font=dict(size=9, color="#F26C2B"),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#F26C2B",
                        borderwidth=1,
                        align="left"
                    )
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.02, y=60,
                        text="Moderate Depth<br>(40-80%)<br>Moderate role",
                        showarrow=False,
                        font=dict(size=9, color="#FFD34E"),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#FFD34E",
                        borderwidth=1,
                        align="left"
                    )
                    fig.add_annotation(
                        xref="paper", yref="y",
                        x=0.02, y=min(140, (80 + y_max) / 2),
                        text="Deep Systems<br>(80%+)<br>Strong role",
                        showarrow=False,
                        font=dict(size=9, color="#0072BC"),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#0072BC",
                        borderwidth=1,
                        align="left"
                    )
                    
                    # Get selected countries
                    selected_countries_list_4322 = selected_countries_4322 if selected_countries_4322 else []
                    
                    # Calculate change since 2000 for tooltips
                    filtered_credit_sorted = filtered_credit.sort_values(['country_or_area', 'year'])
                    baseline_2000 = filtered_credit_sorted[filtered_credit_sorted['year'] == 2000].set_index('country_or_area')['value']
                    filtered_credit_sorted['change_since_2000'] = filtered_credit_sorted.apply(
                        lambda row: row['value'] - baseline_2000.get(row['country_or_area'], np.nan) if row['country_or_area'] in baseline_2000.index else np.nan,
                        axis=1
                    )
                    
                    # Add country lines only if sub-regional averages are NOT shown
                    if not show_benchmark:
                        countries_list_4322 = sorted(filtered_credit_sorted['country_or_area'].dropna().unique())
                        for country in countries_list_4322:
                            country_data = filtered_credit_sorted[filtered_credit_sorted['country_or_area'] == country].sort_values('year')
                            country_data = country_data.dropna(subset=['value'])
                            
                            if not country_data.empty:
                                # Color encoding based on latest value tier
                                latest_value = country_data['value'].iloc[-1]
                                if latest_value > 80:
                                    line_color = '#0072BC'  # Deep financial systems
                                elif latest_value >= 40:
                                    line_color = '#FFD34E'  # Moderate depth
                                else:
                                    line_color = '#F26C2B'  # Shallow depth
                                
                                # Highlight selected countries
                                if country in selected_countries_list_4322:
                                    line_color = '#003366'  # Deep blue for selected
                                    line_width = 3
                                else:
                                    line_width = 2
                                
                                # Create hover text with change since 2000
                                hover_texts = []
                                for idx, row in country_data.iterrows():
                                    change = row.get('change_since_2000', np.nan)
                                    if not pd.isna(change):
                                        change_str = f"{change:+.1f}%"
                                    else:
                                        change_str = "N/A"
                                    
                                    hover_text = (
                                        f"<b>{country}</b><br>" +
                                        f"Year: {int(row['year'])}<br>" +
                                        f"Domestic Credit: {row['value']:.2f}% of GDP<br>" +
                                        f"Change since 2000: {change_str}<br>" +
                                        "<extra></extra>"
                                    )
                                    hover_texts.append(hover_text)
                                
                                fig.add_trace(go.Scatter(
                                    x=country_data['year'],
                                    y=country_data['value'],
                                    mode='lines+markers',
                                    name=country,
                                    line=dict(color=line_color, width=line_width),
                                    marker=dict(color=line_color, size=6 if country in selected_countries_list_4322 else 4),
                                    hovertemplate='%{text}',
                                    text=hover_texts,
                                    showlegend=True
                                ))
                    
                    # Add sub-regional average lines if requested
                    if show_benchmark:
                        # Merge with reference data to get Intermediate Region Name
                        filtered_credit_with_regions = filtered_credit_sorted.merge(
                            africa_ref_data_4322[['Country or Area', 'Intermediate Region Name']],
                            left_on='country_or_area',
                            right_on='Country or Area',
                            how='left'
                        )
                        
                        # Get unique sub-regions
                        sub_regions = sorted(filtered_credit_with_regions['Intermediate Region Name'].dropna().unique())
                        
                        # Color palette for sub-regions
                        sub_region_colors = {
                            'Eastern Africa': '#0072BC',  # Blue
                            'Middle Africa': '#00A1A1',    # Teal
                            'Northern Africa': '#F26C2B',  # Orange
                            'Southern Africa': '#FFD34E',  # Yellow
                            'Western Africa': '#7C4DFF'    # Purple
                        }
                        
                        # Calculate and add average line for each sub-region
                        for sub_region in sub_regions:
                            sub_region_data = filtered_credit_with_regions[
                                filtered_credit_with_regions['Intermediate Region Name'] == sub_region
                            ]
                            
                            if not sub_region_data.empty:
                                # Calculate average for this sub-region
                                sub_region_avg = sub_region_data.groupby('year')['value'].mean().reset_index()
                                sub_region_avg = sub_region_avg.sort_values('year')
                                
                                if not sub_region_avg.empty:
                                    # Get color for this sub-region, default to gray if not in palette
                                    line_color = sub_region_colors.get(sub_region, '#999999')
                                    
                                    fig.add_trace(go.Scatter(
                                        x=sub_region_avg['year'],
                                        y=sub_region_avg['value'],
                                        mode='lines+markers',
                                        name=f'{sub_region} Average',
                                        line=dict(color=line_color, width=3, dash='dash'),
                                        marker=dict(color=line_color, size=6),
                                        hovertemplate=(
                                            f"<b>{sub_region} Average</b><br>" +
                                            "Year: %{x}<br>" +
                                            "Domestic Credit: %{y:.2f}% of GDP<br>" +
                                            "<extra></extra>"
                                        ),
                                        showlegend=True,
                                        legendrank=1  # Ensure regional averages appear first in legend
                                    ))
                    
                    fig.update_layout(
                        height=500,
                        xaxis_title="Year",
                        yaxis_title="Domestic Credit Provided by Financial Sector (% of GDP)",
                        hovermode='closest',
                        yaxis=dict(range=[0, y_max]),  # Use calculated y_max for proper range
                        legend=dict(
                            orientation="v",
                            yanchor="top",
                            y=1,
                            xanchor="left",
                            x=1.02,
                            font=dict(size=10),
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="rgba(0,0,0,0.2)",
                            borderwidth=1
                        ),
                        margin=dict(l=50, r=180, t=20, b=50)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_map_4322:
                # Map View
                if not filtered_credit.empty:
                    map_data_4322 = filtered_credit.copy()
                    
                    # Use the latest year if multiple years, or selected year
                    if selected_year_4322 != "All Years":
                        map_data_4322 = map_data_4322[map_data_4322['year'] == selected_year_4322]
                    else:
                        map_data_4322 = map_data_4322.loc[map_data_4322.groupby('country_or_area')['year'].idxmax()]
                    
                    map_data_4322['value'] = pd.to_numeric(map_data_4322['value'], errors='coerce')
                    map_data_4322 = map_data_4322.dropna(subset=['value'])
                    
                    if not map_data_4322.empty:
                        africa_ref_4322 = ref_data[ref_data['Region Name'] == 'Africa'].copy()
                        if not africa_ref_4322.empty and 'Country or Area' in africa_ref_4322.columns:
                            map_data_merged_4322 = map_data_4322.merge(
                                africa_ref_4322[['Country or Area', 'iso3']],
                                left_on='country_or_area',
                                right_on='Country or Area',
                                how='inner'
                            )
                            
                            if not map_data_merged_4322.empty:
                                iso_col_4322 = 'iso3_y' if 'iso3_y' in map_data_merged_4322.columns else ('iso3_x' if 'iso3_x' in map_data_merged_4322.columns else 'iso3')
                                if iso_col_4322 != 'iso3' and iso_col_4322 in map_data_merged_4322.columns:
                                    map_data_merged_4322['iso3'] = map_data_merged_4322[iso_col_4322]
                                
                                fig_map_4322 = go.Figure(data=go.Choropleth(
                                    locations=map_data_merged_4322['iso3'],
                                    z=map_data_merged_4322['value'],
                                    locationmode='ISO-3',
                                    colorscale='Blues',
                                    showscale=True,
                                    text=map_data_merged_4322.apply(
                                        lambda row: f"{row['country_or_area']}<br>Domestic Credit: {row['value']:.2f}% of GDP<br>Year: {row['year']}",
                                        axis=1
                                    ),
                                    hovertemplate='%{text}<extra></extra>',
                                    colorbar=dict(title="Domestic Credit (% of GDP)")
                                ))
                                
                                fig_map_4322.update_layout(
                                    height=500,
                                    geo=dict(
                                        bgcolor='rgba(0,0,0,0)',
                                        lakecolor='rgba(0,0,0,0)',
                                        landcolor='rgba(217, 217, 217, 1)',
                                        subunitcolor='white',
                                        scope='africa',
                                        showframe=False,
                                        showcoastlines=True,
                                        projection_type='natural earth'
                                    ),
                                    margin={"r":0,"t":0,"l":0,"b":0}
                                )
                                
                                st.plotly_chart(fig_map_4322, use_container_width=True)
                else:
                    st.info("No data available for the selected filters.")
            
            with tab_data_4322:
                # Data Table
                if not filtered_credit.empty:
                    display_df_4322 = filtered_credit[['country_or_area', 'year', 'value']].copy()
                    display_df_4322 = display_df_4322.rename(columns={'value': 'Domestic Credit (% of GDP)'})
                    st.dataframe(display_df_4322, use_container_width=True)
                    
                    csv_4322 = display_df_4322.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_4322,
                        file_name=f"indicator_4_3_2_2_{selected_year_4322 if selected_year_4322 != 'All Years' else 'all_years'}.csv",
                        mime="text/csv",
                        key="ind_4_3_2_2_download_csv"
                    )
                else:
                    st.info("No data available for the selected filters.")
            
            # D. Supporting Information Layers
            with st.expander("Learn more about this indicator", expanded=False):
                tab_def, tab_rel, tab_proxy, tab_pillar = st.tabs(["Definition", "Relevance", "Proxy Justification", "Pillar Connection"])
                with tab_def:
                    st.markdown("""
                    Domestic credit provided by the financial sector includes all credit to various sectors on a gross basis, with the exception of credit to the central government, which is net. The financial sector includes monetary authorities and deposit money banks, as well as other financial corporations where data are available.
                    
                    This indicator is expressed as a percentage of Gross Domestic Product (GDP).
                    
                    **Source:** World Bank - [FS.AST.DOMS.GD.ZS](https://data.worldbank.org/indicator/FS.AST.DOMS.GD.ZS)
                    """)
                with tab_rel:
                    st.markdown("""
                    - **Efficiency**: Measures how effectively financial systems mobilize and allocate funds to productive sectors.
                    - **Effectiveness**: Reflects how financial intermediation supports overall economic activity and private-sector investment.
                    """)
                with tab_proxy:
                    st.markdown("""
                    Direct indicator from World Bank. No proxy needed.
                    """)
                with tab_pillar:
                    st.markdown("""
                    Under Theme 4, this indicator tracks how much of national income is intermediated domestically. It highlights whether growth is financed by internal banking systems or reliant on external capital.
                    """)
            
            with st.expander("Analytical Lens (Efficiency and Effectiveness)", expanded=False):
                st.markdown("""
                **Efficiency:** A growing ratio shows stronger financial intermediation — banks and institutions efficiently converting savings into loans. Countries with efficient financial systems can channel domestic savings into productive investments.
                
                **Effectiveness:** Deepening credit-to-GDP indicates broader access to finance and more inclusive economic growth. Effective financial systems support real-sector activity and reduce dependence on external financing.
                """)
            
            # Data Availability Section for this indicator
            st.markdown("""
            <div style="border-top: 2px solid #F26C2B; margin: 1.5rem 0; clear: both;"></div>
            """, unsafe_allow_html=True)
            
            # Get indicator for this sub-tab
            subtab_indicators_432_2 = {"Private Sector Credit to GDP": "Domestic credit provided by financial sector (% of GDP)"}
            africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
            df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
            
            # Calculate coverage summary
            countries_with_data = df_africa[df_africa['indicator_label'].isin(subtab_indicators_432_2.values())]['country_or_area'].nunique()
            total_africa_countries = len(africa_countries)
            coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0
            
            st.markdown(f"""
            <div class="data-availability-box">
              <div class="left">
                <h4>Data Availability in Africa</h4>
                <p>
                  Data availability determines how confidently we can interpret private sector credit trends across Africa. 
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
                    options=list(subtab_indicators_432_2.keys()),
                    key="ind_4_3_2_2_gap_indicator_select"
                )
                uv.render_data_availability_heatmap(
                    df=df_africa,
                    indicator_label=subtab_indicators_432_2[selected_gap_indicator],
                    title=f"Data Availability for {selected_gap_indicator} (Africa)",
                    container_key="ind_4_3_2_2_gap"
                )

# ========================================
# SUB-TOPIC 4.3.3 – Investment from Institutional Investors
# ========================================
with tab_subtopic_3:
    # For 4.3.3, we have only one indicator, so we display it directly
    # No need for nested tabs since there's only one sub-indicator
    
    # Special textual layout for 4.3.3.1
    st.markdown("""
    <div class='indicator-card'>
        <h4>
            4.3.3.1 – Pension Funds and Sovereign Wealth Funds Investments
            <button type="button" class="info-icon-btn" data-tooltip="Analyzes the role of institutional investors, particularly pension funds, in mobilizing long-term capital in Africa. Focuses on asset allocation patterns, domestic vs foreign investment, and regulatory trends." style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
        </h4>
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
            width: 300px;
            font-size: 0.9em;
            z-index: 1000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            margin-bottom: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Intro narrative paragraph
    st.markdown('''
    **Institutional investors—especially public pension funds—are playing an increasingly important role in mobilizing long-term capital in Africa. Approximately 92% of pension fund assets on the continent are concentrated in South Africa, Nigeria, Kenya, Namibia, and Botswana<sup>1</sup>. Most African pension funds invest primarily in domestic capital markets, often due to regulatory requirements and limited viable foreign opportunities.**
    ''', unsafe_allow_html=True)
    
    # Key Trends section
    st.markdown("#### Key Trends")
    st.markdown("""
    - Asset allocation remains conservative, with a dominant focus on government bonds and local equities.
    - A gradual shift is underway toward real estate, infrastructure, and private equity, although allocations to these alternative assets are still low.
    - Regulatory reforms in countries like Zambia and Nigeria are enabling co-investment in infrastructure and private equity.
    """)
    
    # Country-by-country analysis in expanders
    try:
        df_pension = pd.read_csv('data/Pension_Fund_Asset_Allocation_by_Country.csv')
        country_col = 'Country or Area' if 'Country or Area' in df_pension.columns else 'Country'
        df_pension['Country_Flag'] = df_pension[country_col].map(country_flags) + " " + df_pension[country_col]
    except Exception as e:
        df_pension = pd.DataFrame()
        st.warning(f"Could not load pension fund data: {e}")
    
    for country, flag in country_flags.items():
        with st.expander(f"{flag} {country}"):
            if country == "South Africa":
                st.markdown('''
                <span style="color:#072D92;font-weight:600;">Fund & Size:</span> GEPF (Government Employees Pension Fund) is Africa's largest pension fund, with ~R2.34 trillion under management (as of Mar 2024). There is no formal SWF yet.<br>
                <span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> ~86% of GEPF's portfolio is in domestic SA markets. (PIC's asset allocation: 51% domestic equity, 30% domestic bonds, 4% domestic property, 1% cash – total 86% domestic. Only ~8% in international securities, plus ~4% in other African assets.)<br>
                <span style="color:#072D92;font-weight:600;">Asset Classes:</span> Largest holdings are JSE-listed equities and RSA government bonds. Alternatives (infrastructure, private equity) are still small (~2%). PIC (the fund manager) is expanding in local infrastructure projects (e.g. energy, transport) per its developmental mandate.<br>
                <span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> Recent reforms (like the "two-pot" retirement withdrawal system) are forcing liquidity changes, but GEPF continues to follow conservative targets (e.g. rising fixed-income allocation). The fund is also gradually shifting some equity/property into infrastructure and stable-income assets. Overall, domestic exposure remains very high, driven by regulation and mandate.<br>
                <em>South Africa's Government Employees Pension Fund (GEPF) manages approximately R2.34 trillion in assets, of which about 86% is invested domestically, including 51% in equities and 30% in government bonds.<sup>2</sup></em>
                ''', unsafe_allow_html=True)
            elif country == "Nigeria":
                st.markdown('''
                <span style="color:#072D92;font-weight:600;">Fund & Size:</span> Nigeria's CPS system (contributory pensions) had ~₦17.35 trillion (≈$40B) in assets by Q3 2023. Nigeria's Sovereign Wealth Fund (NSIA) is separate (not shown here).<br>
                <span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> Nigerian pensions are overwhelmingly domestic. ~65.2% of assets are in Federal Government of Nigeria (FGN) securities, ~10.7% in domestic corporate bonds, ~9.2% in Nigerian money-market placements. Domestic equities account for ~7.99% (while foreign equities are only 0.89%). Foreign money-market holdings are ~0.29%. In total, well over 98% is local.<br>
                <span style="color:#072D92;font-weight:600;">Asset Classes:</span> Pensions hold mostly fixed income. FGN bonds/T-bills dominate (65%). Corporate debt is ~11% and local bank placements ~9%. Local stocks are ~8%. Real estate investments are ~1.25%, private equity ~0.37%, and the fledgling Pension Infrastructure Fund ~0.75%. Foreign exposure (global equities/currency positions) is negligible.<br>
                <span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> Regulators have been pushing for more long-term investment: allocations into sukuk (Islamic bonds), green bonds, and infrastructure debt have risen. There is a growing Pension Infrastructure Debt Fund. Still, with limited capital markets depth, funds mainly recycle into government debt. NSIA's SWF also largely focuses on domestic infrastructure but does invest some assets abroad.<br>
                <em>Nigeria's pension system, regulated by PenCom, holds over ₦17.35 trillion in assets, with more than 98% allocated to domestic instruments, including federal government securities, corporate bonds, and Nigerian equities.<sup>3</sup></em>
                ''', unsafe_allow_html=True)
            elif country == "Kenya":
                st.markdown('''
                <span style="color:#072D92;font-weight:600;">Fund & Size:</span> The National Social Security Fund (NSSF) is Kenya's main pension scheme (other retirement schemes are smaller). NSSF AUM rose to ~Ksh 402.2 billion by June 2024. Kenya has no centralized SWF (though infrastructure bonds exist).<br>
                <span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> NSSF is essentially 100% invested in Kenya. (Eurobond / external debt exposure is tiny or zero.)<br>
                <span style="color:#072D92;font-weight:600;">Asset Classes:</span> As of mid-2024, government securities dominated: ~67–72% in Kenyan government bonds. Equities (quoted Kenyan stocks) were ~14–17%. Property/real estate investments are ~10%. Cash and deposits ~3%. (By law, corporate bonds and offshore holdings are minimal: e.g. corporate bonds ~0% and foreign bonds ~2% per latest data.) Overall, domestic debt and markets account for virtually all assets.<br>
                <span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> The 2013 Pension Act (NSSF overhaul) and subsequent contribution hikes (to 12%) have swelled Kenya's pension pool. RBA reports stress building local capital markets; NSSF has begun placing funds into infrastructure projects (e.g. toll-road and housing bonds). There are plans to introduce a new multi-tier pension system, which may affect allocations. For now, the fund's asset mix remains conservative and local.<br>
                <em>Kenya's NSSF holds over Ksh 402.2 billion, with a portfolio heavily weighted toward domestic government bonds (~70%), local equities (~15%), and real estate (~10%).<sup>4</sup></em>
                ''', unsafe_allow_html=True)
            elif country == "Rwanda":
                st.markdown('''
                <span style="color:#072D92;font-weight:600;">Fund & Size:</span> Rwanda's pension scheme is managed by RSSB. Assets reached about Rwf2.14 trillion (~$2 billion) by end-2023. Rwanda has no separate SWF (RSSB also runs health/insurance funds).<br>
                <span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> RSSB is entirely focused on Rwanda's economy. It invests almost all funds domestically (no significant offshore portfolio).<br>
                <span style="color:#072D92;font-weight:600;">Asset Classes:</span> Official summaries highlight real estate and equity: RSSB holds 30+ local company stakes and 15 real-estate projects. Historically, real estate and Rwandan government bonds dominated its portfolio (together ≫70%). Recent information stresses investment in local infrastructure – e.g. RSSB subscribed Rwf10B to a domestic sustainability bond. Equity investments include stakes in banking, agribusiness, etc. Fixed deposits and local bonds provide steady income.<br>
                <span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> A 2019 law raised mandatory contributions, and revenues have grown accordingly. RSSB has introduced ESG reporting (e.g. renewable-energy targets) and is exploring private equity ventures. The aim is to deepen Rwanda's capital markets: RSSB now plays an "anchor investor" role in domestic projects. Nearly 100% local allocation persists.<br>
                <em>Rwanda's RSSB manages Rwf 2.14 trillion in pension assets, investing nearly 100% domestically, with significant exposure to real estate and Rwandan company equity holdings.<sup>5</sup></em>
                ''', unsafe_allow_html=True)
            elif country == "Ghana":
                st.markdown('''
                <span style="color:#072D92;font-weight:600;">Fund & Size:</span> SSNIT (Social Security and National Insurance Trust) is Ghana's main pension fund. Its portfolio was ~GHS 11.3 billion by end-2021 (latest published) and higher now. Ghana also created the Ghana Infrastructure Investment Fund (GIIF) for development projects.<br>
                <span style="color:#F58220;font-weight:600;">Domestic vs Foreign:</span> SSNIT's portfolio is essentially entirely Ghanaian. As of Dec 2023, 99% of SSNIT's investments were domestic. (Offshore exposure is negligible.)<br>
                <span style="color:#072D92;font-weight:600;">Asset Classes/Sectors:</span> SSNIT is heavily invested in real estate and equities. By one estimate, it holds ~49% in equities (roughly 35.8% in unlisted stakes, 13.5% listed) and ~30.5% in property. It also has large allocations by sector: ~37.5% real estate, ~16% energy, ~15% financial, ~15% services and ~3.5% manufacturing. (The rest is in cash and other assets.) Over time, SSNIT has become a major capital-market investor – on the GSE it holds GHS 2.42B of stocks.<br>
                <span style="color:#F58220;font-weight:600;">Trends/Regulation:</span> The 2020 Pensions Act envisions moving SSNIT to a fully-funded defined-contribution model by 2026, which is spurring asset reallocation plans. Currently SSNIT is reducing direct real-estate projects (30% → target 10%) and unlisted equities (to target 4%), while increasing fixed-income (toward a 60% target). It has faced legacy public-sector bond repayments. The upcoming reforms and growth of the pension sector should gradually diversify Ghanaian pension portfolios, but for now domestic investments remain dominant.<br>
                <em>Ghana's SSNIT portfolio is 99% domestically invested, with approximately 49% in equities (mostly unlisted), 30% in real estate, and minimal exposure to foreign assets.<sup>6</sup></em>
                ''', unsafe_allow_html=True)
    
    # Pension Fund Asset Class Mix by Country chart
    if not df_pension.empty:
        st.markdown("#### Pension Fund Asset Class Mix by Country")
        asset_cols = [
            'Domestic_Equities (%)',
            'Domestic_Bonds (%)',
            'Real_Estate (%)',
            'Private_Equity (%)',
            'Cash & Deposits (%)',
            'Foreign_Assets (%)'
        ]
        # Check which columns exist
        available_cols = [col for col in asset_cols if col in df_pension.columns]
        if available_cols:
            import plotly.graph_objects as go
            
            # Prepare data for stacked bar chart
            chart_data = df_pension.set_index('Country_Flag')[available_cols].fillna(0)
            countries = chart_data.index.tolist()
            
            # Color mapping for asset classes using OSAA theme colors
            color_map = {
                'Cash & Deposits (%)': '#003366',  # Deep Blue (OSAA)
                'Domestic_Bonds (%)': '#0072BC',  # Mid Blue (OSAA)
                'Domestic_Equities (%)': '#F26C2B',  # Orange (OSAA)
                'Foreign_Assets (%)': '#FFD34E',  # Yellow (OSAA)
                'Private_Equity (%)': '#007B33',  # Green (OSAA)
                'Real_Estate (%)': '#009D8C'  # Teal (OSAA)
            }
            
            # Create stacked bar chart
            fig = go.Figure()
            
            for col in available_cols:
                fig.add_trace(go.Bar(
                    x=countries,
                    y=chart_data[col].values,
                    name=col.replace(' (%)', ''),
                    marker_color=color_map.get(col, '#999999'),
                    hovertemplate=f"<b>%{{x}}</b><br>{col.replace(' (%)', '')}: %{{y:.1f}}%<extra></extra>"
                ))
            
            fig.update_layout(
                barmode='stack',
                height=500,
                xaxis_title="Country",
                yaxis_title="Percentage (%)",
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02,
                    font=dict(size=10),
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="rgba(0,0,0,0.2)",
                    borderwidth=1
                ),
                margin=dict(l=50, r=180, t=20, b=50),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Asset class data columns not found in the dataset.")
    
    # References section (only for 4.3.3.1)
    st.markdown('''---
#### References
<ol style="font-size:0.95em;">
<li>RisCura. Bright Africa Pension Industry Report 2021. Available at: <a href="https://brightafrica.riscura.com/downloads/pension-industry-report-2021" target="_blank">https://brightafrica.riscura.com/downloads/pension-industry-report-2021</a></li>
<li>GEPF. Annual Report 2022–2023. Available at: <a href="https://www.gepf.co.za/annual-reports/" target="_blank">https://www.gepf.co.za/annual-reports/</a></li>
<li>PenCom. Q3 2023 Report. Available at: <a href="https://www.pencom.gov.ng/category/publications/annual-reports/" target="_blank">https://www.pencom.gov.ng/category/publications/annual-reports/</a></li>
<li>NSSF Kenya. Investments Overview. Available at: <a href="https://www.nssf.or.ke/investments" target="_blank">https://www.nssf.or.ke/investments</a></li>
<li>Rwanda Social Security Board. Investments. Available at: <a href="https://www.rssb.rw/investment" target="_blank">https://www.rssb.rw/investment</a></li>
<li>SSNIT. Investment Portfolio. Available at: <a href="https://www.ssnit.org.gh/about-us/investments/" target="_blank">https://www.ssnit.org.gh/about-us/investments/</a></li>
</ol>
''', unsafe_allow_html=True)

