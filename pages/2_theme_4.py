import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# set_page_config MUST be the first Streamlit command
st.set_page_config(
    page_title="Theme 4: Domestic Resource Mobilization",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add parent directory to path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import data loading modules
try:
    import composite_indicator_methods as cim
    import universal_viz as uv
    DATA_AVAILABLE = True
except ImportError:
    DATA_AVAILABLE = False

# Import navigation component (logo only, Home button moved to left)
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

# Load data for graphs (only if needed for View 3)
if DATA_AVAILABLE:
    try:
        ref_data = uv.load_country_reference_data()
        df_main = uv.load_main_data()
        if not df_main.empty and not ref_data.empty:
            # Apply default filters (all Africa)
            filters = uv.setup_sidebar_filters(ref_data, df_main, key_prefix="theme4_view3")
            df_display = uv.filter_dataframe_by_selections(df_main, filters, ref_data)
        else:
            df_display = pd.DataFrame()
            ref_data = pd.DataFrame()
    except Exception:
        df_display = pd.DataFrame()
        ref_data = pd.DataFrame()
else:
    df_display = pd.DataFrame()
    ref_data = pd.DataFrame()

# Helper function to render Indicator 4.3.1.1 graph (exact replica from exploratory view)
def render_indicator_4311():
    """Render Market Capitalization to GDP graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Calculate Stock Market Capitalization to GDP (exact from exploratory view)
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
        
        if df_stock_cap.empty:
            st.info("No data available for Market Capitalization to GDP.")
            return
        
        # Filter for Africa region
        africa_ref_data_431 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data_431.empty:
            africa_countries_431 = africa_ref_data_431['Country or Area'].unique()
            df_stock_cap = df_stock_cap[df_stock_cap['country_or_area'].isin(africa_countries_431)]
        
        if df_stock_cap.empty:
            st.info("No data available for selected region.")
            return
        
        # Use all data (no filters for policy brief)
        filtered_stock_cap = df_stock_cap.copy()
        
        # Get GDP per capita data for tooltips
        gdp_pc_label = "GDP per Capita Constant USD - USD - value"
        gdp_pc_data = df_display[df_display['indicator_label'] == gdp_pc_label].copy()
        
        # Line chart with reference bands (exact implementation)
        fig = go.Figure()
        
        # Identify outliers (countries with values > 200% - like Seychelles)
        outlier_threshold = 200
        outlier_countries = filtered_stock_cap.groupby('country_or_area')['value'].max()
        outlier_countries = outlier_countries[outlier_countries > outlier_threshold].index.tolist()
        
        # Filter out outliers for main chart and regional average calculation
        filtered_main = filtered_stock_cap[~filtered_stock_cap['country_or_area'].isin(outlier_countries)].copy()
        
        # Calculate regional average (excluding outliers)
        filtered_for_avg = filtered_stock_cap[~filtered_stock_cap['country_or_area'].isin(outlier_countries)].copy()
        regional_avg = pd.DataFrame()
        if not filtered_for_avg.empty:
            regional_avg = filtered_for_avg.groupby('year')['value'].mean().reset_index()
            regional_avg.columns = ['year', 'regional_avg']
        
        # Determine y-axis range
        if not filtered_main.empty:
            y_max = min(filtered_main['value'].max() * 1.1, 200)  # Cap at 200% or 10% above max
            y_max = max(y_max, 100)  # At least show up to 100%
        else:
            y_max = 200
        
        # Add reference bands (shaded areas) with labels - EXACT from exploratory view
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=0, x1=1, y1=20,
            fillcolor="#FFD34E",
            opacity=0.15,
            layer="below",
            line_width=0,
        )
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=20, x1=1, y1=60,
            fillcolor="#F26C2B",
            opacity=0.15,
            layer="below",
            line_width=0,
        )
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
                    legendrank=1
                ))
        
        # Show top 10 countries by latest value (excluding outliers)
        if not filtered_main.empty:
            latest_values = filtered_main.groupby('country_or_area')['value'].last().sort_values(ascending=False)
            top_countries = latest_values.head(10).index.tolist()
            countries_to_show = top_countries
        else:
            countries_to_show = []
        
        # Add country lines
        for country in countries_to_show:
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
                    marker=dict(color=line_color, size=4),
                    hovertemplate=hovertemplate,
                    customdata=country_data_merged['value_gdppc'].fillna(0),
                    showlegend=True
                ))
        
        # Show warning if outliers are excluded
        if outlier_countries:
            st.info(f"⚠️ Note: Countries with extreme values (>200% of GDP) are excluded from the main chart for clarity: {', '.join(outlier_countries[:5])}{' and more' if len(outlier_countries) > 5 else ''}.")
        
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
            yaxis=dict(range=[0, y_max]),
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
        
        # Add link back to exploratory view
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 0.5rem;">
            <p style="margin: 0; color: #666; font-size: 0.85rem;">
                Navigate to Exploratory View → Topic 4.3 → Sub-topic 4.3.1
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("View full interactive version", key="link_4311", use_container_width=True):
                st.switch_page("pages/5_topic_4_3.py")
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

# Helper function to render Indicator 4.3.1.2 graph (Portfolio Investment Bonds - Heatmap) - exact replica
def render_indicator_4312():
    """Render Portfolio Investment Bonds heatmap - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Load Portfolio Investment Bonds data (exact from exploratory view)
        bond_indicator_label = "Portfolio investment, bonds (PPG + PNG) (NFL, current US$)"
        df_bonds = df_display[df_display['indicator_label'] == bond_indicator_label].copy()
        
        # Calculate % of GDP for metric toggle
        if not df_bonds.empty:
            gdp_data = df_display[df_display['indicator_label'] == 'GDP (current US$)'].copy()
            if not gdp_data.empty:
                df_bonds_merged = df_bonds.merge(
                    gdp_data[['country_or_area', 'year', 'value']],
                    on=['country_or_area', 'year'],
                    how='left',
                    suffixes=('_bonds', '_gdp')
                )
                df_bonds_merged['value_pct_gdp'] = (df_bonds_merged['value_bonds'] / df_bonds_merged['value_gdp']) * 100
                df_bonds_merged = df_bonds_merged.dropna(subset=['value_bonds'])
                df_bonds = df_bonds_merged.copy()
        
        # Filter for Africa
        africa_ref_data_432 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data_432.empty:
            africa_countries_432 = africa_ref_data_432['Country or Area'].unique()
            df_bonds = df_bonds[df_bonds['country_or_area'].isin(africa_countries_432)]
        
        if df_bonds.empty:
            st.info("No data available for Portfolio Investment Bonds.")
            return
        
        # Use normalized heatmap view (default for policy brief) - EXACT from exploratory view
        value_col = 'value_pct_gdp'
        colorbar_title = "% of GDP"
        zmin = 0.0
        zmax = 1.0
        
        # Filter out negative values
        filtered_bonds_display = df_bonds[df_bonds[value_col].notna()].copy()
        if value_col in filtered_bonds_display.columns:
            filtered_bonds_display = filtered_bonds_display[filtered_bonds_display[value_col] >= 0]
        
        if filtered_bonds_display.empty:
            st.info("No valid data for heatmap visualization.")
            return
        
        # Prepare heatmap data (exact from exploratory view)
        heatmap_df = filtered_bonds_display[['country_or_area', 'year', value_col]].copy()
        
        # Fix Cause 3: Ensure year is properly formatted as integer then string for categorical axis
        heatmap_df['year'] = pd.to_numeric(heatmap_df['year'], errors='coerce')
        heatmap_df = heatmap_df.dropna(subset=['year'])
        
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
        country_data_counts = heatmap_df.groupby('country_or_area')[value_col].apply(lambda x: (~pd.isna(x)).sum())
        if len(country_data_counts) > 20:
            # Only filter if we have many countries
            countries_with_sufficient_data = country_data_counts[country_data_counts >= 3].index.tolist()
            heatmap_df = heatmap_df[heatmap_df['country_or_area'].isin(countries_with_sufficient_data)]
        else:
            # Show all countries if we have few
            countries_with_sufficient_data = country_data_counts.index.tolist()
        
        if heatmap_df.empty:
            st.warning("⚠️ No data available for heatmap visualization.")
        else:
            # Sort countries by number of non-null data points (descending)
            country_data_counts_filtered = heatmap_df.groupby('country_or_area')[value_col].apply(lambda x: (~pd.isna(x)).sum()).sort_values(ascending=False)
            sorted_countries = country_data_counts_filtered.index.tolist()
            
            # Get sorted years (as strings, since we converted to string)
            sorted_years = sorted(heatmap_df['year'].unique())
            
            # Create pivot table with proper data validation
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
            
            # Prepare customdata for hover (unit label)
            if not heatmap_pivot.empty:
                customdata_unit = "%"
                customdata_array = np.full(heatmap_pivot.shape, customdata_unit)
            else:
                customdata_array = None
            
            # Create heatmap (fixed scale 0-1% of GDP)
            if not heatmap_pivot.empty and heatmap_pivot.shape[1] > 0:
                # Years are already strings from earlier conversion - keep them as strings
                x_values_all = heatmap_pivot.columns.tolist()
                y_values = heatmap_pivot.index.tolist()
                
                # Convert to numpy array and ensure proper types
                z_values = heatmap_pivot.values
                
                # Ensure z_values are numeric (float)
                z_values = pd.DataFrame(z_values).apply(pd.to_numeric, errors='coerce').values
                
                # Verify we have numeric data
                if z_values.dtype == 'object':
                    z_values = np.array([[float(val) if pd.notna(val) and val is not None and not (isinstance(val, float) and np.isnan(val)) else np.nan for val in row] for row in z_values], dtype=float)
                
                # Check if we have any valid (non-NaN) values
                valid_count = np.sum(~np.isnan(z_values))
                if valid_count == 0:
                    st.warning("⚠️ No valid numeric values found in heatmap data.")
                elif valid_count < z_values.size * 0.1:
                    st.info(f"ℹ️ Only {valid_count}/{z_values.size} cells have valid data ({(valid_count/z_values.size*100):.1f}%). This is normal for sparse datasets.")
                
                # Determine which years to show on x-axis
                if len(x_values_all) > 20:
                    step = max(1, len(x_values_all) // 20)
                    tick_indices = list(range(0, len(x_values_all), step))
                    if tick_indices[-1] != len(x_values_all) - 1:
                        tick_indices.append(len(x_values_all) - 1)
                    x_tickvals = [x_values_all[i] for i in sorted(set(tick_indices))]
                else:
                    x_tickvals = x_values_all
                
                # Create heatmap figure (exact from exploratory view)
                heatmap_data = {
                    "z": z_values,
                    "x": x_values_all,
                    "y": y_values,
                    "colorscale": "Blues",
                    "showscale": True,
                    "zmin": zmin,
                    "zmax": zmax,
                    "xgap": 1,
                    "ygap": 1,
                    "hoverongaps": False,
                    "text": None,
                    "texttemplate": "",
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
                
                if customdata_array is not None:
                    heatmap_data['customdata'] = customdata_array
                
                fig = go.Figure(data=go.Heatmap(**heatmap_data))
                
                # Add crisis band overlays
                if 2007 in sorted_years or 2008 in sorted_years or 2009 in sorted_years:
                    fig.add_vrect(
                        x0=2007.5, x1=2009.5,
                        fillcolor="grey",
                        opacity=0.2,
                        layer="below",
                        line_width=0
                    )
                
                if 2013 in sorted_years or 2014 in sorted_years or 2015 in sorted_years or 2016 in sorted_years:
                    fig.add_vrect(
                        x0=2013.5, x1=2016.5,
                        fillcolor="grey",
                        opacity=0.2,
                        layer="below",
                        line_width=0
                    )
                
                if 2019 in sorted_years or 2020 in sorted_years or 2021 in sorted_years:
                    fig.add_vrect(
                        x0=2019.5, x1=2021.5,
                        fillcolor="grey",
                        opacity=0.2,
                        layer="below",
                        line_width=0
                    )
                
                # Update layout (exact from exploratory view)
                fig.update_layout(
                    title=None,
                    height=600,
                    xaxis=dict(
                        title=dict(
                            text="Year",
                            font=dict(size=11)
                        ),
                        type="category",
                        tickangle=-45,
                        tickmode='array',
                        tickvals=x_tickvals,
                        ticktext=x_tickvals,
                        showticklabels=True,
                        tickfont=dict(size=9)
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
                st.info("Unable to create heatmap: insufficient valid data.")
        
        # Add link back to exploratory view
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 0.5rem;">
            <p style="margin: 0; color: #666; font-size: 0.85rem;">
                Navigate to Exploratory View → Topic 4.3 → Sub-topic 4.3.1
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("View full interactive version", key="link_4312", use_container_width=True):
                st.switch_page("pages/5_topic_4_3.py")
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

# Helper function to render Indicator 4.3.1.3 graph (Adequacy of International Reserves) - exact replica
def render_indicator_4313():
    """Render Adequacy of International Reserves graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Calculate Adequacy of International Reserves (exact from exploratory view)
        df_reserves = cim.calculate_adequacy_of_international_reserves(df_display)
        if not df_reserves.empty:
            df_reserves = df_reserves.rename(columns={'Adequacy of International Reserves': 'value'})
            df_reserves['indicator_label'] = 'Adequacy of International Reserves'
        
        # Filter for Africa
        africa_ref_data_433 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data_433.empty:
            africa_countries_433 = africa_ref_data_433['Country or Area'].unique()
            df_reserves = df_reserves[df_reserves['country_or_area'].isin(africa_countries_433)]
        
        if df_reserves.empty:
            st.info("No data available for Adequacy of International Reserves.")
            return
        
        # Use all data (no filters for policy brief)
        filtered_reserves = df_reserves.copy()
        
        # Snapshot view (latest year) - MAIN VIEW (exact from exploratory view)
        snapshot_year = filtered_reserves['year'].max()
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
                # Normalize data to handle extreme outliers (exact from exploratory view)
                original_values = snapshot_data['value'].copy()
                
                # Calculate percentiles to identify outliers
                q1 = snapshot_data['value'].quantile(0.25)
                q3 = snapshot_data['value'].quantile(0.75)
                iqr = q3 - q1
                
                # Define reasonable bounds for visualization
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
                
                # Color encoding based on risk tiers (using original values for color) - EXACT from exploratory view
                colors = []
                for val in snapshot_data['value']:
                    if val >= 1.0:  # ≥100% (Adequate)
                        colors.append('#007B33')
                    elif val >= 0.5:  # 50-99% (Moderate)
                        colors.append('#FFD34E')
                    else:  # <50% (High risk)
                        colors.append('#F26C2B')
                
                fig = go.Figure()
                
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
                
                # Add risk tier bands (exact from exploratory view)
                # Critical Risk (Negative values)
                fig.add_shape(
                    type="rect",
                    xref="x", yref="paper",
                    x0=-10, y0=0, x1=0, y1=1,
                    fillcolor="#B30000",
                    opacity=0.1,
                    layer="below",
                    line_width=0,
                )
                # High Risk: 0 to 0.5
                fig.add_shape(
                    type="rect",
                    xref="x", yref="paper",
                    x0=0, y0=0, x1=0.5, y1=1,
                    fillcolor="#F26C2B",
                    opacity=0.1,
                    layer="below",
                    line_width=0,
                )
                # Moderate Risk: 0.5 to 1.0
                fig.add_shape(
                    type="rect",
                    xref="x", yref="paper",
                    x0=0.5, y0=0, x1=1.0, y1=1,
                    fillcolor="#FFD34E",
                    opacity=0.1,
                    layer="below",
                    line_width=0,
                )
                # Adequate Coverage: 1.0+
                fig.add_shape(
                    type="rect",
                    xref="x", yref="paper",
                    x0=1.0, y0=0, x1=5.0, y1=1,
                    fillcolor="#007B33",
                    opacity=0.1,
                    layer="below",
                    line_width=0,
                )
                
                # Determine x-axis range based on normalized data
                x_min = min(snapshot_data['value_normalized'].min(), -1.0)
                x_max = max(snapshot_data['value_normalized'].max(), 2.0)
                
                fig.update_layout(
                    height=500,
                    xaxis_title="Reserve Adequacy Ratio (Reserves / Short-Term Debt)",
                    yaxis_title="Country",
                    hovermode='closest',
                    margin=dict(l=150, r=50, t=20, b=50),
                    xaxis=dict(
                        range=[x_min - 0.5, x_max + 0.5]
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No data available for year {snapshot_year}.")
        
        # Add link back to exploratory view
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 0.5rem;">
            <p style="margin: 0; color: #666; font-size: 0.85rem;">
                Navigate to Exploratory View → Topic 4.3 → Sub-topic 4.3.1
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("View full interactive version", key="link_4313", use_container_width=True):
                st.switch_page("pages/5_topic_4_3.py")
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

# Helper function to render Indicator 4.3.2.1 graph (Banking Sector Development Index) - exact replica
def render_indicator_4321():
    """Render Banking Sector Development Index graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Calculate Banking Sector Development Index (exact from exploratory view)
        df_bsdi = cim.calculate_banking_sector_development_index(df_display)
        if df_bsdi.empty:
            st.info("No data available for Banking Sector Development Index.")
            return
        
        df_bsdi = df_bsdi.rename(columns={'Banking Sector Development Index': 'value'})
        df_bsdi['indicator_label'] = 'Banking Sector Development Index'
        
        # Filter for Africa
        africa_ref_data_4321 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data_4321.empty:
            africa_countries_4321 = africa_ref_data_4321['Country or Area'].unique()
            df_bsdi = df_bsdi[df_bsdi['country_or_area'].isin(africa_countries_4321)]
        
        if df_bsdi.empty:
            st.info("No data available for selected region.")
            return
        
        # Use all data (no filters for policy brief)
        filtered_bsdi = df_bsdi.copy()
        
        # Create line chart with reference bands (exact from exploratory view)
        fig = go.Figure()
        
        # Add reference bands (shaded areas) for development tiers
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=0, x1=1, y1=0.4,
            fillcolor="#F26C2B",
            opacity=0.2,
            layer="below",
            line_width=0,
        )
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=0.4, x1=1, y1=0.7,
            fillcolor="#FFD34E",
            opacity=0.2,
            layer="below",
            line_width=0,
        )
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
        
        # Get component data for tooltips
        capital_data = df_display[df_display['indicator_label'] == 'Bank capital to assets ratio (%)'].copy()
        liquidity_data = df_display[df_display['indicator_label'] == 'Bank liquid reserves to bank assets ratio (%)'].copy()
        credit_data = df_display[df_display['indicator_label'] == 'Domestic credit provided by financial sector (% of GDP)'].copy()
        
        # Add country lines (all countries, but limit display if too many)
        countries_list_4321 = sorted(filtered_bsdi['country_or_area'].dropna().unique())
        # Limit to top 15 by latest value for readability
        if len(countries_list_4321) > 15:
            latest_values = filtered_bsdi.groupby('country_or_area')['value'].last().sort_values(ascending=False)
            countries_list_4321 = latest_values.head(15).index.tolist()
        
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
                
                line_width = 2
                
                # Merge with component data for tooltips
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
                    marker=dict(color=line_color, size=4),
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
        
        # Add link back to exploratory view
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 0.5rem;">
            <p style="margin: 0; color: #666; font-size: 0.85rem;">
                Navigate to Exploratory View → Topic 4.3 → Sub-topic 4.3.2
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("View full interactive version", key="link_4321", use_container_width=True):
                st.switch_page("pages/5_topic_4_3.py")
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

# Helper function to render Indicator 4.3.2.2 graph (Private Sector Credit to GDP) - exact replica
def render_indicator_4322():
    """Render Private Sector Credit to GDP graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Load Private Sector Credit data (exact from exploratory view)
        credit_indicator_label = "Domestic credit provided by financial sector (% of GDP)"
        df_credit = df_display[df_display['indicator_label'] == credit_indicator_label].copy()
        
        if df_credit.empty:
            st.info("No data available for Private Sector Credit to GDP.")
            return
        
        # Filter for Africa
        africa_ref_data_4322 = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data_4322.empty:
            africa_countries_4322 = africa_ref_data_4322['Country or Area'].unique()
            df_credit = df_credit[df_credit['country_or_area'].isin(africa_countries_4322)]
        
        if df_credit.empty:
            st.info("No data available for selected region.")
            return
        
        # Use all data (no filters for policy brief)
        filtered_credit = df_credit.copy()
        filtered_credit_sorted = filtered_credit.sort_values(['country_or_area', 'year'])
        
        # Create line chart with reference bands (exact from exploratory view)
        fig = go.Figure()
        
        # Determine max value for y-axis
        y_max = max(filtered_credit['value'].max() * 1.1, 200) if not filtered_credit.empty else 200
        
        # Add reference bands (shaded areas) for financial depth tiers
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=0, x1=1, y1=40,
            fillcolor="#F26C2B",
            opacity=0.2,
            layer="below",
            line_width=0,
        )
        fig.add_shape(
            type="rect",
            xref="paper", yref="y",
            x0=0, y0=40, x1=1, y1=80,
            fillcolor="#FFD34E",
            opacity=0.2,
            layer="below",
            line_width=0,
        )
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
        
        # Calculate change since 2000 for tooltips
        baseline_2000 = filtered_credit_sorted[filtered_credit_sorted['year'] == 2000].set_index('country_or_area')['value']
        filtered_credit_sorted['change_since_2000'] = filtered_credit_sorted.apply(
            lambda row: row['value'] - baseline_2000.get(row['country_or_area'], np.nan) if row['country_or_area'] in baseline_2000.index else np.nan,
            axis=1
        )
        
        # Add country lines (limit to top 15 by latest value for readability)
        countries_list_4322 = sorted(filtered_credit_sorted['country_or_area'].dropna().unique())
        if len(countries_list_4322) > 15:
            latest_values = filtered_credit_sorted.groupby('country_or_area')['value'].last().sort_values(ascending=False)
            countries_list_4322 = latest_values.head(15).index.tolist()
        
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
                    marker=dict(color=line_color, size=4),
                    hovertemplate='%{text}',
                    text=hover_texts,
                    showlegend=True
                ))
        
        fig.update_layout(
            height=500,
            xaxis_title="Year",
            yaxis_title="Domestic Credit Provided by Financial Sector (% of GDP)",
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
        
        # Add link back to exploratory view
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 0.5rem;">
            <p style="margin: 0; color: #666; font-size: 0.85rem;">
                Navigate to Exploratory View → Topic 4.3 → Sub-topic 4.3.2
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("View full interactive version", key="link_4322", use_container_width=True):
                st.switch_page("pages/5_topic_4_3.py")
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

# ========================================
# IFF INDICATOR HELPER FUNCTIONS (Topic 4.4)
# ========================================

def render_indicator_4421():
    """Render Trade Mispricing graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Define trade mispricing indicators
        trade_mispricing_indicators = {
            "Global Trading Partners (USD Millions)": {
                "label": "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and all of their Global Trading Partners, 2009–2018 in USD Millions",
                "code": "GFI.TableE.gap_usd_all",
                "color": "#F26C2B"
            }
        }
        
        # Get data for the indicator
        indicator_label = trade_mispricing_indicators["Global Trading Partners (USD Millions)"]["label"]
        chart_data = df_display[df_display['indicator_label'] == indicator_label].copy()
        
        # Filter for Africa
        africa_ref_data = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data.empty:
            africa_countries = africa_ref_data['Country or Area'].unique()
            chart_data = chart_data[chart_data['country_or_area'].isin(africa_countries)]
        
        if chart_data.empty:
            st.info("No data available for Trade Mispricing.")
            return
        
        # Get latest year data for bar chart
        latest_year = chart_data['year'].max()
        year_data = chart_data[chart_data['year'] == latest_year].copy()
        
        if year_data.empty:
            st.info("No data available for the latest year.")
            return
        
        # Sort by value and take top 15
        year_data_sorted = year_data.sort_values('value', ascending=False).head(15)
        
        # Create horizontal bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=year_data_sorted['country_or_area'],
            x=year_data_sorted['value'],
            orientation='h',
            marker_color=trade_mispricing_indicators["Global Trading Partners (USD Millions)"]["color"],
            hovertemplate="<b>%{y}</b><br>Year: " + str(int(latest_year)) + "<br>Value: %{x:,.0f} USD Millions<br><extra></extra>"
        ))
        
        fig.update_layout(
            title="Indicator 4.4.2.1 – Trade Mispricing",
            xaxis_title="Value Gap (USD Millions)",
            yaxis_title="Country",
            height=max(500, len(year_data_sorted) * 40),
            yaxis=dict(categoryorder='total ascending'),
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_4421_policy")
        
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

def render_indicator_4422():
    """Render Tax Evasion graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Define tax type indicators
        tax_type_indicators = {
            "Active taxpayers on PIT register as percentage of Labor Force": {"color": "#0072BC", "type": "PIT"},
            "On CIT register": {"color": "#00A1A1", "type": "CIT"},
            "On VAT register": {"color": "#F26C2B", "type": "VAT"}
        }
        
        # Filter to only available indicators
        available_tax_indicators = {
            k: v for k, v in tax_type_indicators.items()
            if k in df_display['indicator_label'].unique()
        }
        
        if not available_tax_indicators:
            st.info("No data available for Tax Evasion indicators.")
            return
        
        # Get latest year
        chart_data = df_display[df_display['indicator_label'].isin(available_tax_indicators.keys())].copy()
        latest_year = chart_data['year'].max() if not chart_data.empty else None
        
        if latest_year is None:
            st.info("No data available for Tax Evasion.")
            return
        
        year_data = chart_data[chart_data['year'] == latest_year].copy()
        
        # Filter for Africa
        africa_ref_data = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data.empty:
            africa_countries = africa_ref_data['Country or Area'].unique()
            year_data = year_data[year_data['country_or_area'].isin(africa_countries)]
        
        if year_data.empty:
            st.info("No data available for selected region.")
            return
        
        # Create grouped bar chart by tax type
        fig = go.Figure()
        
        countries = sorted(year_data['country_or_area'].unique())
        for tax_label in available_tax_indicators.keys():
            tax_data = year_data[year_data['indicator_label'] == tax_label]
            tax_color = available_tax_indicators[tax_label]["color"]
            
            country_values = []
            for country in countries:
                country_row = tax_data[tax_data['country_or_area'] == country]
                if len(country_row) > 0:
                    country_values.append(country_row['value'].values[0])
                else:
                    country_values.append(0)
            
            fig.add_trace(go.Bar(
                name=tax_label,
                x=countries,
                y=country_values,
                marker_color=tax_color,
                hovertemplate=f"<b>{tax_label}</b><br>%{{x}}<br>Value: %{{y:.2f}}%<br><extra></extra>"
            ))
        
        fig.update_layout(
            title="Indicator 4.4.2.2 – Tax Evasion and Aggressive Tax Planning",
            xaxis_title="Country",
            yaxis_title="Percentage",
            barmode='group',
            height=500,
            hovermode='closest',
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_4422_policy")
        
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

def render_indicator_4423():
    """Render Criminal Activities graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Get UNODC data
        unodc_indicator_label = "Monetary losses (in USD) to drug sales. Amount of drugs seized in kilograms multiplied by the drug price in kilograms. Excludes all seizures not measured in grams or kilograms."
        unodc_indicator_code = "UNODC.DPS.losses"
        
        # Try to get data by code first, then by label
        if 'indicator_code' in df_display.columns:
            chart_data = df_display[df_display['indicator_code'].astype(str).str.strip() == unodc_indicator_code].copy()
        else:
            chart_data = df_display[df_display['indicator_label'] == unodc_indicator_label].copy()
        
        if chart_data.empty:
            chart_data = df_display[df_display['indicator_label'] == unodc_indicator_label].copy()
        
        if chart_data.empty:
            st.info("No data available for Criminal Activities.")
            return
        
        # Filter for Africa
        africa_ref_data = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data.empty:
            africa_countries = africa_ref_data['Country or Area'].unique()
            chart_data = chart_data[chart_data['country_or_area'].isin(africa_countries)]
        
        if chart_data.empty:
            st.info("No data available for selected region.")
            return
        
        # Get latest year for bar chart
        latest_year = chart_data['year'].max()
        year_data = chart_data[chart_data['year'] == latest_year].copy()
        
        if year_data.empty:
            st.info("No data available for the latest year.")
            return
        
        # Sort by value and take top 15
        year_data_sorted = year_data.sort_values('value', ascending=False).head(15)
        
        # Create bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=year_data_sorted['country_or_area'],
            y=year_data_sorted['value'],
            marker=dict(
                color=year_data_sorted['value'],
                colorscale='Reds',
                showscale=True
            ),
            hovertemplate="<b>%{x}</b><br>Year: " + str(int(latest_year)) + "<br>Value: $%{y:,.0f}<br><extra></extra>"
        ))
        
        fig.update_layout(
            title="Indicator 4.4.2.3 – IFFs from Drug Trafficking",
            xaxis_title="Country",
            yaxis_title="Value (USD)",
            height=500,
            xaxis={'categoryorder': 'total descending'},
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_4423_policy")
        
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

def render_indicator_4424():
    """Render Corruption graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Get Control of Corruption indicator
        corruption_indicator_label = "Control of Corruption: Estimate"
        chart_data = df_display[df_display['indicator_label'] == corruption_indicator_label].copy()
        
        if chart_data.empty:
            st.info("No data available for Corruption indicator.")
            return
        
        # Filter for Africa
        africa_ref_data = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data.empty:
            africa_countries = africa_ref_data['Country or Area'].unique()
            chart_data = chart_data[chart_data['country_or_area'].isin(africa_countries)]
        
        if chart_data.empty:
            st.info("No data available for selected region.")
            return
        
        # Get latest year
        latest_year = chart_data['year'].max()
        year_data = chart_data[chart_data['year'] == latest_year].copy()
        
        if year_data.empty:
            st.info("No data available for the latest year.")
            return
        
        # Sort by value (lower is worse for corruption)
        year_data_sorted = year_data.sort_values('value', ascending=True).head(20)
        
        # Create bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=year_data_sorted['country_or_area'],
            y=year_data_sorted['value'],
            marker=dict(
                color=year_data_sorted['value'],
                colorscale='RdYlGn',
                reversescale=True,
                showscale=True,
                cmin=-2.5,
                cmax=2.5
            ),
            hovertemplate="<b>%{x}</b><br>Year: " + str(int(latest_year)) + "<br>Control of Corruption: %{y:.2f}<br><extra></extra>"
        ))
        
        fig.update_layout(
            title="Indicator 4.4.2.4 – Corruption-related IFFs",
            xaxis_title="Country",
            yaxis_title="Control of Corruption Score",
            height=500,
            xaxis={'categoryorder': 'total ascending'},
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_4424_policy")
        
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

def render_indicator_4431():
    """Render Detection Efficacy graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Define governance indicators for composite
        governance_indicators = {
            "Control of Corruption: Estimate": {
                "label": "Control of Corruption: Estimate",
                "color": "#F26C2B"
            },
            "CPIA transparency, accountability, and corruption in the public sector rating": {
                "label": "CPIA transparency, accountability, and corruption in the public sector rating",
                "code": "IQ.CPA.PUBS.XQ",
                "color": "#FFD34E"
            },
            "CPIA quality of public administration rating": {
                "label": "CPIA quality of public administration rating",
                "code": "IQ.CPA.PADM.XQ",
                "color": "#009D8C"
            }
        }
        
        # Get available indicators
        available_indicators = {}
        for key, info in governance_indicators.items():
            if info["label"] in df_display['indicator_label'].unique():
                available_indicators[key] = info
            elif info.get("code") and 'indicator_code' in df_display.columns:
                if info["code"] in df_display['indicator_code'].astype(str).values:
                    available_indicators[key] = info
        
        if not available_indicators:
            st.info("No data available for Detection Efficacy indicators.")
            return
        
        # Get latest year
        chart_data = df_display[df_display['indicator_label'].isin([v["label"] for v in available_indicators.values()])].copy()
        latest_year = chart_data['year'].max() if not chart_data.empty else None
        
        if latest_year is None:
            st.info("No data available for Detection Efficacy.")
            return
        
        year_data = chart_data[chart_data['year'] == latest_year].copy()
        
        # Filter for Africa
        africa_ref_data = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data.empty:
            africa_countries = africa_ref_data['Country or Area'].unique()
            year_data = year_data[year_data['country_or_area'].isin(africa_countries)]
        
        if year_data.empty:
            st.info("No data available for selected region.")
            return
        
        # Calculate average score per country across indicators
        country_scores = year_data.groupby('country_or_area')['value'].mean().reset_index()
        country_scores = country_scores.sort_values('value', ascending=False).head(20)
        
        # Create bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=country_scores['country_or_area'],
            y=country_scores['value'],
            marker_color='#0072BC',
            hovertemplate="<b>%{x}</b><br>Year: " + str(int(latest_year)) + "<br>Efficacy Score: %{y:.2f}<br><extra></extra>"
        ))
        
        fig.update_layout(
            title="Indicator 4.4.3.1 – Efficacy of Anti-IFF Measures",
            xaxis_title="Country",
            yaxis_title="Efficacy Score (Average)",
            height=500,
            xaxis={'categoryorder': 'total descending'},
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_4431_policy")
        
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

def render_indicator_4432b():
    """Render Resources and ICT Infrastructure graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Look for ICT-related indicators (these may vary based on available data)
        ict_indicators = [
            "% staff in ICT support",
            "ICT expenditure (% of total)",
            "ICT operating cost (% of total operating expenditure)"
        ]
        
        # Find available indicators
        available_ict = [ind for ind in ict_indicators if ind in df_display['indicator_label'].unique()]
        
        if not available_ict:
            st.info("No data available for Resources and ICT Infrastructure indicators.")
            return
        
        # Use the first available indicator
        chart_data = df_display[df_display['indicator_label'] == available_ict[0]].copy()
        
        # Filter for Africa
        africa_ref_data = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data.empty:
            africa_countries = africa_ref_data['Country or Area'].unique()
            chart_data = chart_data[chart_data['country_or_area'].isin(africa_countries)]
        
        if chart_data.empty:
            st.info("No data available for selected region.")
            return
        
        # Get latest year
        latest_year = chart_data['year'].max()
        year_data = chart_data[chart_data['year'] == latest_year].copy()
        
        if year_data.empty:
            st.info("No data available for the latest year.")
            return
        
        # Sort and take top 20
        year_data_sorted = year_data.sort_values('value', ascending=False).head(20)
        
        # Create bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=year_data_sorted['country_or_area'],
            y=year_data_sorted['value'],
            marker_color='#009D8C',
            hovertemplate="<b>%{x}</b><br>Year: " + str(int(latest_year)) + "<br>Value: %{y:.2f}%<br><extra></extra>"
        ))
        
        fig.update_layout(
            title="Indicator 4.4.3.2.b – Resources and ICT Infrastructure",
            xaxis_title="Country",
            yaxis_title=available_ict[0],
            height=500,
            xaxis={'categoryorder': 'total descending'},
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_4432b_policy")
        
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

def render_indicator_4432c():
    """Render Staff Metrics graph - exact replica from exploratory view"""
    if df_display.empty or not DATA_AVAILABLE:
        st.info("Data not available. Please ensure data files are loaded.")
        return
    
    try:
        # Look for staff-related indicators
        staff_indicators = [
            "Number of auditors",
            "Number of tax officials",
            "Staff in tax administration"
        ]
        
        # Find available indicators
        available_staff = [ind for ind in staff_indicators if ind in df_display['indicator_label'].unique()]
        
        if not available_staff:
            st.info("No data available for Staff Metrics indicators.")
            return
        
        # Use the first available indicator
        chart_data = df_display[df_display['indicator_label'] == available_staff[0]].copy()
        
        # Filter for Africa
        africa_ref_data = ref_data[ref_data['Region Name'] == 'Africa'].copy() if not ref_data.empty else pd.DataFrame()
        if not africa_ref_data.empty:
            africa_countries = africa_ref_data['Country or Area'].unique()
            chart_data = chart_data[chart_data['country_or_area'].isin(africa_countries)]
        
        if chart_data.empty:
            st.info("No data available for selected region.")
            return
        
        # Get latest year
        latest_year = chart_data['year'].max()
        year_data = chart_data[chart_data['year'] == latest_year].copy()
        
        if year_data.empty:
            st.info("No data available for the latest year.")
            return
        
        # Sort and take top 20
        year_data_sorted = year_data.sort_values('value', ascending=False).head(20)
        
        # Create bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=year_data_sorted['country_or_area'],
            y=year_data_sorted['value'],
            marker_color='#7C4DFF',
            hovertemplate="<b>%{x}</b><br>Year: " + str(int(latest_year)) + "<br>Value: %{y:,.0f}<br><extra></extra>"
        ))
        
        fig.update_layout(
            title="Indicator 4.4.3.2.c – Staff Metrics",
            xaxis_title="Country",
            yaxis_title=available_staff[0],
            height=500,
            xaxis={'categoryorder': 'total descending'},
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="plot_4432c_policy")
        
    except Exception as e:
        st.info(f"Unable to render graph: {str(e)}")

# Initialize session state for view navigation
if 'current_view' not in st.session_state:
    st.session_state.current_view = 1  # Default to View 1: Exploratory View

# === Custom Styling for This Page ===
st.markdown("""
<style>
    /* Page-specific styling */
    .theme-hero {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.03) 0%, rgba(232, 119, 34, 0.02) 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        border-left: 6px solid #E87722;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    
    .theme-hero h1 {
        color: #002B7F;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .theme-hero-divider {
        width: 120px;
        height: 4px;
        background: linear-gradient(90deg, #E87722, #F68E42);
        border-radius: 4px;
        margin: 1rem 0 1.5rem 0;
    }
    
    .theme-hero p {
        color: #555;
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 0;
    }
    
    /* Rationale Card */
    .rationale-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #002B7F;
        margin-bottom: 2.5rem;
    }
    
    .rationale-card h3 {
        color: #002B7F;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .rationale-item {
        background: linear-gradient(180deg, #F9FAFB 0%, #FFFFFF 100%);
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 3px solid #E87722;
    }
    
    .rationale-item:last-child {
        margin-bottom: 0;
    }
    
    .rationale-label {
        color: #E87722;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .rationale-text {
        color: #333;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Three-View Navigation Bar */
    .nav-button-container {
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Style Streamlit buttons to look like tabs - Navy blue theme */
    button[kind="primary"] {
        background: linear-gradient(135deg, #002B7F 0%, #003d99 100%) !important;
        background-color: #002B7F !important;
        color: white !important;
        border: 2px solid #002B7F !important;
        box-shadow: 0 4px 12px rgba(0, 43, 127, 0.3) !important;
        font-weight: 600 !important;
    }
    
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #001f5c 0%, #002B7F 100%) !important;
        background-color: #001f5c !important;
        border-color: #001f5c !important;
    }
    
    button[kind="secondary"] {
        background: #F9FAFB !important;
        background-color: #F9FAFB !important;
        color: #555 !important;
        border: 2px solid transparent !important;
        font-weight: 600 !important;
    }
    
    button[kind="secondary"]:hover {
        background: #F0F4F8 !important;
        background-color: #F0F4F8 !important;
        border-color: #002B7F !important;
    }
    
    /* More specific selectors for navigation buttons */
    .nav-button-container button[kind="primary"] {
        background: linear-gradient(135deg, #002B7F 0%, #003d99 100%) !important;
        background-color: #002B7F !important;
        color: white !important;
        border: 2px solid #002B7F !important;
        box-shadow: 0 4px 12px rgba(0, 43, 127, 0.3) !important;
    }
    
    .nav-button-container button[kind="secondary"] {
        background: #F9FAFB !important;
        background-color: #F9FAFB !important;
        color: #555 !important;
        border: 2px solid transparent !important;
    }
    
    .nav-button-container button[kind="secondary"]:hover {
        background: #F0F4F8 !important;
        background-color: #F0F4F8 !important;
        border-color: #002B7F !important;
    }
    
    /* Topic Cards */
    .topic-card-enhanced {
        background: white;
        border-radius: 12px;
        padding: 0;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        height: 100%;
        overflow: hidden;
        border: 1px solid rgba(0, 43, 127, 0.1);
    }
    
    .topic-card-enhanced:hover {
        transform: translateY(-6px);
        box-shadow: 0 8px 24px rgba(0, 43, 127, 0.15);
    }
    
    .topic-card-header {
        background: linear-gradient(135deg, #0072BC 0%, #005a9c 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .topic-number {
        background: rgba(255, 255, 255, 0.25);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .topic-card-header h3 {
        color: white !important;
        margin: 0;
        font-size: 1.1rem;
        font-weight: 700;
        line-height: 1.3;
    }
    
    .topic-card-body {
        padding: 1.5rem;
    }
    
    .topic-description {
        color: #555;
        line-height: 1.6;
        margin-bottom: 1.2rem;
        font-size: 0.95rem;
    }
    
    /* User Guidance Text */
    .view-guidance {
        background: linear-gradient(135deg, rgba(232, 119, 34, 0.08) 0%, rgba(232, 119, 34, 0.03) 100%);
        border-left: 4px solid #E87722;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(232, 119, 34, 0.1);
    }
    
    .view-guidance p {
        color: #002B7F;
        line-height: 1.7;
        margin: 0;
        font-size: 1.05rem;
        font-weight: 500;
    }
    
    /* Placeholder View */
    .placeholder-view {
        background: white;
        border-radius: 12px;
        padding: 4rem 2rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 2px dashed #E0E0E0;
    }
    
    /* View Definition Section */
    .view-definition {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.05) 0%, rgba(232, 119, 34, 0.05) 100%);
        border-left: 4px solid #002B7F;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .view-definition h4 {
        color: #002B7F;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        margin-top: 0;
    }
    
    .view-definition .definition-label {
        color: #002B7F;
        font-weight: 600;
        margin-bottom: 0.3rem;
        font-size: 0.95rem;
    }
    
    .view-definition .definition-text {
        color: #555;
        line-height: 1.7;
        margin-bottom: 1rem;
        font-size: 0.95rem;
    }
    
    .view-definition .purpose-label {
        color: #002B7F;
        font-weight: 600;
        margin-bottom: 0.3rem;
        font-size: 0.95rem;
    }
    
    .view-definition .purpose-text {
        color: #555;
        line-height: 1.7;
        margin: 0;
        font-size: 0.95rem;
    }
    
    /* View 3: Policy Brief Styling (OSAA Theme) */
    .policy-brief-header {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.05) 0%, rgba(232, 119, 34, 0.03) 100%);
        border-left: 5px solid #E87722;
        border-radius: 10px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .policy-brief-header h2 {
        color: #002B7F;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Streamlit Tabs Styling */
    div[data-baseweb="tab-list"] {
        background: white;
        border-radius: 10px 10px 0 0;
        padding: 0.5rem;
        margin-bottom: 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    button[data-baseweb="tab"] {
        background: transparent !important;
        color: #555 !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    button[data-baseweb="tab"]:hover {
        background: rgba(0, 43, 127, 0.05) !important;
        color: #002B7F !important;
    }
    
    button[aria-selected="true"][data-baseweb="tab"] {
        background: linear-gradient(135deg, #002B7F 0%, #003d99 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 43, 127, 0.2) !important;
    }
    
    /* Tab Content Styling */
    div[data-baseweb="tab-panel"] {
        background: white;
        border-radius: 0 0 10px 10px;
        padding: 2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin-top: 0;
    }
    
    /* Strategic Question Styling */
    .strategic-question {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%);
        border-left: 4px solid #002B7F;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .strategic-question h2 {
        color: #002B7F;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.4;
    }
    
    /* Thesis Statement Styling */
    div[data-testid="stInfo"] {
        background: linear-gradient(135deg, rgba(232, 119, 34, 0.1) 0%, rgba(232, 119, 34, 0.05) 100%) !important;
        border-left: 4px solid #E87722 !important;
        border-radius: 8px !important;
        padding: 1.2rem 1.5rem !important;
        margin-bottom: 2rem !important;
    }
    
    div[data-testid="stInfo"] > div {
        color: #002B7F !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    /* Evidence Block Styling - Standardized */
    .evidence-block {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-left: 4px solid #E87722;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .evidence-block h2 {
        color: #002B7F;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        margin-top: 0;
        line-height: 1.3;
    }
    
    .evidence-block h3 {
        color: #002B7F;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        margin-top: 0;
        line-height: 1.3;
    }
    
    .evidence-block p {
        color: #555;
        line-height: 1.7;
        margin-bottom: 1rem;
        font-size: 1rem;
    }
    
    /* Evidence Item Title - Standardized */
    .evidence-item-title {
        color: #002B7F;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    /* Graph Title - Standardized */
    .graph-title {
        color: #666;
        font-style: italic;
        font-size: 1rem;
        font-weight: 400;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Policy Synthesis Styling */
    .policy-synthesis {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.05) 0%, rgba(232, 119, 34, 0.03) 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 3px solid #E87722;
    }
    
    .policy-synthesis h3 {
        color: #002B7F;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        margin-top: 0;
    }
    
    .policy-synthesis ul {
        color: #555;
        line-height: 1.8;
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .policy-synthesis li {
        margin-bottom: 0.8rem;
    }
    
    .policy-synthesis strong {
        color: #002B7F;
        font-weight: 600;
    }
    
    .placeholder-view h3 {
        color: #002B7F;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .placeholder-view p {
        color: #777;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Footer */
    .theme-footer {
        background: linear-gradient(180deg, #F9FAFB 0%, #FFFFFF 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-top: 3px solid #E87722;
        text-align: center;
        margin-top: 3rem;
    }
    
    .theme-footer p {
        color: #555;
        margin: 0;
        line-height: 1.6;
    }
    
    /* Grid spacing */
    .stColumn {
        padding: 0.5rem;
    }
    
    /* Expander Styling - Make title more evident */
    [data-testid="stExpander"] {
        border: 2px solid #E87722 !important;
        border-radius: 8px !important;
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.05) 0%, rgba(232, 119, 34, 0.03) 100%) !important;
        margin-bottom: 1.5rem !important;
    }
    
    [data-testid="stExpander"] details {
        border: none !important;
    }
    
    [data-testid="stExpander"] summary {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%) !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 1.2rem 1.5rem !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #002B7F !important;
        cursor: pointer !important;
    }
    
    [data-testid="stExpander"] summary:hover {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.12) 0%, rgba(232, 119, 34, 0.08) 100%) !important;
        color: #E87722 !important;
    }
    
    [data-testid="stExpander"] summary::-webkit-details-marker {
        color: #E87722 !important;
        font-size: 1.2rem !important;
    }
    
    [data-testid="stExpander"] [data-baseweb="accordion"] {
        background: transparent !important;
    }
    
    /* Expander Content - Increased font size */
    [data-testid="stExpander"] [data-baseweb="accordion"] > div {
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
        color: #555 !important;
    }
    
    [data-testid="stExpander"] [data-baseweb="accordion"] p {
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
        color: #555 !important;
    }
    
    [data-testid="stExpander"] [data-baseweb="accordion"] ul,
    [data-testid="stExpander"] [data-baseweb="accordion"] ol {
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
        color: #555 !important;
    }
</style>
""", unsafe_allow_html=True)

# === PAGE CONTENT ===

# === 1. CONSOLIDATED TITLE AND NAVIGATION (Horizontal Layout) ===
# Home button styling - orange button with white text (top-left position)
# Match exact styling from navigation component
st.markdown("""
<style>
    /* Home Button Styling - Orange gradient design - Match navigation component exactly */
    a[href*="00_prototype_switcher"],
    a[href*="/pages/00_prototype_switcher"],
    a[href*="pages/00_prototype_switcher"],
    div[data-testid="stPageLink"] a[href*="00_prototype_switcher"],
    div[data-testid="stPageLink"] a[href*="/pages/00_prototype_switcher"],
    [data-testid="stPageLink"] a[href*="00_prototype_switcher"],
    div[data-baseweb="button"] a[href*="00_prototype_switcher"],
    .stPageLink a[href*="00_prototype_switcher"],
    .stPageLink a[href*="/pages/00_prototype_switcher"] {
        background: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
        background-color: #F26C2B !important;
        background-image: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-width: 0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.5px !important;
        text-decoration: none !important;
        padding: 0.7rem 1.8rem !important;
        border-radius: 30px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        box-shadow: 0 3px 10px rgba(242, 108, 43, 0.25), 
                    0 1px 3px rgba(0, 0, 0, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
        min-height: 44px !important;
        white-space: nowrap !important;
    }
    
    /* Ensure all nested text elements are white */
    a[href*="00_prototype_switcher"] *,
    a[href*="/pages/00_prototype_switcher"] *,
    a[href*="pages/00_prototype_switcher"] *,
    div[data-testid="stPageLink"] a[href*="00_prototype_switcher"] *,
    [data-testid="stPageLink"] a[href*="00_prototype_switcher"] * {
        color: #FFFFFF !important;
    }
    
    a[href*="00_prototype_switcher"]:hover,
    a[href*="/pages/00_prototype_switcher"]:hover,
    a[href*="pages/00_prototype_switcher"]:hover,
    div[data-testid="stPageLink"] a[href*="00_prototype_switcher"]:hover,
    [data-testid="stPageLink"] a[href*="00_prototype_switcher"]:hover {
        background: linear-gradient(135deg, #E85A1F 0%, #D1490F 100%) !important;
        background-color: #E85A1F !important;
        background-image: linear-gradient(135deg, #E85A1F 0%, #D1490F 100%) !important;
        color: #FFFFFF !important;
        text-decoration: none !important;
        box-shadow: 0 6px 20px rgba(242, 108, 43, 0.35), 
                    0 2px 6px rgba(0, 0, 0, 0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    a[href*="00_prototype_switcher"]:active,
    a[href*="/pages/00_prototype_switcher"]:active,
    a[href*="pages/00_prototype_switcher"]:active,
    div[data-testid="stPageLink"] a[href*="00_prototype_switcher"]:active,
    [data-testid="stPageLink"] a[href*="00_prototype_switcher"]:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 8px rgba(242, 108, 43, 0.3) !important;
    }
</style>
<script>
    // Aggressively style Home button - match navigation component approach
    function styleHomeLink() {
        // Find home link - try multiple selectors
        let homeLink = document.querySelector('a[href*="00_prototype_switcher"], a[href*="/pages/00_prototype_switcher"], a[href*="pages/00_prototype_switcher"]');
        if (!homeLink) {
            // Try finding by text content
            const allLinks = document.querySelectorAll('a');
            for (let link of allLinks) {
                if (link.textContent.trim() === 'Home' && (link.href.includes('00_prototype_switcher') || link.href.includes('prototype_switcher'))) {
                    homeLink = link;
                    break;
                }
            }
        }
        
        if (homeLink && homeLink.textContent.trim() === 'Home') {
            // Apply beautiful styling directly via JavaScript using cssText (more aggressive)
            homeLink.style.cssText = `
                background: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
                background-color: #F26C2B !important;
                background-image: linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-width: 0 !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                letter-spacing: 0.5px !important;
                text-decoration: none !important;
                padding: 0.7rem 1.8rem !important;
                border-radius: 30px !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                width: 100% !important;
                box-shadow: 0 3px 10px rgba(242, 108, 43, 0.25), 0 1px 3px rgba(0, 0, 0, 0.1) !important;
                position: relative !important;
                overflow: hidden !important;
                min-height: 44px !important;
                white-space: nowrap !important;
                gap: 0.5rem !important;
            `;
            
            // Ensure all nested elements are white
            const allElements = homeLink.querySelectorAll('*');
            allElements.forEach(el => {
                el.style.setProperty('color', '#FFFFFF', 'important');
            });
            
            // Add hover effect
            homeLink.addEventListener('mouseenter', function() {
                this.style.background = 'linear-gradient(135deg, #E85A1F 0%, #D1490F 100%)';
                this.style.boxShadow = '0 6px 20px rgba(242, 108, 43, 0.35), 0 2px 6px rgba(0, 0, 0, 0.15)';
                this.style.transform = 'translateY(-2px)';
            });
            homeLink.addEventListener('mouseleave', function() {
                this.style.background = 'linear-gradient(135deg, #F26C2B 0%, #E85A1F 100%)';
                this.style.boxShadow = '0 3px 10px rgba(242, 108, 43, 0.25), 0 1px 3px rgba(0, 0, 0, 0.1)';
                this.style.transform = 'translateY(0)';
            });
            
            // Ensure text content is "Home"
            if (homeLink.textContent.trim() !== 'Home') {
                const textNode = Array.from(homeLink.childNodes).find(n => n.nodeType === Node.TEXT_NODE);
                if (textNode) {
                    textNode.textContent = 'Home';
                } else {
                    homeLink.textContent = 'Home';
                }
            }
        }
    }
    
    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', styleHomeLink);
    } else {
        styleHomeLink();
    }
    
    // Also run after delays to catch dynamically added elements
    setTimeout(styleHomeLink, 100);
    setTimeout(styleHomeLink, 500);
    setTimeout(styleHomeLink, 1000);
    
    // Use MutationObserver to catch dynamically added elements
    const observer = new MutationObserver(function(mutations) {
        styleHomeLink();
    });
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# Home button row (above title)
home_col_left, home_col_right = st.columns([0.25, 3.75])
with home_col_left:
    st.page_link("pages/00_prototype_switcher.py", label="Home")

# Title and navigation row
title_col, nav_col = st.columns([2, 1])

with title_col:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <h1 style="color: #002B7F; font-size: 2.4rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.2;">
            Theme 4: Domestic Resource Mobilization (DRM)
        </h1>
        <p style="color: #555; font-size: 1.05rem; line-height: 1.7; margin: 0;">
            Institutions & Systems — Building robust financial frameworks for sustainable development through efficient resource management, transparent governance, and institutional capacity.
        </p>
    </div>
    """, unsafe_allow_html=True)

with nav_col:
    st.markdown("<div style='padding-top: 0.5rem;'>", unsafe_allow_html=True)
    # Navigation buttons in a vertical stack - reordered
    if st.button("1. Exploratory View", key="nav_1", use_container_width=True, type="primary" if st.session_state.current_view == 1 else "secondary"):
        st.session_state.current_view = 1
        st.rerun()
    
    if st.button("2. Explanatory View", key="nav_3", use_container_width=True, type="primary" if st.session_state.current_view == 3 else "secondary"):
        st.session_state.current_view = 3
        st.rerun()
    
    if st.button("3. View Evidence Process", key="nav_2", use_container_width=True, type="primary" if st.session_state.current_view == 2 else "secondary"):
        st.session_state.current_view = 2
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# === 2. UNDERSTANDING THE FRAMEWORK (Collapsed in Expander) ===
st.markdown("""
<style>
    /* Target Streamlit expander more aggressively */
    div[data-testid="stExpander"] {
        border: 2px solid #E87722 !important;
        border-radius: 8px !important;
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.05) 0%, rgba(232, 119, 34, 0.03) 100%) !important;
        margin-bottom: 1.5rem !important;
    }
    
    div[data-testid="stExpander"] > div {
        background: transparent !important;
    }
    
    div[data-testid="stExpander"] summary {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%) !important;
        padding: 1.2rem 1.5rem !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #002B7F !important;
        border-radius: 6px 6px 0 0 !important;
    }
    
    div[data-testid="stExpander"] summary:hover {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.12) 0%, rgba(232, 119, 34, 0.08) 100%) !important;
        color: #E87722 !important;
    }
    
    div[data-testid="stExpander"] p {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #002B7F !important;
    }
</style>
""", unsafe_allow_html=True)

with st.expander("Understanding the Framework", expanded=False):
    st.markdown("""
    <div style="font-size: 1.1rem; line-height: 1.8;">
    <strong>The Challenge (What):</strong> Countries have money, but it is not where it should be, it is not used as it should be, and does not benefit whom it should.
    <br><br>
    <strong>The Root Cause (Why):</strong> Institutional weaknesses in managing and capturing domestic financial resources.
    <br><br>
    <strong>The Solution (Therefore):</strong> Stronger ability to evaluate and manage domestic resources contributes to offering sustainable financial resources.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# === 3. CONDITIONAL CONTENT BASED ON SELECTED VIEW ===

if st.session_state.current_view == 1:
    # === VIEW 1: EXPLORATORY VIEW ===
    st.markdown("""
    <div class="view-definition">
        <h4>What is this view about?</h4>
        <div class="definition-label">Definition:</div>
        <div class="definition-text">Access raw, indicator-level data for all four topics.</div>
        <div class="purpose-label">Purpose:</div>
        <div class="purpose-text">Enable unfiltered data discovery and direct validation of the framework's Challenge and Root Cause.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
    <div class="view-guidance">
        <p>Use the dashboards below to drill into the indicators that provide evidence for the Challenge and Root Cause defined above.</p>
    </div>
    """, unsafe_allow_html=True)

    # Define topics data
    topics_config = [
    {
        "number": "4.1",
        "title": "Public Expenditures",
        "description": "Efficient management of public funds ensures that they are allocated toward priority sectors like education and infrastructure and are spent responsibly to avoid waste.",
        "route": "pages/3_topic_4_1.py",
        "key": "topic_4_1"
    },
    {
        "number": "4.3",
        "title": "Capital Markets",
        "description": "Well-developed capital markets channel savings into productive investments, promoting economic growth and reducing reliance on foreign financing.",
        "route": "pages/5_topic_4_3.py",
        "key": "topic_4_3"
    },
    {
        "number": "4.2",
        "title": "Budget and Tax Revenues",
        "description": "Strengthening tax administration and expanding the taxpayer base are critical for mobilizing domestic resources while minimizing revenue losses from inefficiencies.",
        "route": "pages/4_topic_4_2.py",
        "key": "topic_4_2"
    },
    {
        "number": "4.4",
        "title": "Illicit Financial Flows (IFFs)",
        "description": "Addressing IFFs helps retain domestic resources by curbing trade mispricing, tax evasion, and corruption, ensuring that financial resources stay within the country.",
        "route": "pages/6_topic_4_4.py",
        "key": "topic_4_4"
    }
    ]

    # Row 1
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        # Topic 4.1
        with col1:
            topic = topics_config[0]
            st.markdown(f"""
            <div class="topic-card-enhanced">
                <div class="topic-card-header">
                    <div class="topic-number">{topic['number']}</div>
                    <h3>{topic['title']}</h3>
                </div>
                <div class="topic-card-body">
                    <p class="topic-description">{topic['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore Topic {topic['number']}", key=topic['key'], use_container_width=True, type="primary"):
                st.switch_page(topic['route'])
        
        # Topic 4.3
        with col2:
            topic = topics_config[1]
            st.markdown(f"""
            <div class="topic-card-enhanced">
                <div class="topic-card-header">
                    <div class="topic-number">{topic['number']}</div>
                    <h3>{topic['title']}</h3>
                </div>
                <div class="topic-card-body">
                    <p class="topic-description">{topic['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore Topic {topic['number']}", key=topic['key'], use_container_width=True, type="primary"):
                st.switch_page(topic['route'])

    # Add spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2
    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        # Topic 4.2
        with col1:
            topic = topics_config[2]
            st.markdown(f"""
            <div class="topic-card-enhanced">
                <div class="topic-card-header">
                    <div class="topic-number">{topic['number']}</div>
                    <h3>{topic['title']}</h3>
                </div>
                <div class="topic-card-body">
                    <p class="topic-description">{topic['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore Topic {topic['number']}", key=topic['key'], use_container_width=True, type="primary"):
                st.switch_page(topic['route'])
        
        # Topic 4.4
        with col2:
            topic = topics_config[3]
            st.markdown(f"""
            <div class="topic-card-enhanced">
                <div class="topic-card-header">
                    <div class="topic-number">{topic['number']}</div>
                    <h3>{topic['title']}</h3>
                </div>
                <div class="topic-card-body">
                    <p class="topic-description">{topic['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore Topic {topic['number']}", key=topic['key'], use_container_width=True, type="primary"):
                st.switch_page(topic['route'])

elif st.session_state.current_view == 2:
    # === VIEW 2: LOGIC VIEW (View Evidence Process) ===
    
    # === SECTION 1: THE ANALYTICAL JOURNEY ===
    st.markdown("### From Data to Policy: The DRM Journey")
    
    # Custom styling for the journey diagram
    st.markdown("""
    <style>
    .journey-container {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.02) 0%, rgba(232, 119, 34, 0.01) 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    .journey-box {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 43, 127, 0.08);
        height: 100%;
        position: relative;
    }
    .journey-box-exploratory {
        border-top: 2px solid #E87722;
        border-right: 2px solid #E87722;
        border-bottom: 2px solid #002B7F;
        border-left: 2px solid #002B7F;
    }
    .journey-box-explanatory {
        border-top: 2px solid #002B7F;
        border-right: 2px solid #002B7F;
        border-bottom: 2px solid #E87722;
        border-left: 2px solid #E87722;
    }
    .journey-title {
        color: #002B7F;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E87722;
    }
    .journey-arrow-container {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        min-height: 300px;
        position: relative;
        padding: 0 0.5rem;
    }
    .journey-arrow-main {
        width: 60%;
        height: 8px;
        background: #E87722;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        border-radius: 4px;
    }
    .journey-arrow-main::after {
        content: '';
        position: absolute;
        right: -18px;
        top: 50%;
        transform: translateY(-50%);
        width: 0;
        height: 0;
        border-left: 18px solid #E87722;
        border-top: 12px solid transparent;
        border-bottom: 12px solid transparent;
        z-index: 1;
    }
    .journey-step-label {
        color: #002B7F;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .journey-bullet {
        color: #002B7F;
        margin-right: 0.5rem;
    }
    .journey-question {
        color: #E87722;
        font-style: italic;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    .example-box {
        background: white;
        border: 2px solid #E87722;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 43, 127, 0.08);
        height: 100%;
    }
    .example-box-exploratory {
        border-left: 5px solid #002B7F;
    }
    .example-box-explanatory {
        border-left: 5px solid #E87722;
    }
    .example-title {
        color: #002B7F;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E87722;
    }
    .example-arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        min-height: 300px;
        font-size: 2.5rem;
        color: #E87722;
        font-weight: bold;
    }
    .example-synthesis {
        color: #555;
        font-style: italic;
        margin: 0.75rem 0;
        padding: 0.75rem;
        background: rgba(232, 119, 34, 0.05);
        border-left: 3px solid #E87722;
        border-radius: 4px;
    }
    .example-implication {
        color: #002B7F;
        font-weight: 600;
        margin-top: 1rem;
    }
    .example-link {
        color: #E87722;
        text-decoration: none;
        font-weight: 600;
        margin-top: 1rem;
        display: inline-block;
    }
    .example-link:hover {
        color: #002B7F;
        text-decoration: underline;
    }
    .entry-point-card {
        background: white;
        border: 2px solid #E87722;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 43, 127, 0.08);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .entry-point-title {
        color: #002B7F;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    .entry-point-desc {
        color: #555;
        margin-bottom: 1rem;
        font-size: 0.95rem;
    }
    .entry-point-list {
        color: #555;
        line-height: 1.8;
        margin: 0.5rem 0 1rem 0;
        flex-grow: 1;
    }
    .entry-point-list-item {
        margin-bottom: 0.5rem;
    }
    .entry-point-here {
        background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.06) 100%);
        border: 2px solid #002B7F;
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        color: #002B7F;
        font-weight: 600;
        margin-top: auto;
    }
    .example-summary {
        text-align: center;
        color: #555;
        font-style: italic;
        margin-top: 1.5rem;
        padding: 1rem;
        background: rgba(0, 43, 127, 0.03);
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="journey-container">', unsafe_allow_html=True)
        
        # Header row with step labels
        col_step1_label, col_spacer, col_step2_label = st.columns([2, 0.5, 2], gap="medium")
        
        with col_step1_label:
            st.markdown('<div class="journey-step-label">Step 1: Explore</div>', unsafe_allow_html=True)
        
        with col_step2_label:
            st.markdown('<div class="journey-step-label">Step 2: Synthesize</div>', unsafe_allow_html=True)
        
        # Main content row
        col_step1, col_arrow, col_step2 = st.columns([2, 0.5, 2], gap="medium")
        
        with col_step1:
            st.markdown("""
            <div class="journey-box journey-box-exploratory">
                <div class="journey-title">Exploratory View</div>
                <p style="color: #555; margin-bottom: 1rem;"><strong>Purpose:</strong> Validate framework assumptions with raw data</p>
                <p style="color: #555; margin-bottom: 0.5rem;"><strong>What you do:</strong></p>
                <ul style="color: #555; line-height: 1.8; margin-left: 1.2rem;">
                    <li><span class="journey-bullet">•</span> Filter countries</li>
                    <li><span class="journey-bullet">•</span> Compare years</li>
                    <li><span class="journey-bullet">•</span> Test hypotheses</li>
                    <li><span class="journey-bullet">•</span> Export findings</li>
                </ul>
                <p class="journey-question" style="margin-top: 1rem;">"How shallow ARE African markets?"</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_arrow:
            st.markdown("""
            <div class="journey-arrow-container">
                <div class="journey-arrow-main"></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_step2:
            st.markdown("""
            <div class="journey-box journey-box-explanatory">
                <div class="journey-title">Explanatory View</div>
                <p style="color: #555; margin-bottom: 1rem;"><strong>Purpose:</strong> Answer strategic policy questions with evidence</p>
                <p style="color: #555; margin-bottom: 0.5rem;"><strong>What you get:</strong></p>
                <ul style="color: #555; line-height: 1.8; margin-left: 1.2rem;">
                    <li><span class="journey-bullet">•</span> Pre-filtered data</li>
                    <li><span class="journey-bullet">•</span> Strategic framing</li>
                    <li><span class="journey-bullet">•</span> Interpretation</li>
                    <li><span class="journey-bullet">•</span> Recommendations</li>
                </ul>
                <p class="journey-question" style="margin-top: 1rem;">"CAN markets finance development?"</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    st.info("**Key Insight:** Every graph in the Explanatory View is built from patterns discovered and validated in the Exploratory View")
    
    # === SECTION 2: CONCRETE EXAMPLE ===
    st.markdown("---")
    st.markdown("### Concrete Example: How Market Capitalization Analysis Becomes Policy Insight")
    
    st.markdown("**Indicator: 4.3.1.1 - Market Capitalization to GDP**")
    st.markdown("")
    
    col_explore_ex, col_arrow_ex, col_synthesize_ex = st.columns([2, 0.3, 2], gap="medium")
    
    with col_explore_ex:
        st.markdown("""
        <div class="example-box example-box-exploratory">
            <div class="example-title">In Exploratory View</div>
            <p style="color: #555; margin-bottom: 0.75rem;"><strong>You discover:</strong></p>
            <ol style="color: #555; line-height: 1.8; margin-left: 1.2rem; padding-left: 0.5rem;">
                <li style="margin-bottom: 0.5rem;">Select "All African countries"</li>
                <li style="margin-bottom: 0.5rem;">Filter 2015-2023</li>
                <li style="margin-bottom: 0.5rem;">See median = 23% of GDP</li>
                <li style="margin-bottom: 0.5rem;">Compare to global benchmark: 120%</li>
                <li style="margin-bottom: 0.5rem;">Export data table for verification</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col_arrow_ex:
        st.markdown('<div class="example-arrow">→</div>', unsafe_allow_html=True)
    
    with col_synthesize_ex:
        st.markdown("""
        <div class="example-box example-box-explanatory">
            <div class="example-title">In Explanatory View</div>
            <p style="color: #555; margin-bottom: 0.75rem;"><strong>We synthesize:</strong></p>
            <div class="example-synthesis">
                "African markets remain shallow: median market cap is 23% of GDP vs 120% in developed economies."
            </div>
            <p class="example-implication">→ Policy implication:</p>
            <p style="color: #555; margin-bottom: 1rem;">Cannot rely on domestic capital markets alone</p>
            <a href="#" class="example-link">[See full evidence] →</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="example-summary">
        <strong>The exact same data, the exact same calculation function, but different contexts and conclusions</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # === SECTION 3: THE TECHNICAL BRIDGE ===
    st.markdown("---")
    st.markdown("### How the Views Share Code and Data")
    
    with st.expander("Show technical details", expanded=False):
        st.markdown("#### 1. Same Data Source")
        st.markdown("Both views query: `df_main + ref_data`")
        if DATA_AVAILABLE:
            try:
                view2_ref_data = uv.load_country_reference_data()
                view2_df_main = uv.load_main_data()
                st.markdown(f"{len(view2_df_main):,} rows | {view2_df_main['indicator_label'].nunique():,} indicators | {view2_df_main['country_or_area'].nunique():,} countries" if not view2_df_main.empty else "616,409 rows | 457 indicators | 239 countries")
            except:
                st.markdown("616,409 rows | 457 indicators | 239 countries")
        else:
            st.markdown("616,409 rows | 457 indicators | 239 countries")
        
        st.markdown("")
        st.markdown("#### 2. Same Calculation Functions")
        st.markdown("`render_indicator_4311()` ← Used in BOTH views")
        st.markdown("- Loads same data")
        st.markdown("- Applies same formula: (Market Cap / GDP) × 100")
        st.markdown("- Generates same chart type")
        
        st.markdown("")
        st.markdown("#### 3. Different Presentation Layers")
        
        col_pres_exploratory, col_pres_explanatory = st.columns(2, gap="large")
        
        with col_pres_exploratory:
            st.markdown("**Exploratory:**")
            st.markdown("- User controls filters")
            st.markdown("- Full date range slider")
            st.markdown("- Multiple chart options")
            st.markdown("- No guidance text")
            st.markdown("- Raw table export")
        
        with col_pres_explanatory:
            st.markdown("**Explanatory:**")
            st.markdown("- Pre-filtered (Africa, latest)")
            st.markdown("- Strategic question framing")
            st.markdown("- Narrative interpretation")
            st.markdown("- Policy recommendations")
            st.markdown("- Link to full interactive")
        
        st.markdown("")
        st.markdown("#### 4. Traceability Guarantee")
        st.markdown("Every Explanatory View chart has a \"View in Exploratory\" link that takes you to the exact same indicator with full controls")
    
    # === SECTION 4: YOUR PATH FORWARD ===
    st.markdown("---")
    st.markdown("### Choose Your Entry Point")
    st.markdown("**I want to...**")
    
    col_path1, col_path2, col_path3 = st.columns(3, gap="large")
    
    with col_path1:
        st.markdown("""
        <div class="entry-point-card">
            <div class="entry-point-title">Explore the data myself</div>
            <p class="entry-point-desc">Start with the Exploratory View</p>
            <ul class="entry-point-list">
                <li class="entry-point-list-item">→ Pick a topic below (4.1, 4.2, 4.3, 4.4)</li>
                <li class="entry-point-list-item">→ Filter, compare, validate your hypotheses</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Exploratory View", key="path_explore", use_container_width=True, type="primary"):
            st.session_state.current_view = 1
            st.rerun()
    
    with col_path2:
        st.markdown("""
        <div class="entry-point-card">
            <div class="entry-point-title">Understand the policy implications</div>
            <p class="entry-point-desc">Start with the Explanatory View (Policy Brief)</p>
            <ul class="entry-point-list">
                <li class="entry-point-list-item">→ Read strategic question framing</li>
                <li class="entry-point-list-item">→ Review synthesized evidence</li>
                <li class="entry-point-list-item">→ Click through to explore underlying data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Policy Brief", key="path_policy", use_container_width=True, type="primary"):
            st.session_state.current_view = 3
            st.rerun()
    
    with col_path3:
        st.markdown("""
        <div class="entry-point-card">
            <div class="entry-point-title">Understand the methodology</div>
            <p class="entry-point-desc">See how we built this system</p>
            <ul class="entry-point-list">
                <li class="entry-point-list-item">→ View data sources and ETL pipeline</li>
                <li class="entry-point-list-item">→ Check indicator calculation logic</li>
                <li class="entry-point-list-item">→ Review quality and coverage stats</li>
            </ul>
            <div class="entry-point-here">You are here</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_view == 3:
    # === VIEW 3: EXPLANATORY VIEW ===
    st.markdown("""
    <div class="view-definition">
        <h4>What is this view about?</h4>
        <div class="definition-label">Definition:</div>
        <div class="definition-text">Synthesis of data to answer a high-level strategic policy question.</div>
        <div class="purpose-label">Purpose:</div>
        <div class="purpose-text">Provide actionable conclusions and policy recommendations, fulfilling The Solution.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initial Header
    st.markdown("""
    <div class="policy-brief-header">
        <h2>Policy Brief: Strategic Insights from DRM Data</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Implement Tabbed Navigation
    tab_cm, tab_iff = st.tabs(["Capital Markets (Topic 4.3)", "Illicit Flows (Topic 4.4)"])
    
    # Tab 1: Capital Markets (Topic 4.3)
    with tab_cm:
        # Strategic Question
        st.markdown("""
        <div class="strategic-question">
            <h2>Strategic Question: Can Africa's domestic capital markets truly finance sustainable development, or is external reliance structural?</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Thesis Statement
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%); border-left: 5px solid #002B7F; border-radius: 10px; padding: 1.5rem; margin: 1.5rem 0;">
            <h3 style="color: #002B7F; margin-top: 0; margin-bottom: 1rem;">Thesis Statement</h3>
            <p style="color: #555; line-height: 1.7; margin: 0; font-size: 1.05rem;">Africa's domestic capital markets cannot yet replace external finance as a primary engine for sustainable development, because shallow and volatile markets, weak banking intermediation, and conservative institutional investors keep long-term capital scarce and pro-cyclical; external reliance is therefore structural for now, but can be reduced if these system weaknesses are addressed in a coordinated Solution across expenditures, revenues and IFFs.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Evidence Block 1 – Market Depth and Stability: The Challenge
        st.markdown("""
        <div class="evidence-block">
            <h2>Evidence Block 1 – Market Depth and Stability: The Challenge</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h2 class="evidence-item-title">1. Equity market depth is thin and volatile (Indicator 4.3.1.1: Market Capitalization to GDP)</h2>
        """, unsafe_allow_html=True)
        st.markdown("""
        <h4 class="graph-title">Indicator 4.3.1.1 – Market Capitalization to GDP</h4>
        """, unsafe_allow_html=True)
        render_indicator_4311()
        
        st.markdown("""
        <p>The market-capitalisation chart shows three key patterns:</p>
        <ul>
            <li>Most markets sit in the "shallow" or lower "developing" range (0–40% of GDP). Only a handful of countries (e.g. Botswana, Mauritius, Morocco) occasionally cross into the "deep" band above 60% of GDP, and these peaks are not sustained.</li>
            <li>The Africa regional average stays below the 60% "deep market" threshold throughout the period, and often closer to 20–40%.</li>
            <li>Equity values are highly sensitive to shocks: the commodity-price downturn (2014–2016) and COVID-19 (2020) coincide with visible dips in market capitalisation.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 43, 127, 0.05) 0%, rgba(232, 119, 34, 0.03) 100%); padding: 1rem; border-left: 4px solid #002B7F; border-radius: 8px; margin: 1rem 0;">
            <p style="margin: 0; color: #002B7F; font-weight: 600;">Implication for the Challenge</p>
            <p style="margin: 0.5rem 0 0 0;">Domestic equity markets do not yet provide broad, reliable access to long-term capital. Large issuances by governments or firms can easily move prices and liquidity, which makes these markets risky as a primary financing source for long-term infrastructure or climate investments.</p>
            <p style="margin: 0.5rem 0 0 0;">The volatility around global shocks shows that, when external conditions tighten, domestic markets often shrink rather than counter-act the shock.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h2 class="evidence-item-title">2. External bond flows are episodic and concentrated (Indicator 4.3.1.2: Portfolio Investment Bonds)</h2>
        """, unsafe_allow_html=True)
        st.markdown("""
        <h4 class="graph-title">Indicator 4.3.1.2 – Portfolio Investment Bonds</h4>
        """, unsafe_allow_html=True)
        render_indicator_4312()
        
        st.markdown("""
        <p>The normalised heatmap of portfolio bond flows reveals that:</p>
        <ul>
            <li>Bond inflows are highly concentrated in time and country: a few countries (such as South Africa, Egypt, Nigeria, Ghana, Kenya, Morocco) show deep blue cells in selected years, while many others show very little activity or sporadic single-year spikes.</li>
            <li>There is no continuous, stable pattern of portfolio bond financing across the region; instead, inflows cluster in "windows" (e.g. mid-2010s), followed by quieter periods.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 43, 127, 0.05) 0%, rgba(232, 119, 34, 0.03) 100%); padding: 1rem; border-left: 4px solid #002B7F; border-radius: 8px; margin: 1rem 0;">
            <p style="margin: 0; color: #002B7F; font-weight: 600;">Implication for the Challenge</p>
            <p style="margin: 0.5rem 0 0 0;">Although international investors occasionally channel large volumes into African bonds, these flows are pro-cyclical and reversible, not a stable base of long-term finance.</p>
            <p style="margin: 0.5rem 0 0 0;">Countries that try to rely heavily on such portfolio flows risk sudden stops and refinancing stress, reinforcing the structural dependence on external sentiment.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h2 class="evidence-item-title">3. External resilience is limited (Indicator 4.3.1.3: Adequacy of International Reserves)</h2>
        """, unsafe_allow_html=True)
        st.markdown("""
        <h4 class="graph-title">Indicator 4.3.1.3 – Adequacy of International Reserves</h4>
        """, unsafe_allow_html=True)
        render_indicator_4313()
        
        st.markdown("""
        <p>The reserve-adequacy snapshot (reserves / short-term external debt) shows:</p>
        <ul>
            <li>Many countries fall short of the "full coverage" benchmark of 1.0; several have ratios near or below zero once normalised, signalling very weak coverage.</li>
            <li>Only a small group has reserve buffers clearly above short-term debt.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 43, 127, 0.05) 0%, rgba(232, 119, 34, 0.03) 100%); padding: 1rem; border-left: 4px solid #002B7F; border-radius: 8px; margin: 1rem 0;">
            <p style="margin: 0; color: #002B7F; font-weight: 600;">Implication for the Challenge</p>
            <p style="margin: 0.5rem 0 0 0;">When global conditions tighten, countries with low reserve adequacy cannot easily smooth shocks or roll over external obligations.</p>
            <p style="margin: 0.5rem 0 0 0;">This heightens the risk that attempts to deepen domestic capital markets via external portfolio participation will amplify vulnerability rather than reduce it.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; border: 2px solid #E87722; border-radius: 10px; padding: 1.5rem; margin: 2rem 0;">
            <p style="margin: 0; color: #002B7F; font-weight: 700; font-size: 1.1rem;">Taken together, Indicators 4.3.1.1–4.3.1.3 show a clear Challenge:</p>
            <p style="margin: 0.5rem 0 0 0; color: #555; line-height: 1.7;">Africa's capital markets remain shallow and shock-prone, and are embedded in macro-financial settings where external volatility can quickly spill back into domestic financing conditions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Evidence Block 2 – Domestic Intermediation and Institutional Investors: The Root Cause
        st.markdown("""
        <div class="evidence-block">
            <h2>Evidence Block 2 – Domestic Intermediation and Institutional Investors: The Root Cause</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h2 class="evidence-item-title">4. Banking systems are only moderately developed (Indicator 4.3.2.1: Banking Sector Development Index)</h2>
        """, unsafe_allow_html=True)
        st.markdown("""
        <h4 class="graph-title">Indicator 4.3.2.1 – Banking Sector Development Index</h4>
        """, unsafe_allow_html=True)
        render_indicator_4321()
        
        st.markdown("""
        <p>The Banking Sector Development Index (0–1 scale) highlights that:</p>
        <ul>
            <li>The Africa regional average sits in the "moderate development" band (0.4–0.7), not in the "high development" zone above 0.7.</li>
            <li>Several large economies (e.g. Angola, South Africa, Uganda) remain in the lower half of the moderate or even "weak" range, with limited improvement over time.</li>
            <li>Only a few countries approach the upper part of the moderate band.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(232, 119, 34, 0.08) 0%, rgba(232, 119, 34, 0.03) 100%); padding: 1rem; border-left: 4px solid #E87722; border-radius: 8px; margin: 1rem 0;">
            <p style="margin: 0; color: #E87722; font-weight: 600;">Implication for the Root Cause</p>
            <p style="margin: 0.5rem 0 0 0;">Banking systems provide basic intermediation but not deep, diversified financial services that can reliably support complex, long-term investments.</p>
            <p style="margin: 0.5rem 0 0 0;">Regulatory and supervisory capacity is often stretched, which constrains banks' ability to manage longer-maturity, higher-risk assets such as infrastructure loans or green projects.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h2 class="evidence-item-title">5. Private-sector credit is shallow outside a few outliers (Indicator 4.3.2.2: Private Sector Credit to GDP)</h2>
        """, unsafe_allow_html=True)
        st.markdown("""
        <h4 class="graph-title">Indicator 4.3.2.2 – Private Sector Credit to GDP</h4>
        """, unsafe_allow_html=True)
        render_indicator_4322()
        
        st.markdown("""
        <p>The Domestic Credit Provided by the Financial Sector (% of GDP) graph shows:</p>
        <ul>
            <li>The regional average rises over time and sits in the "moderate to deep" band largely because of a few large, credit-intensive systems.</li>
            <li>Many individual countries remain in the "shallow systems" band below 40% of GDP, with only gradual increases.</li>
            <li>Where credit is higher, it is often concentrated in a few sectors and tilted towards short-term and government-linked lending.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(232, 119, 34, 0.08) 0%, rgba(232, 119, 34, 0.03) 100%); padding: 1rem; border-left: 4px solid #E87722; border-radius: 8px; margin: 1rem 0;">
            <p style="margin: 0; color: #E87722; font-weight: 600;">Implication for the Root Cause</p>
            <p style="margin: 0.5rem 0 0 0;">For most countries, private firms—especially SMEs and new green sectors—face tight credit constraints.</p>
            <p style="margin: 0.5rem 0 0 0;">Even where total credit is large, its composition often reflects short-term lending and sovereign exposure, not diversified long-term project finance.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h2 class="evidence-item-title">6. Institutional capital is large but conservatively deployed (Sub-topic 4.3.3.1: Pension Funds and Sovereign Wealth Funds Investments)</h2>
        """, unsafe_allow_html=True)
        st.markdown("""
        <h4 class="graph-title">Sub-topic 4.3.3.1 – Pension Funds and Sovereign Wealth Funds Investments</h4>
        """, unsafe_allow_html=True)
        
        # Note: This indicator is primarily text-based analysis in the exploratory view
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #E87722;">
            <p style="margin: 0; color: #002B7F; font-weight: 600; margin-bottom: 0.5rem;">Analysis: Pension Fund Asset Class Mix by Country</p>
            <p style="margin: 0; font-size: 0.9rem; color: #666;">This sub-topic provides detailed text-based analysis of pension fund asset allocation across government bonds, equities, infrastructure, real estate, and private equity. View the detailed analysis in <a href="pages/5_topic_4_3.py" target="_blank" style="color: #E87722; font-weight: 600;">Exploratory View → Topic 4.3 → Sub-topic 4.3.3</a></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <p>The key-indicator text and the pension-fund asset-mix chart show that:</p>
        <ul>
            <li>Around 92% of pension-fund assets are concentrated in just a few countries (South Africa, Nigeria, Kenya, Namibia, Botswana).</li>
            <li>Asset allocation is dominated by domestic government bonds and listed equities; allocations to infrastructure, real estate and private equity are visible but still small.</li>
            <li>Foreign assets play only a minor role, and regulatory frameworks remain conservative, though some reforms (e.g. in Zambia and Nigeria) are opening space for co-investment.</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(232, 119, 34, 0.08) 0%, rgba(232, 119, 34, 0.03) 100%); padding: 1rem; border-left: 4px solid #E87722; border-radius: 8px; margin: 1rem 0;">
            <p style="margin: 0; color: #E87722; font-weight: 600;">Implication for the Root Cause</p>
            <p style="margin: 0.5rem 0 0 0;">A potentially powerful pool of long-term domestic savings is "parked" in low-risk, liquid assets, often government debt.</p>
            <p style="margin: 0.5rem 0 0 0;">This reflects a combination of prudential rules, limited bankable projects, governance concerns, and shallow capital-market instruments, rather than an absolute lack of savings.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; border: 2px solid #E87722; border-radius: 10px; padding: 1.5rem; margin: 2rem 0;">
            <p style="margin: 0; color: #002B7F; font-weight: 700; font-size: 1.1rem;">Overall, these indicators highlight the Root Cause:</p>
            <p style="margin: 0.5rem 0 0 0; color: #555; line-height: 1.7;">Domestic financial systems and institutional investors are present but structurally conservative and shallow. They are not yet designed or incentivised to channel savings into long-term, transformative investment at scale.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Policy Synthesis & Linkage – The Solution
        st.markdown('<div class="policy-synthesis"><h3>Policy Synthesis & Linkage – The Solution</h3><p style="color: #555; line-height: 1.7; margin-bottom: 1.5rem;">To reduce structural external reliance and make domestic capital markets a credible pillar of sustainable development finance, reforms must tackle both the Challenge (shallow, volatile markets) and the Root Cause (conservative intermediation and investment behaviour). This requires coordinated action across all Theme 4 topics.</p></div>', unsafe_allow_html=True)
        
        # Render list using HTML string directly
        policy_html = '''
        <div class="policy-synthesis">
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 1rem;">
                    <strong style="color: #002B7F;">1. Use public expenditure quality to create investable pipelines (Topic 4.1 × 4.3)</strong><br>
                    <span style="margin-left: 1.5rem; display: block; margin-top: 0.5rem;">
                        Strengthen public investment management and budget credibility so that infrastructure and climate projects come with transparent costings, clear risk-sharing, and predictable payment streams.<br>
                        Package priority projects into standardised, investment-ready vehicles (e.g. infrastructure bonds, green bonds, PPP structures) that banking systems and pension funds can realistically buy, given their risk limits and capacity.
                    </span>
                </li>
                <li style="margin-bottom: 1rem;">
                    <strong style="color: #002B7F;">2. Broaden and stabilise revenue to avoid crowding out (Topic 4.2 × 4.3)</strong><br>
                    <span style="margin-left: 1.5rem; display: block; margin-top: 0.5rem;">
                        Improve tax administration and base-broadening so revenues are more predictable, reducing reliance on short-term domestic borrowing that crowds banks and pension funds into government paper.<br>
                        As revenue stabilises, re-profile debt toward longer maturities and more diversified instruments, freeing room for private-sector borrowers and lowering the risk that domestic markets seize up during shocks.
                    </span>
                </li>
                <li style="margin-bottom: 1rem;">
                    <strong style="color: #002B7F;">3. Re-align prudential rules with development objectives (Core Topic 4.3)</strong><br>
                    <span style="margin-left: 1.5rem; display: block; margin-top: 0.5rem;">
                        Gradually update investment regulations so that a prudent share of pension and insurance portfolios can be invested in domestic infrastructure, sustainable agriculture, and green industrialisation—backed by risk-based supervision rather than blunt asset-class caps.<br>
                        Encourage pooled and blended vehicles (regional infrastructure funds, credit-enhanced green bonds, guarantee facilities) that allow institutional investors to diversify, while leveraging concessional finance to absorb first-loss risk.
                    </span>
                </li>
                <li style="margin-bottom: 1rem;">
                    <strong style="color: #002B7F;">4. Deepen banking-sector capacity and resilience (4.3.2 × 4.3.1)</strong><br>
                    <span style="margin-left: 1.5rem; display: block; margin-top: 0.5rem;">
                        Invest in bank supervision, resolution frameworks and credit-information systems, raising the Banking Sector Development Index over time.<br>
                        Promote instruments that lengthen bank funding tenors (e.g. term deposits, local-currency bond issuance by banks) so banks can responsibly extend longer-maturity credit to the private sector.<br>
                        Use macro-prudential tools to prevent excessive sovereign exposure and to incentivise banks to diversify lending toward productive, climate-resilient sectors.
                    </span>
                </li>
                <li style="margin-bottom: 1rem;">
                    <strong style="color: #002B7F;">5. Plug leakages to increase on-shore savings (Topic 4.4 × 4.3)</strong><br>
                    <span style="margin-left: 1.5rem; display: block; margin-top: 0.5rem;">
                        Strengthen Illicit Financial Flows (IFF) controls—trade mispricing detection, beneficial-ownership transparency, and AML enforcement—to keep more savings onshore and protect the integrity of capital markets.<br>
                        Coordinate FIUs, tax authorities and market regulators so that suspicious capital-market transactions are quickly identified and acted on, reinforcing investor confidence and reducing reputational risk.
                    </span>
                </li>
            </ul>
        </div>
        '''
        st.markdown(policy_html, unsafe_allow_html=True)
        
        # Conclusion
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%); border-left: 5px solid #002B7F; border-radius: 10px; padding: 1.5rem; margin-top: 2rem;">
            <h3 style="color: #002B7F; margin-top: 0; margin-bottom: 1rem;">Conclusion</h3>
            <p style="color: #555; line-height: 1.7; margin: 0;">Africa's domestic capital markets are not yet deep or stable enough to independently finance sustainable development, and external reliance remains structural. However, the indicators show that the constraint is not an absolute lack of savings, but a system in which shallow markets, moderate banking development and conservative institutional investors limit the translation of existing savings into long-term investment. A coherent Solution—linking expenditure quality, revenue stability, capital-market regulation and IFF controls—can gradually shift this structure so that domestic markets become a stronger, more reliable complement to external finance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tab 2: Illicit Flows (Topic 4.4)
    with tab_iff:
        # Strategic Question
        st.markdown("""
        <div class="strategic-question">
            <h2>Strategic Question: Is the primary vulnerability in Africa's anti-IFF efforts a failure to detect flows or a failure to prevent large-scale commercial leakage?</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Thesis Statement
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%); border-left: 5px solid #002B7F; border-radius: 10px; padding: 1.5rem; margin: 1.5rem 0;">
            <h3 style="color: #002B7F; margin-top: 0; margin-bottom: 1rem;">Thesis Statement</h3>
            <p style="color: #555; line-height: 1.7; margin: 0; font-size: 1.05rem;">Africa's primary vulnerability is the massive scale of commercial and criminal leakage—especially Trade Mispricing—which consistently overwhelms existing institutional capacity for detection and enforcement. The Challenge lies in the dominance and persistence of these commercial IFF channels, while the Root Cause is weak, under-resourced detection and enforcement systems that cannot keep pace with them.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Evidence Block 1 – Channels of IFFs and the Challenge
        st.markdown("""
        <div class="evidence-block" style="margin-top: 2rem;">
            <h2>Evidence Block 1 – Channels of IFFs and the Challenge</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 1. Trade Mispricing
        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <h2 class="evidence-item-title">1. Trade Mispricing as the dominant channel (4.4.2.1 – Trade Mispricing)</h2>
            <p style="color: #555; line-height: 1.8; margin-bottom: 1rem;">The Channels of IFFs graph is structured to show the relative size of each channel:</p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;"><strong>Trade Mispricing (4.4.2.1)</strong>—typically the largest bar—captures losses arising from deliberate under- or over-invoicing and misclassification of imports and exports.</li>
                <li style="margin-bottom: 0.75rem;">It is often concentrated in extractive industries and high-value trade flows, where under-reported volumes or prices can shift very large amounts of value offshore.</li>
                <li style="margin-bottom: 0.75rem;">Across Africa, multiple studies indicate that trade mispricing alone accounts for a majority share of total estimated IFFs, dwarfing many other channels. This aligns with the AU/ECA High-Level Panel and UNCTAD findings that commercial practices related to trade and tax are the single biggest source of outflows.</li>
            </ul>
            <div style="background: rgba(0, 43, 127, 0.05); border-left: 4px solid #002B7F; padding: 1rem; margin-top: 1rem; border-radius: 5px;">
                <p style="color: #555; line-height: 1.7; margin: 0;"><strong style="color: #002B7F;">Interpretation – The Challenge (What):</strong> This indicator is used because it directly answers the question: "Where is most of the money leaking?" By focusing on trade mispricing, the graph shows that the primary Challenge is not isolated corruption scandals but structural commercial behaviour, embedded in normal trade transactions. The visual dominance of the Trade Mispricing bar makes clear that the money is not where it should be: it is being quietly shifted offshore through under-invoicing, misclassification, and profit-shifting in global value chains.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Graph placeholder for Trade Mispricing - will be replaced with actual graph
        st.markdown("""
        <div style="margin: 1rem 0;">
            <p style="color: #888; font-style: italic; margin-bottom: 0.5rem;">Navigate to Exploratory View → Topic 4.4 → Sub-topic 4.4.2 → 4.4.2.1 – Trade Mispricing</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h4 class="graph-title">Indicator 4.4.2.1 – Trade Mispricing</h4>
        """, unsafe_allow_html=True)
        render_indicator_4421()
        
        # Navigation button
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        with col_nav2:
            if st.button("View full interactive version", key="nav_4421", use_container_width=True):
                st.switch_page("pages/6_topic_4_4.py")
        
        st.markdown("---")
        
        # 2. Tax Evasion
        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <h2 class="evidence-item-title">2. Commercial tax practices and evasion (4.4.2.2 – Tax Evasion and Aggressive Tax Planning)</h2>
            <p style="color: #555; line-height: 1.8; margin-bottom: 1rem;">A second component of commercial IFFs in the Channels graph is Tax Evasion and Aggressive Tax Practices (4.4.2.2):</p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">This captures revenue lost through deliberate non-compliance (e.g. false declarations) and strategic tax planning that exploits loopholes and gaps in international tax rules.</li>
                <li style="margin-bottom: 0.75rem;">It is particularly relevant for multinational enterprises in sectors such as mining, telecoms, and finance, where complex group structures make it easier to shift profits to low-tax jurisdictions.</li>
            </ul>
            <div style="background: rgba(0, 43, 127, 0.05); border-left: 4px solid #002B7F; padding: 1rem; margin-top: 1rem; border-radius: 5px;">
                <p style="color: #555; line-height: 1.7; margin: 0;"><strong style="color: #002B7F;">Interpretation – The Challenge:</strong> This indicator is used to show that the commercial Challenge is broader than trade invoices alone; it includes how firms organise their tax affairs across borders. Together with Trade Mispricing, it demonstrates that commercial and tax-related channels form the core of Africa's IFF problem, confirming that policy must prioritise these areas rather than treat them as residual issues.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0;">
            <p style="color: #888; font-style: italic; margin-bottom: 0.5rem;">Navigate to Exploratory View → Topic 4.4 → Sub-topic 4.4.2 → 4.4.2.2 – Tax Evasion</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h4 class="graph-title">Indicator 4.4.2.2 – Tax Evasion and Aggressive Tax Planning</h4>
        """, unsafe_allow_html=True)
        render_indicator_4422()
        
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        with col_nav2:
            if st.button("View full interactive version", key="nav_4422", use_container_width=True):
                st.switch_page("pages/6_topic_4_4.py")
        
        st.markdown("---")
        
        # 3. Criminal Activities
        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <h2 class="evidence-item-title">3. Criminal Activities – drug trafficking as a structured IFF component (4.4.2.3 – Criminal Activities)</h2>
            <p style="color: #555; line-height: 1.8; margin-bottom: 1rem;">The Criminal Activities (4.4.2.3) component includes drug trafficking and other organised crime. The drug-related IFF indicator is built as follows:</p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">It starts from observable UNODC seizure data (quantities of drugs seized at borders or within countries).</li>
                <li style="margin-bottom: 0.75rem;">It then applies typical market prices to these quantities to estimate what the seized drugs would have been worth if they had reached the market.</li>
            </ul>
            <p style="color: #555; line-height: 1.8; margin-top: 1rem; margin-bottom: 1rem;">This logic is used because it:</p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">Converts physical seizures into a monetary scale that can be compared to other IFF channels in the same graph.</li>
                <li style="margin-bottom: 0.75rem;">Provides a conservative, lower-bound estimate, since seizures represent only a fraction of the total volume trafficked.</li>
                <li style="margin-bottom: 0.75rem;">Ties the estimate directly to law-enforcement performance: it reflects both the intensity of trafficking and the degree to which interdiction is (or is not) catching up.</li>
            </ul>
            <div style="background: rgba(0, 43, 127, 0.05); border-left: 4px solid #002B7F; padding: 1rem; margin-top: 1rem; border-radius: 5px;">
                <p style="color: #555; line-height: 1.7; margin: 0;"><strong style="color: #002B7F;">Interpretation – Part of the Challenge:</strong> If seizures are only a slice of overall flows, the resulting drug-IFF values indicate that large amounts of criminal money are still successfully moving through trafficking networks, even after enforcement. This tells us that border interdiction, while active, is not structurally winning against traffickers.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0;">
            <p style="color: #888; font-style: italic; margin-bottom: 0.5rem;">Navigate to Exploratory View → Topic 4.4 → Sub-topic 4.4.2 → 4.4.2.3 – Criminal Activities</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h4 class="graph-title">Indicator 4.4.2.3 – IFFs from Drug Trafficking</h4>
        """, unsafe_allow_html=True)
        render_indicator_4423()
        
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        with col_nav2:
            if st.button("View full interactive version", key="nav_4423", use_container_width=True):
                st.switch_page("pages/6_topic_4_4.py")
        
        st.markdown("---")
        
        # 4. Corruption
        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <h2 class="evidence-item-title">4. Corruption as a reinforcing channel (4.4.2.4 – Corruption)</h2>
            <p style="color: #555; line-height: 1.8; margin-bottom: 1rem;">For corruption-related IFFs, the methodology allocates a regional loss envelope (e.g. US$148 billion) across countries in proportion to their Control of Corruption weaknesses:</p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">Countries with lower World Bank Control of Corruption (WGI) scores are assigned higher estimated corruption losses.</li>
                <li style="margin-bottom: 0.75rem;">The indicator therefore treats corruption not as a random shock but as a systemic feature of weak institutions, directly linked to governance quality.</li>
            </ul>
            <div style="background: rgba(0, 43, 127, 0.05); border-left: 4px solid #002B7F; padding: 1rem; margin-top: 1rem; border-radius: 5px;">
                <p style="color: #555; line-height: 1.7; margin: 0;"><strong style="color: #002B7F;">Interpretation – Completing the Challenge picture:</strong> Corruption is both a channel of IFFs and an enabler of other channels (trade mispricing, tax abuse, criminal flows). The indicator is used to show that countries with weaker anti-corruption environments are systematically more exposed to capital leakage, not just occasionally unlucky.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%); border-left: 5px solid #002B7F; border-radius: 10px; padding: 1.5rem; margin-top: 1rem;">
            <p style="color: #555; line-height: 1.7; margin: 0;"><strong style="color: #002B7F;">Taken together, the Channels of IFFs indicators show that commercial and criminal leakages are both large and persistent.</strong> The core Challenge is the scale and structural nature of outflows—especially through trade mispricing and tax abuse—rather than the absence of isolated enforcement actions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0;">
            <p style="color: #888; font-style: italic; margin-bottom: 0.5rem;">Navigate to Exploratory View → Topic 4.4 → Sub-topic 4.4.2 → 4.4.2.4 – Corruption and Bribery</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h4 class="graph-title">Indicator 4.4.2.4 – Corruption-related IFFs</h4>
        """, unsafe_allow_html=True)
        render_indicator_4424()
        
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        with col_nav2:
            if st.button("View full interactive version", key="nav_4424", use_container_width=True):
                st.switch_page("pages/6_topic_4_4.py")
        
        st.markdown("---")
        
        # Evidence Block 2 – Detection Capacity and the Root Cause
        st.markdown("""
        <div class="evidence-block" style="margin-top: 2rem;">
            <h2>Evidence Block 2 – Detection Capacity and the Root Cause</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 5. Corruption Estimate
        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <h2 class="evidence-item-title">5. Corruption loss as a proxy for institutional weakness (4.4.2.4.a – Corruption Estimate)</h2>
            <p style="color: #555; line-height: 1.8; margin-bottom: 1rem;">The Corruption Estimate refines the corruption story by:</p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">Linking quantitative loss estimates directly to a country's governance score (Control of Corruption);</li>
                <li style="margin-bottom: 0.75rem;">Showing that countries with poor governance indicators carry disproportionately high estimated losses.</li>
            </ul>
            <p style="color: #555; line-height: 1.8; margin-top: 1rem; margin-bottom: 1rem;"><strong style="color: #002B7F;">Why this methodology?</strong></p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">It turns an abstract governance index into a concrete measure of the Root Cause: where corruption is systemic, rules are not enforced, and public officials can facilitate the very trade and tax practices driving IFFs.</li>
                <li style="margin-bottom: 0.75rem;">It recognises that the same institutional weaknesses that allow bribes and embezzlement also undermine detection and enforcement across all IFF channels.</li>
            </ul>
            <div style="background: rgba(0, 43, 127, 0.05); border-left: 4px solid #002B7F; padding: 1rem; margin-top: 1rem; border-radius: 5px;">
                <p style="color: #555; line-height: 1.7; margin: 0;"><strong style="color: #002B7F;">Interpretation – The Root Cause (Why):</strong> This indicator is included to underscore that IFFs are not only about technical price gaps or misdeclared invoices; they are about states that lack the integrity and capacity to prevent and punish these behaviours. It visually anchors the idea that weak institutions are the Root Cause, allowing both commercial and criminal flows to occur at scale.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0;">
            <p style="color: #888; font-style: italic; margin-bottom: 0.5rem;">Navigate to Exploratory View → Topic 4.4 → Sub-topic 4.4.2 → 4.4.2.4 – Corruption and Bribery</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h4 class="graph-title">Indicator 4.4.2.4.a – Corruption Loss vs Control of Corruption</h4>
        """, unsafe_allow_html=True)
        # Note: This is a scatter/dual-axis chart - using the same corruption indicator for now
        render_indicator_4424()
        
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        with col_nav2:
            if st.button("View full interactive version", key="nav_4424a", use_container_width=True):
                st.switch_page("pages/6_topic_4_4.py")
        
        st.markdown("---")
        
        # 6. Detection Efficacy
        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <h2 class="evidence-item-title">6. Detection Efficacy – measuring whether the state can fight back (4.4.3.1, 4.4.3.2.b, 4.4.3.2.c)</h2>
            <p style="color: #555; line-height: 1.8; margin-bottom: 1rem;">The Detection Efficacy indicator (4.4.3.1) aggregates multiple operational dimensions:</p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">Existence and implementation of key legal frameworks and procedures (beneficial-ownership transparency, AML/CFT rules, transfer-pricing documentation, etc.);</li>
                <li style="margin-bottom: 0.75rem;"><strong>Resources and ICT Infrastructure (4.4.3.2.b)</strong> – the availability of modern risk-based customs systems, e-invoicing, analytics tools, and inter-agency data-sharing platforms;</li>
                <li style="margin-bottom: 0.75rem;"><strong>Staff Metrics (4.4.3.2.c)</strong> – the number, skills and deployment of auditors, investigators, data analysts and prosecutors in tax, customs and FIUs.</li>
            </ul>
            <p style="color: #555; line-height: 1.8; margin-top: 1rem; margin-bottom: 1rem;">Across many African countries, these graphs typically show:</p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">Low to moderate Efficacy scores, with only a small group approaching the upper end of the scale;</li>
                <li style="margin-bottom: 0.75rem;">A clear pattern where countries with low Efficacy scores also have thin staffing and weak ICT infrastructure, especially in frontline agencies.</li>
            </ul>
            <p style="color: #555; line-height: 1.8; margin-top: 1rem; margin-bottom: 1rem;"><strong style="color: #002B7F;">Why this methodology?</strong></p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">It explicitly ties the performance of anti-IFF systems to what states have actually invested in—people, tools and systems—rather than to legal texts alone.</li>
                <li style="margin-bottom: 0.75rem;">It answers the question: "Do agencies have the minimum operational muscle to detect and act on the kinds of flows shown in the Channels indicators?"</li>
            </ul>
            <div style="background: rgba(0, 43, 127, 0.05); border-left: 4px solid #002B7F; padding: 1rem; margin-top: 1rem; border-radius: 5px;">
                <p style="color: #555; line-height: 1.7; margin: 0;"><strong style="color: #002B7F;">Interpretation – Quantifying the Root Cause:</strong> Where Detection Efficacy is low and capacity indicators are weak, it is clear that institutions simply cannot match the scale and sophistication of trade mispricing, aggressive tax planning and organised crime. This is the Root Cause (Why): even when the problem is recognised and laws exist on paper, the machinery of the state is too weak to deliver effective enforcement.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 1rem 0;">
            <p style="color: #888; font-style: italic; margin-bottom: 0.5rem;">Navigate to Exploratory View → Topic 4.4 → Sub-topic 4.4.3 → 4.4.3.1 – Efficacy of Anti-IFF Measures</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h4 class="graph-title">Indicator 4.4.3.1 – Efficacy of Anti-IFF Measures</h4>
        """, unsafe_allow_html=True)
        render_indicator_4431()
        
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        with col_nav2:
            if st.button("View full interactive version", key="nav_4431", use_container_width=True):
                st.switch_page("pages/6_topic_4_4.py")
        
        st.markdown("---")
        
        st.markdown("""
        <div style="margin: 1rem 0;">
            <p style="color: #888; font-style: italic; margin-bottom: 0.5rem;">Navigate to Exploratory View → Topic 4.4 → Sub-topic 4.4.3 → 4.4.3.2.b – Resources and ICT Infrastructure</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h4 class="graph-title">Indicator 4.4.3.2.b – Resources and ICT Infrastructure</h4>
        """, unsafe_allow_html=True)
        render_indicator_4432b()
        
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        with col_nav2:
            if st.button("View full interactive version", key="nav_4432b", use_container_width=True):
                st.switch_page("pages/6_topic_4_4.py")
        
        st.markdown("---")
        
        st.markdown("""
        <div style="margin: 1rem 0;">
            <p style="color: #888; font-style: italic; margin-bottom: 0.5rem;">Navigate to Exploratory View → Topic 4.4 → Sub-topic 4.4.3 → 4.4.3.2.c – Staff Metrics</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h4 class="graph-title">Indicator 4.4.3.2.c – Staff Metrics</h4>
        """, unsafe_allow_html=True)
        render_indicator_4432c()
        
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        with col_nav2:
            if st.button("View full interactive version", key="nav_4432c", use_container_width=True):
                st.switch_page("pages/6_topic_4_4.py")
        
        st.markdown("---")
        
        # Policy Synthesis
        st.markdown("""
        <div class="policy-synthesis" style="margin-top: 2rem;">
            <h2>Policy Synthesis – Achieving The Solution</h2>
            <p style="color: #555; line-height: 1.8; margin-bottom: 1.5rem;">The evidence answers the Strategic Question as follows:</p>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem; margin-bottom: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">The largest vulnerability in absolute size is commercial leakage, especially Trade Mispricing and related tax practices.</li>
                <li style="margin-bottom: 0.75rem;">The decisive Root Cause is weak detection and enforcement capacity, which cannot contain or deter these flows.</li>
                <li style="margin-bottom: 0.75rem;">The Solution is therefore to prioritise the biggest IFF channels (commercial/trade) and aggressively reinforce the weakest point (detection capacity), while integrating this work with the broader DRM agenda (Topics 4.1, 4.2, 4.3).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        policy_html = '''
        <div style="background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%); border-left: 5px solid #002B7F; border-radius: 10px; padding: 1.5rem; margin-top: 1rem;">
            <h3 style="color: #002B7F; margin-top: 0; margin-bottom: 1rem;">Policy Recommendations</h3>
            <ul style="color: #555; line-height: 1.8; margin: 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 1rem;">
                    <strong style="color: #002B7F;">1. Target the biggest leakage – Trade Mispricing and Tax Evasion (4.4.2.1, 4.4.2.2)</strong><br>
                    <span style="margin-left: 1.5rem; display: block; margin-top: 0.5rem;">
                        <strong>Recommendation:</strong> Re-align anti-IFF strategies so that specialised units and tools focus on the main commercial channels.<br>
                        • Create or strengthen specialised trade-tax audit units that focus on high-risk sectors (extractives, major importers/exporters, large MNEs).<br>
                        • Systematically use mirror trade statistics, price-reference databases and third-party data (e.g. shipping records) to identify under- and over-invoicing patterns tied to specific firms or sectors.<br>
                        • Integrate this analytical work into joint tax–customs investigations, rather than treating trade and income tax separately.
                    </span>
                </li>
                <li style="margin-bottom: 1rem;">
                    <strong style="color: #002B7F;">2. Strengthen institutional capacity – fix the Root Cause (4.4.3.1, 4.4.3.2.b, 4.4.3.2.c)</strong><br>
                    <span style="margin-left: 1.5rem; display: block; margin-top: 0.5rem;">
                        <strong>Recommendation:</strong> Make Detection Capacity a core budgetary and reform priority.<br>
                        • Substantially increase funding for Resources and ICT Infrastructure (4.4.3.2.b): risk-based customs systems, e-invoicing, data warehouses, cross-border information exchange.<br>
                        • Improve Staff Metrics (4.4.3.2.c) by: recruiting and retaining specialised auditors, forensic accountants and data scientists; providing continuous training on complex IFF detection; aligning incentives (careers, promotions) with successful IFF casework.<br>
                        • Raise Detection Efficacy (4.4.3.1) by linking capacity investments to clear performance targets—more high-risk audits, more complex cases investigated, more successful prosecutions.
                    </span>
                </li>
                <li style="margin-bottom: 1rem;">
                    <strong style="color: #002B7F;">3. Prevent future leakage and reinforce domestic revenues (Link to Topic 4.2 – Revenues)</strong><br>
                    <span style="margin-left: 1.5rem; display: block; margin-top: 0.5rem;">
                        <strong>Recommendation:</strong> Use anti-IFF success to strengthen and legitimise the tax system.<br>
                        • Publicise major enforcement successes to signal that large-scale evasion and mispricing are high-risk activities, while simultaneously simplifying compliance for willing taxpayers.<br>
                        • Channel recovered assets and improved compliance into visible public investments (e.g. social protection, climate adaptation), reinforcing the link between fighting IFFs and development outcomes.<br>
                        • Embed anti-IFF analysis into tax-policy design (Topic 4.2), reducing loopholes and discretionary incentives that create opportunities for profit-shifting and mispricing.
                    </span>
                </li>
                <li style="margin-bottom: 1rem;">
                    <strong style="color: #002B7F;">4. Align capital markets and financial systems with anti-IFF goals (Link to Topic 4.3 – Capital Markets)</strong><br>
                    <span style="margin-left: 1.5rem; display: block; margin-top: 0.5rem;">
                        <strong>Recommendation:</strong> Ensure that efforts to deepen domestic capital markets do not create new IFF channels.<br>
                        • Require robust beneficial-ownership disclosure, AML/CFT checks and transaction monitoring for major listings, bond issues and cross-border investments.<br>
                        • Use improved detection data (from 4.4.3) to screen high-risk sectors and entities in capital-market transactions, ensuring that domestic and regional markets become tools for development, not vehicles for laundering illicit funds.
                    </span>
                </li>
            </ul>
        </div>
        '''
        st.markdown(policy_html, unsafe_allow_html=True)
        
        # Conclusion
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 43, 127, 0.08) 0%, rgba(232, 119, 34, 0.05) 100%); border-left: 5px solid #002B7F; border-radius: 10px; padding: 1.5rem; margin-top: 2rem;">
            <h3 style="color: #002B7F; margin-top: 0; margin-bottom: 1rem;">Conclusion</h3>
            <p style="color: #555; line-height: 1.7; margin: 0;">In answer to the Strategic Question—"Is the primary vulnerability in Africa's anti-IFF efforts a failure to detect flows or a failure to prevent large-scale commercial leakage?"—the evidence suggests a layered conclusion:</p>
            <ul style="color: #555; line-height: 1.8; margin: 1rem 0; padding-left: 1.5rem;">
                <li style="margin-bottom: 0.75rem;">The primary vulnerability in scale is the dominance of commercial IFFs, especially Trade Mispricing and related tax practices, which account for the largest share of outflows.</li>
                <li style="margin-bottom: 0.75rem;">The primary vulnerability in systems is weak detection and enforcement capacity, which cannot effectively counter these flows.</li>
                <li style="margin-bottom: 0.75rem;">The Solution is not to choose between "detection" and "commercial leakage", but to build strong detection systems precisely where commercial leakage is largest. By targeting the main channels, reinforcing institutional capacity, and linking anti-IFF work to broader revenue and capital-market reforms, African countries can move from documenting leaks to systematically retaining the resources needed for sustainable development.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# === 5. FOOTER ===
st.markdown("""
<div class="theme-footer">
    <p>Theme 4 supports countries in strengthening domestic financial management systems for long-term, inclusive development.</p>
</div>
""", unsafe_allow_html=True)
