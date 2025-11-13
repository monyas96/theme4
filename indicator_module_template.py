"""
Reusable Template for Indicator Module
======================================

Copy this template and adapt it for each new indicator.
Replace all placeholders marked with [PLACEHOLDER] with actual values.

Usage:
1. Copy this entire template
2. Replace [PLACEHOLDER] values
3. Adjust chart_type and chart_options based on viz spec
4. Customize map view if applicable
5. Add legend if needed
"""

# ========================================
# INDICATOR MODULE TEMPLATE
# ========================================

with st.container():
    # A. Indicator Header
    indicator_label = "[INDICATOR_LABEL]"  # e.g., "PEFA: PI-1 Aggregate expenditure out-turn"
    
    st.markdown("""
    <div class='indicator-card'>
        <h4>
            Indicator [X.X.X]: [Indicator Name]
            <button type="button" class="info-icon-btn" data-tooltip="[Tooltip text describing the indicator]" style="background: none; border: none; cursor: help; font-size: 0.8em; color: #666; margin-left: 0.5rem; padding: 0;">ℹ️</button>
        </h4>
        <p style="color: #555; line-height: 1.6; margin-bottom: 1rem;">
            <strong>Analytical Focus Question:</strong> [Analytical focus question text]
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
    
    # B. Local Filter Row (scoped to this indicator)
    # Initialize session state for local filters if not exists
    session_key_prefix = "ind_[X_X_X]"  # e.g., "ind_4_1_1"
    
    if f'{session_key_prefix}_year' not in st.session_state:
        st.session_state[f'{session_key_prefix}_year'] = None
    if f'{session_key_prefix}_countries' not in st.session_state:
        st.session_state[f'{session_key_prefix}_countries'] = []
    if f'{session_key_prefix}_region_filter' not in st.session_state:
        st.session_state[f'{session_key_prefix}_region_filter'] = []
    
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
            key=f"{session_key_prefix}_year_filter"
        )
    
    with filter_col2:
        selected_countries_ind = st.multiselect(
            "Select Country",
            options=africa_countries,
            default=[],
            key=f"{session_key_prefix}_country_filter"
        )
    
    with filter_col3:
        selected_regions_ind = st.multiselect(
            "Select Region",
            options=available_regions,
            default=[],
            key=f"{session_key_prefix}_region_filter"
        )
    
    with filter_col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset", key=f"{session_key_prefix}_reset", use_container_width=True):
            # Delete session state keys to reset widgets to defaults
            if f'{session_key_prefix}_year_filter' in st.session_state:
                del st.session_state[f'{session_key_prefix}_year_filter']
            if f'{session_key_prefix}_country_filter' in st.session_state:
                del st.session_state[f'{session_key_prefix}_country_filter']
            if f'{session_key_prefix}_region_filter' in st.session_state:
                del st.session_state[f'{session_key_prefix}_region_filter']
            st.rerun()
    
    # Prepare filtered data for this indicator
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
    
    # C. Visualization Panel with Multi-View Tabs
    tab_graph, tab_map, tab_data = st.tabs(["Graph View", "Map View", "Data Table"])
    
    with tab_graph:
        # Add "How to Read This Graph" hover button
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <button type="button" class="how-to-read-btn" data-tooltip="[How to read this graph instructions - detailed explanation]" style="background: none; border: none; cursor: help; font-size: 0.9em; color: #666; padding: 0.25rem 0.5rem; margin-left: auto;">
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
        
        # Render chart (use chart_type from viz spec: heatmap, line, bar, stacked_bar, etc.)
        if not filtered_ind_data.empty:
            # Use selected regions if provided, otherwise use all
            intermediate_regions = selected_regions_ind if selected_regions_ind else None
            
            uv.render_indicator_section(
                df=filtered_ind_data,
                indicator_label=indicator_label,
                title="",
                description="",
                chart_type="[heatmap|line|bar|stacked_bar]",  # From viz spec
                selected_countries=selected_countries_ind if selected_countries_ind else None,
                year_range=(selected_year_ind, selected_year_ind) if selected_year_ind != "All Years" else None,
                chart_options={
                    # Chart-specific options from viz spec
                    # Examples:
                    # 'x': 'year',
                    # 'y': 'country_or_area',
                    # 'color': 'country_or_area',
                    # 'reference_data': ref_data,
                    # 'intermediate_region_filter': intermediate_regions
                },
                show_data_table=False,
                container_key="[topic_X_X_ind_X_chart]"  # e.g., "topic4_1_ind1_chart"
            )
            
            # Add legend if needed (directly under graph)
            # [LEGEND_CODE_HERE]
            # Example for PEFA scores:
            # st.markdown("""
            # <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            #     <h5 style="color: #002B7F; margin-bottom: 0.5rem;">[Legend Title]</h5>
            #     [Legend content]
            # </div>
            # """, unsafe_allow_html=True)
        else:
            st.info("No data available for the selected filters.")
    
    with tab_map:
        # Map View (if applicable)
        # Should reflect graph view colors/values
        if not filtered_ind_data.empty:
            # Prepare map data
            map_data = filtered_ind_data.copy()
            
            # Convert values if needed (e.g., for PEFA scores or discrete categories)
            # [MAP_DATA_PREPARATION_CODE]
            
            # Use the latest year if multiple years, or selected year
            if selected_year_ind != "All Years":
                map_data = map_data[map_data['year'] == selected_year_ind]
            else:
                # Use latest year per country
                map_data = map_data.loc[map_data.groupby('country_or_area')['year'].idxmax()]
            
            # Create map
            # [MAP_CREATION_CODE]
            # Example using go.Choropleth for discrete colors:
            # import plotly.graph_objects as go
            # 
            # # Merge with reference data to get ISO codes
            # africa_ref = ref_data[ref_data['Region Name'] == 'Africa'].copy()
            # if not africa_ref.empty and 'Country or Area' in africa_ref.columns:
            #     map_data_merged = map_data.merge(
            #         africa_ref[['Country or Area', 'iso3']],
            #         left_on='country_or_area',
            #         right_on='Country or Area',
            #         how='inner'
            #     )
            #     
            #     if not map_data_merged.empty:
            #         # Determine the correct ISO column name after merge
            #         iso_col = 'iso3_y' if 'iso3_y' in map_data_merged.columns else ('iso3_x' if 'iso3_x' in map_data_merged.columns else 'iso3')
            #         if iso_col != 'iso3' and iso_col in map_data_merged.columns:
            #             map_data_merged['iso3'] = map_data_merged[iso_col]
            #         
            #         # Create choropleth
            #         fig = go.Figure(data=go.Choropleth(
            #             locations=map_data_merged['iso3'],
            #             z=map_data_merged['[value_column]'],
            #             locationmode='ISO-3',
            #             colorscale='[colorscale]',
            #             showscale=[True/False],
            #             hovertemplate='[hover_template]',
            #             zmin=[min_value],
            #             zmax=[max_value]
            #         ))
            #         
            #         fig.update_layout(
            #             height=500,
            #             geo=dict(
            #                 bgcolor='rgba(0,0,0,0)',
            #                 lakecolor='rgba(0,0,0,0)',
            #                 landcolor='rgba(217, 217, 217, 1)',
            #                 subunitcolor='white',
            #                 scope='africa',
            #                 showframe=False,
            #                 showcoastlines=True,
            #                 projection_type='natural earth'
            #             ),
            #             margin={"r":0,"t":0,"l":0,"b":0}
            #         )
            #         
            #         st.plotly_chart(fig, use_container_width=True)
            #         
            #         # Add legend if needed
            #         # [MAP_LEGEND_CODE]
        else:
            st.info("No data available for the selected filters.")
    
    with tab_data:
        # Data Table
        if not filtered_ind_data.empty:
            cols_to_show = ['country_or_area', 'year', 'value']  # Adjust as needed
            display_df = filtered_ind_data[[col for col in cols_to_show if col in filtered_ind_data.columns]].copy()
            
            # Rename columns as needed
            # if 'value' in display_df.columns:
            #     display_df = display_df.rename(columns={'value': '[Display Name]'})
            
            st.dataframe(display_df, use_container_width=True)
            
            # Export options
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"indicator_[X_X_X]_{selected_year_ind if selected_year_ind != 'All Years' else 'all_years'}.csv",
                mime="text/csv",
                key=f"{session_key_prefix}_download_csv"
            )
        else:
            st.info("No data available for the selected filters.")
    
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


# ========================================
# PLACEHOLDER REPLACEMENT GUIDE
# ========================================
"""
Replace the following placeholders:

[INDICATOR_LABEL]          - The exact indicator label from your data
[X.X.X]                    - Indicator number (e.g., 4.1.1)
[Indicator Name]           - Full indicator name
[Tooltip text...]          - Brief description for info icon tooltip
[Analytical focus question] - The analytical question text
[X_X_X]                    - Indicator number with underscores (e.g., 4_1_1)
[topic_X_X_ind_X_chart]    - Container key (e.g., topic4_1_ind1_chart)
[heatmap|line|bar|stacked_bar] - Chart type from viz spec
[LEGEND_CODE_HERE]         - Legend HTML/CSS if needed
[MAP_DATA_PREPARATION_CODE] - Code to prepare map data
[MAP_CREATION_CODE]        - Code to create the map
[MAP_LEGEND_CODE]          - Legend for map if needed
[value_column]             - Column name for map values
[colorscale]               - Plotly colorscale name or custom colorscale
[hover_template]           - Hover template string
[min_value]                - Minimum value for map scale
[max_value]                - Maximum value for map scale
[Display Name]             - Display name for data table column
[Definition text]          - Indicator definition
[Source link]              - URL or reference to source
[Efficiency explanation]   - Efficiency relevance text
[Effectiveness explanation] - Effectiveness relevance text
[Proxy justification text] - Why this is a proxy indicator
[Pillar connection text]   - How it connects to the pillar
[Efficiency analysis text] - Efficiency lens analysis
[Effectiveness analysis text] - Effectiveness lens analysis
"""

