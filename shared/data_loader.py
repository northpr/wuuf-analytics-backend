"""
Data loader module for WUUF Analytics Backend
Handles loading data from Google Sheets and joining tables
"""
import os
import json
import re
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from functools import lru_cache


# Cache configuration
CACHE_DURATION_MINUTES = 5
_cache_timestamp = None
_cached_data = None


def get_google_sheets_client():
    """
    Initialize and return a Google Sheets client using service account credentials.
    Supports both file-based and environment variable credentials.
    """
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    
    # Try to load credentials from environment variable (Railway deployment)
    creds_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    
    if creds_json:
        # Parse JSON string from environment variable
        try:
            creds_dict = json.loads(creds_json)
            credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        except json.JSONDecodeError:
            raise ValueError("Invalid GOOGLE_SERVICE_ACCOUNT_JSON format")
    else:
        # Load from file (local development)
        creds_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'gold-totem-478004-q0-9501779d48ad.json')
        if not os.path.exists(creds_file):
            raise FileNotFoundError(f"Service account file not found: {creds_file}")
        credentials = Credentials.from_service_account_file(creds_file, scopes=scopes)
    
    return gspread.authorize(credentials)


def load_sheet_to_dataframe(sheet, sheet_name: str) -> pd.DataFrame:
    """
    Load a specific worksheet from Google Sheets and convert to pandas DataFrame.
    Filters out empty template rows automatically.
    
    Args:
        sheet: Google Sheets spreadsheet object
        sheet_name: Name of the worksheet to load
        
    Returns:
        pd.DataFrame: Loaded data with empty rows filtered out
    """
    try:
        worksheet = sheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        # Filter out empty template rows based on key fields
        if sheet_name == 'Orders':
            # Keep only rows where Order_ID is not empty
            df = df[df['Order_ID'].notna() & (df['Order_ID'] != '')]
        elif sheet_name == 'Order_Items':
            # Keep only rows where SKU is not empty
            df = df[df['SKU'].notna() & (df['SKU'] != '')]
        elif sheet_name == 'Products':
            # Keep only rows where SKU is not empty
            df = df[df['SKU'].notna() & (df['SKU'] != '')]
        
        return df
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Worksheet '{sheet_name}' not found in the Google Sheet")
    except Exception as e:
        raise Exception(f"Error loading worksheet '{sheet_name}': {str(e)}")


def extract_collection_from_sku(sku: str) -> str:
    """
    Extract collection prefix from SKU.
    Example: "WUUF-001-WH-M" -> "WUUF-001"
    
    Args:
        sku: Product SKU string
        
    Returns:
        str: Collection prefix
    """
    if pd.isna(sku) or not sku:
        return ""
    
    # Try regex pattern first
    match = re.match(r'(WUUF-\d{3})', str(sku))
    if match:
        return match.group(1)
    
    # Fallback to split method
    parts = str(sku).split('-')
    if len(parts) >= 2:
        return f"{parts[0]}-{parts[1]}"
    
    return str(sku)


def join_transactions(orders_df: pd.DataFrame, 
                      order_items_df: pd.DataFrame, 
                      products_df: pd.DataFrame) -> pd.DataFrame:
    """
    Join Orders, Order_Items, and Products tables to create combined transactions dataset.
    
    Args:
        orders_df: Orders dataframe
        order_items_df: Order_Items dataframe
        products_df: Products dataframe
        
    Returns:
        pd.DataFrame: Combined transactions dataframe
    """
    # Join Order_Items with Orders on Order_ID
    transactions = order_items_df.merge(
        orders_df,
        on='Order_ID',
        how='left'
    )
    
    # Join with Products on SKU
    transactions = transactions.merge(
        products_df[['SKU', 'Product_Name', 'Dog_Breed']],
        on='SKU',
        how='left'
    )
    
    # Extract Collection from SKU
    transactions['Collection'] = transactions['SKU'].apply(extract_collection_from_sku)
    
    # Convert Order_Date to datetime
    transactions['Order_Date'] = pd.to_datetime(transactions['Order_Date'], errors='coerce')
    
    # Ensure numeric columns are proper numeric types
    numeric_columns = ['Qty', 'Unit_Price_THB', 'Line_Subtotal', 'COGS_THB', 'Line_Profit']
    for col in numeric_columns:
        if col in transactions.columns:
            transactions[col] = pd.to_numeric(transactions[col], errors='coerce').fillna(0)
    
    # Select and order columns
    column_order = [
        'Order_Date', 'Order_ID', 'Channel', 'Customer_Name', 'Instagram', 'Phone',
        'SKU', 'Collection', 'Product_Name', 'Dog_Breed', 
        'Shirt_Color', 'Size', 'Qty', 'Unit_Price_THB', 
        'Line_Subtotal', 'COGS_THB', 'Line_Profit'
    ]
    
    # Only include columns that exist
    available_columns = [col for col in column_order if col in transactions.columns]
    transactions = transactions[available_columns]
    
    return transactions


def load_transactions(force_refresh: bool = False) -> pd.DataFrame:
    """
    Load and cache transaction data from Google Sheets.
    
    Args:
        force_refresh: Force reload from Google Sheets, ignoring cache
        
    Returns:
        pd.DataFrame: Combined transactions dataframe
    """
    global _cache_timestamp, _cached_data
    
    # Check if cache is valid
    if not force_refresh and _cached_data is not None and _cache_timestamp is not None:
        time_since_cache = datetime.now() - _cache_timestamp
        if time_since_cache < timedelta(minutes=CACHE_DURATION_MINUTES):
            return _cached_data.copy()
    
    # Load fresh data from Google Sheets
    sheet_id = os.getenv('GOOGLE_SHEET_ID', '1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE')
    
    try:
        # Step 1: Get Google Sheets client
        try:
            client = get_google_sheets_client()
        except FileNotFoundError as e:
            raise Exception(f"Service account credentials file not found. Error: {str(e)}")
        except ValueError as e:
            raise Exception(f"Invalid service account credentials format. Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to authenticate with Google Sheets. Error: {str(e)}")
        
        # Step 2: Open spreadsheet
        try:
            sheet = client.open_by_key(sheet_id)
        except gspread.exceptions.SpreadsheetNotFound:
            raise Exception(f"Spreadsheet not found with ID: {sheet_id}. Make sure the sheet is shared with the service account: wuuf-817@gold-totem-478004-q0.iam.gserviceaccount.com")
        except gspread.exceptions.APIError as e:
            raise Exception(f"Google Sheets API error: {str(e)}. Check if the sheet is shared with the service account.")
        except Exception as e:
            raise Exception(f"Failed to open spreadsheet: {str(e)}")
        
        # Step 3: Load worksheets - with detailed error messages
        try:
            orders_df = load_sheet_to_dataframe(sheet, 'Orders')
        except ValueError as e:
            available_sheets = [ws.title for ws in sheet.worksheets()]
            raise Exception(f"Sheet 'Orders' not found. Available sheets: {', '.join(available_sheets)}. Sheet names are case-sensitive!")
        except Exception as e:
            raise Exception(f"Error loading Orders sheet: {str(e)}")
        
        try:
            order_items_df = load_sheet_to_dataframe(sheet, 'Order_Items')
        except ValueError as e:
            available_sheets = [ws.title for ws in sheet.worksheets()]
            raise Exception(f"Sheet 'Order_Items' not found. Available sheets: {', '.join(available_sheets)}. Sheet names are case-sensitive!")
        except Exception as e:
            raise Exception(f"Error loading Order_Items sheet: {str(e)}")
        
        try:
            products_df = load_sheet_to_dataframe(sheet, 'Products')
        except ValueError as e:
            available_sheets = [ws.title for ws in sheet.worksheets()]
            raise Exception(f"Sheet 'Products' not found. Available sheets: {', '.join(available_sheets)}. Sheet names are case-sensitive!")
        except Exception as e:
            raise Exception(f"Error loading Products sheet: {str(e)}")
        
        # Step 4: Join tables
        try:
            transactions = join_transactions(orders_df, order_items_df, products_df)
        except Exception as e:
            raise Exception(f"Error joining data tables: {str(e)}")
        
        # Update cache
        _cached_data = transactions
        _cache_timestamp = datetime.now()
        
        return transactions.copy()
        
    except Exception as e:
        # If cache exists, return it even if expired
        if _cached_data is not None:
            print(f"Warning: Failed to refresh data, using cached data. Error: {str(e)}")
            return _cached_data.copy()
        else:
            # Re-raise with full error message
            error_msg = str(e) if str(e) else "Unknown error occurred"
            raise Exception(error_msg)


def get_cache_info() -> dict:
    """
    Get information about the current cache status.
    
    Returns:
        dict: Cache information
    """
    global _cache_timestamp, _cached_data
    
    if _cached_data is None:
        return {
            'cached': False,
            'cache_timestamp': None,
            'records_count': 0
        }
    
    return {
        'cached': True,
        'cache_timestamp': _cache_timestamp.isoformat() if _cache_timestamp else None,
        'records_count': len(_cached_data),
        'cache_age_seconds': (datetime.now() - _cache_timestamp).total_seconds() if _cache_timestamp else None
    }
