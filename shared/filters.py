"""
Filtering module for WUUF Analytics Backend
Handles applying filters to transaction data
"""
from typing import Optional
from datetime import datetime
import pandas as pd


def apply_filters(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    size: Optional[str] = None,
    collection: Optional[str] = None,
    breed: Optional[str] = None,
    channel: Optional[str] = None
) -> pd.DataFrame:
    """
    Apply filters to the transactions dataframe.
    
    Args:
        df: Transactions dataframe
        start_date: Start date filter (ISO format YYYY-MM-DD)
        end_date: End date filter (ISO format YYYY-MM-DD)
        size: Exact size filter
        collection: Exact collection filter
        breed: Exact dog breed filter
        channel: Exact channel filter
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    filtered_df = df.copy()
    
    # Filter by start_date
    if start_date:
        try:
            start_dt = pd.to_datetime(start_date)
            filtered_df = filtered_df[filtered_df['Order_Date'] >= start_dt]
        except Exception as e:
            print(f"Warning: Invalid start_date format '{start_date}': {str(e)}")
    
    # Filter by end_date
    if end_date:
        try:
            end_dt = pd.to_datetime(end_date)
            # Include the entire end date (end of day)
            end_dt = end_dt + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            filtered_df = filtered_df[filtered_df['Order_Date'] <= end_dt]
        except Exception as e:
            print(f"Warning: Invalid end_date format '{end_date}': {str(e)}")
    
    # Filter by Size (exact match)
    if size:
        filtered_df = filtered_df[filtered_df['Size'] == size]
    
    # Filter by Collection (exact match)
    if collection:
        filtered_df = filtered_df[filtered_df['Collection'] == collection]
    
    # Filter by Dog_Breed (exact match)
    if breed:
        filtered_df = filtered_df[filtered_df['Dog_Breed'] == breed]
    
    # Filter by Channel (exact match)
    if channel:
        filtered_df = filtered_df[filtered_df['Channel'] == channel]
    
    return filtered_df


def get_filter_options(df: pd.DataFrame) -> dict:
    """
    Get available filter options from the dataset.
    Useful for populating dropdowns in the frontend.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        dict: Available options for each filter
    """
    return {
        'sizes': sorted(df['Size'].dropna().unique().tolist()),
        'collections': sorted(df['Collection'].dropna().unique().tolist()),
        'breeds': sorted(df['Dog_Breed'].dropna().unique().tolist()),
        'channels': sorted(df['Channel'].dropna().unique().tolist()),
        'date_range': {
            'min_date': df['Order_Date'].min().isoformat() if not df.empty else None,
            'max_date': df['Order_Date'].max().isoformat() if not df.empty else None
        }
    }
