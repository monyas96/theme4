import pandas as pd

def calculate_banking_sector_development_index(df, country_col='country_or_area', year_col='year'):
    """
    Calculate the Banking Sector Development Index for each country-year.

    Methodology:
    1. Collect three variables from WDI:
       - FB.BNK.CAPA.ZS (Bank capital-to-assets ratio, %)
       - FD.RES.LIQU.AS.ZS (Bank liquid reserves-to-assets ratio, %)
       - FS.AST.DOMS.GD.ZS (Domestic credit to private sector, % GDP)
    2. Normalize variables (min-max scaling to 0-1 range) to make them comparable
    3. Apply weighted aggregation: BSDI = 0.4 × CapitalRatio + 0.3 × LiquidityRatio + 0.3 × CreditRatio
    
    If any of the three indicators is missing for a country-year, the index is not calculated for that country-year.

    Weights:
      - Bank capital to assets ratio: 40%
      - Bank liquid reserves to bank assets ratio: 30%
      - Domestic credit provided by financial sector: 30%

    Rationale:
    This weighting balances financial stability (capital and liquidity) with economic growth (credit provision),
    aligning with Basel III and empirical research (see references).

    References:
    1. Jordà, Ò., Schularick, M., & Taylor, A. M. (2017). Macrofinancial History and the New Business Cycle Facts. NBER.
    2. Berger, A. N., & Bouwman, C. H. (2013). How Does Capital Affect Bank Performance During Financial Crises? JFE.
    3. Diamond, D. W., & Dybvig, P. H. (1983). Bank Runs, Deposit Insurance, and Liquidity. JPE.
    4. Brunnermeier, M. K., & Pedersen, L. H. (2009). Market Liquidity and Funding Liquidity. RFS.
    5. Schularick, M., & Taylor, A. M. (2012). Credit Booms Gone Bust. AER.
    6. Gambacorta, L., & Shin, H. S. (2018). Why Bank Capital Matters for Monetary Policy. JFI.

    Parameters:
        df (pd.DataFrame): DataFrame with columns: country_col, year_col, indicator_label, value
        country_col (str): Name of the country column
        year_col (str): Name of the year column

    Returns:
        pd.DataFrame: DataFrame with columns [country_col, year_col, 'Banking Sector Development Index']
    """
    # Define indicator labels (must match your data exactly)
    # These correspond to WDI codes:
    # FB.BNK.CAPA.ZS, FD.RES.LIQU.AS.ZS, FS.AST.DOMS.GD.ZS
    indicators = {
        'Bank capital to assets ratio (%)': 0.4,
        'Bank liquid reserves to bank assets ratio (%)': 0.3,
        'Domestic credit provided by financial sector (% of GDP)': 0.3
    }
    
    # Filter to only required indicators
    df_filtered = df[df['indicator_label'].isin(indicators.keys())].copy()
    
    # Check if we have any data
    if df_filtered.empty:
        return pd.DataFrame(columns=[country_col, year_col, 'Banking Sector Development Index'])
    
    # Pivot to wide format: one row per country-year, columns for each indicator
    df_pivot = df_filtered.pivot_table(
        index=[country_col, year_col],
        columns='indicator_label',
        values='value'
    )
    
    # Check if pivot was successful
    if df_pivot.empty:
        return pd.DataFrame(columns=[country_col, year_col, 'Banking Sector Development Index'])
    
    # Only keep rows where all three indicators are present
    # Check which indicator columns actually exist after pivot
    available_cols = [col for col in indicators.keys() if col in df_pivot.columns]
    if len(available_cols) < len(indicators.keys()):
        # Not all indicators are present in the data
        return pd.DataFrame(columns=[country_col, year_col, 'Banking Sector Development Index'])
    
    df_pivot = df_pivot.dropna(subset=indicators.keys())
    
    # Check if we have any rows after dropping NAs
    if df_pivot.empty:
        return pd.DataFrame(columns=[country_col, year_col, 'Banking Sector Development Index'])
    
    # STEP 2: Normalize each indicator using min-max scaling to 0-1 range
    # This makes the indicators comparable before weighted aggregation
    df_pivot_normalized = df_pivot.copy()
    
    for ind_label in indicators.keys():
        if ind_label in df_pivot_normalized.columns:
            col_data = df_pivot_normalized[ind_label]
            min_val = col_data.min()
            max_val = col_data.max()
            
            # Avoid division by zero
            if max_val > min_val:
                df_pivot_normalized[ind_label] = (col_data - min_val) / (max_val - min_val)
            else:
                # If all values are the same, set to 0.5 (neutral)
                df_pivot_normalized[ind_label] = 0.5
    
    # STEP 3: Calculate weighted sum of normalized indicators
    df_pivot_normalized['Banking Sector Development Index'] = sum(
        df_pivot_normalized[ind] * weight for ind, weight in indicators.items()
    )
    
    # Reset index for output
    result = df_pivot_normalized[['Banking Sector Development Index']].reset_index()
    return result 

def calculate_stock_market_cap_to_gdp(df, country_col='country_or_area', year_col='year'):
    """
    Calculate Stock Market Capitalization to GDP (%) for each country-year.
    Formula: (Market capitalization of listed domestic companies (current US$) / GDP (current US$)) * 100
    If either value is missing for a country-year, the result is missing for that country-year.
    Returns a DataFrame with columns: country, year, Stock Market Cap to GDP (%)
    Handles both wide and long formats.
    """
    market_cap_col = 'Market capitalization of listed domestic companies (current US$)'
    gdp_col = 'GDP (current US$)'
    indicators = [market_cap_col, gdp_col]
    # If wide format, melt to long
    if all(col in df.columns for col in [country_col, year_col, market_cap_col, gdp_col]):
        df_long = df.melt(
            id_vars=[country_col, year_col],
            value_vars=indicators,
            var_name='indicator_label',
            value_name='value'
        )
    elif all(col in df.columns for col in [country_col, year_col, 'indicator_label', 'value']):
        df_long = df.copy()
    else:
        return pd.DataFrame(columns=[country_col, year_col, 'Stock Market Cap to GDP (%)'])
    df_pivot = df_long[df_long['indicator_label'].isin(indicators)].pivot_table(
        index=[country_col, year_col],
        columns='indicator_label',
        values='value'
    )
    if not set(indicators).issubset(df_pivot.columns):
        return pd.DataFrame(columns=[country_col, year_col, 'Stock Market Cap to GDP (%)'])
    df_pivot = df_pivot.dropna(subset=indicators)
    df_pivot['Stock Market Cap to GDP (%)'] = (df_pivot[market_cap_col] / df_pivot[gdp_col]) * 100
    result = df_pivot[['Stock Market Cap to GDP (%)']].reset_index()
    return result

def calculate_adequacy_of_international_reserves(df, country_col='country_or_area', year_col='year'):
    """
    Calculate Adequacy of International Reserves for each country-year.
    Formula: (Reserves and related items (BoP, current US$)) / (External debt stocks, short-term (DOD, current US$))
    If either value is missing for a country-year, the result is missing for that country-year.
    Returns a DataFrame with columns: country, year, Adequacy of International Reserves
    """
    reserves_label = 'Reserves and related items (BoP, current US$)'
    debt_label = 'External debt stocks, short-term (DOD, current US$)'
    indicators = [reserves_label, debt_label]
    df_pivot = df[df['indicator_label'].isin(indicators)].pivot_table(
        index=[country_col, year_col],
        columns='indicator_label',
        values='value'
    )
    if not set(indicators).issubset(df_pivot.columns):
        return pd.DataFrame(columns=[country_col, year_col, 'Adequacy of International Reserves'])
    df_pivot = df_pivot.dropna(subset=indicators)
    
    # Handle division by zero: if short-term debt is 0 or very small, set ratio to NaN
    # This prevents infinity values
    df_pivot['Adequacy of International Reserves'] = df_pivot[reserves_label] / df_pivot[debt_label]
    
    # Replace infinity and very large values with NaN (when debt is 0 or near 0)
    # Also cap extremely large but valid ratios at a reasonable maximum (e.g., 10.0)
    df_pivot.loc[df_pivot[debt_label] <= 0, 'Adequacy of International Reserves'] = pd.NA
    df_pivot.loc[df_pivot['Adequacy of International Reserves'] == float('inf'), 'Adequacy of International Reserves'] = pd.NA
    df_pivot.loc[df_pivot['Adequacy of International Reserves'] == float('-inf'), 'Adequacy of International Reserves'] = pd.NA
    
    # Cap extremely large ratios at 10.0 for visualization purposes (countries with very high reserves relative to debt)
    # This prevents outliers from making the chart unreadable
    df_pivot.loc[df_pivot['Adequacy of International Reserves'] > 10.0, 'Adequacy of International Reserves'] = 10.0
    
    result = df_pivot[['Adequacy of International Reserves']].reset_index()
    return result 

def calculate_indicator_with_gap(df, required_labels, calculation_func, country_col='country_or_area', year_col='year'):
    """
    Generalized function to calculate an indicator and identify data gaps.

    Parameters:
        df (pd.DataFrame): DataFrame with columns: country_col, year_col, indicator_label, value
        required_labels (list): List of required indicator labels
        calculation_func (function): Function to calculate the indicator from a DataFrame
        country_col (str): Name of the country column
        year_col (str): Name of the year column

    Returns:
        result (pd.DataFrame): DataFrame with calculated indicator
        missing (pd.DataFrame): DataFrame with missing country-year pairs
    """
    df_required = df[df['indicator_label'].isin(required_labels)]
    df_pivot = df_required.pivot_table(index=[country_col, year_col], columns='indicator_label', values='value')
    missing_mask = df_pivot.isnull().any(axis=1)
    missing = df_pivot[missing_mask].reset_index()[[country_col, year_col]]
    df_pivot = df_pivot.dropna()
    result = calculation_func(df_pivot)
    return result, missing 

def calculate_corruption_losses(df):
    """
    Calculate each country's share of the $148B annual corruption losses using WGI Control of Corruption scores.

    Steps:
    1. Normalize scores to [0, 1]: normalized_score = (score + 2.5) / 5.0
    2. Invert: inverted_score = 1 - normalized_score
    3. Assign weights = inverted_score
    4. Allocate $148B: corruption_loss_billion_usd = (weight / total_weight) * 148

    Returns a DataFrame with columns:
    ['country_or_area', 'year', 'value', 'normalized_score', 'inverted_score', 'corruption_loss_billion_usd']
    """
    idx = df.groupby('country_or_area')['year'].transform('max') == df['year']
    latest = df[idx].copy()
    latest['normalized_score'] = (latest['value'] + 2.5) / 5.0
    latest['normalized_score'] = latest['normalized_score'].clip(0, 1)
    latest['inverted_score'] = 1 - latest['normalized_score']
    latest['weight'] = latest['inverted_score']
    total_weight = latest['weight'].sum()
    latest['corruption_loss_billion_usd'] = (latest['weight'] / total_weight) * 148
    latest['corruption_loss_billion_usd'] = latest['corruption_loss_billion_usd'].round(2)
    return latest 