"""
Test script to load data from Google Sheets and export to CSV files
This script will:
1. Load data from Google Sheets
2. Save to CSV files in data/ folder
3. Display data summaries
4. Run basic analytics
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from shared.data_loader import load_transactions, get_google_sheets_client, load_sheet_to_dataframe
from shared.aggregations import sales_overview, daily_sales, sales_by_collection, sales_by_breed, sales_by_size
import pandas as pd

def create_data_folder():
    """Create data folder if it doesn't exist"""
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)
    return data_folder

def save_to_csv(df, filename, folder):
    """Save dataframe to CSV file"""
    filepath = folder / filename
    df.to_csv(filepath, index=False)
    print(f"✓ Saved: {filepath} ({len(df)} rows)")
    return filepath

def display_dataframe_info(df, name):
    """Display information about a dataframe"""
    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"{'='*60}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"\nColumn Names:")
    for col in df.columns:
        dtype = df[col].dtype
        null_count = df[col].isnull().sum()
        print(f"  - {col} ({dtype}) - {null_count} nulls")
    
    print(f"\nFirst 3 rows:")
    print(df.head(3).to_string())
    print()

def main():
    print("="*60)
    print("WUUF Analytics - Data Loading Test")
    print("="*60)
    print()
    
    # Create data folder
    print("Step 1: Creating data folder...")
    data_folder = create_data_folder()
    print(f"✓ Data folder ready: {data_folder.absolute()}\n")
    
    # Load data from Google Sheets
    print("Step 2: Loading data from Google Sheets...")
    print("(This may take a few moments...)\n")
    
    try:
        # Get Google Sheets client
        sheet_id = os.getenv('GOOGLE_SHEET_ID', '1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE')
        client = get_google_sheets_client()
        sheet = client.open_by_key(sheet_id)
        
        # Load individual sheets
        print("Loading Orders sheet...")
        orders_df = load_sheet_to_dataframe(sheet, 'Orders')
        print(f"✓ Loaded {len(orders_df)} orders")
        
        print("Loading Order_Items sheet...")
        order_items_df = load_sheet_to_dataframe(sheet, 'Order_Items')
        print(f"✓ Loaded {len(order_items_df)} order items")
        
        print("Loading Products sheet...")
        products_df = load_sheet_to_dataframe(sheet, 'Products')
        print(f"✓ Loaded {len(products_df)} products")
        
        # Load joined transactions
        print("\nLoading joined transactions...")
        transactions_df = load_transactions(force_refresh=True)
        print(f"✓ Created {len(transactions_df)} transaction records")
        
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        return
    
    # Save to CSV files
    print("\nStep 3: Saving to CSV files...")
    try:
        save_to_csv(orders_df, "Orders.csv", data_folder)
        save_to_csv(order_items_df, "Order_Items.csv", data_folder)
        save_to_csv(products_df, "Products.csv", data_folder)
        save_to_csv(transactions_df, "Transactions.csv", data_folder)
        print("✓ All files saved successfully!")
    except Exception as e:
        print(f"✗ Error saving files: {str(e)}")
        return
    
    # Display data summaries
    print("\n" + "="*60)
    print("DATA SUMMARIES")
    print("="*60)
    
    display_dataframe_info(orders_df, "ORDERS")
    display_dataframe_info(order_items_df, "ORDER ITEMS")
    display_dataframe_info(products_df, "PRODUCTS")
    display_dataframe_info(transactions_df, "TRANSACTIONS (JOINED)")
    
    # Data quality checks
    print("\n" + "="*60)
    print("DATA QUALITY CHECKS")
    print("="*60)
    print()
    
    print("Unique Values:")
    print(f"  - Unique Orders: {transactions_df['Order_ID'].nunique()}")
    print(f"  - Unique Collections: {transactions_df['Collection'].nunique()}")
    print(f"  - Unique Dog Breeds: {transactions_df['Dog_Breed'].nunique()}")
    print(f"  - Unique Sizes: {transactions_df['Size'].nunique()}")
    print(f"  - Unique Channels: {transactions_df['Channel'].nunique()}")
    
    print(f"\nDate Range:")
    if 'Order_Date' in transactions_df.columns:
        min_date = transactions_df['Order_Date'].min()
        max_date = transactions_df['Order_Date'].max()
        print(f"  - From: {min_date}")
        print(f"  - To: {max_date}")
    
    print(f"\nCollections:")
    collections = transactions_df['Collection'].value_counts()
    for col, count in collections.head(10).items():
        print(f"  - {col}: {count} items")
    
    print(f"\nDog Breeds:")
    breeds = transactions_df['Dog_Breed'].value_counts()
    for breed, count in breeds.head(10).items():
        print(f"  - {breed}: {count} items")
    
    print(f"\nSales Channels:")
    channels = transactions_df['Channel'].value_counts()
    for channel, count in channels.items():
        print(f"  - {channel}: {count} items")
    
    # Run analytics
    print("\n" + "="*60)
    print("ANALYTICS")
    print("="*60)
    print()
    
    try:
        # Overall sales
        overview = sales_overview(transactions_df)
        print("Overall Sales Overview:")
        print(f"  Total Revenue: {overview['total_revenue']:,.2f} THB")
        print(f"  Total Cost: {overview['total_cost']:,.2f} THB")
        print(f"  Total Profit: {overview['total_profit']:,.2f} THB")
        print(f"  Profit Margin: {(overview['total_profit']/overview['total_revenue']*100):.1f}%")
        print(f"  Total Orders: {overview['total_orders']}")
        print(f"  Total Quantity: {overview['total_quantity']}")
        print(f"  Average Order Value: {overview['average_order_value']:,.2f} THB")
        
        # Top collections
        print(f"\nTop 5 Collections by Revenue:")
        by_collection = sales_by_collection(transactions_df)
        for i, item in enumerate(by_collection[:5], 1):
            print(f"  {i}. {item['collection']}: {item['revenue']:,.2f} THB ({item['quantity']} items)")
        
        # Top breeds
        print(f"\nTop 5 Dog Breeds by Revenue:")
        by_breed = sales_by_breed(transactions_df)
        for i, item in enumerate(by_breed[:5], 1):
            print(f"  {i}. {item['breed']}: {item['revenue']:,.2f} THB ({item['quantity']} items)")
        
        # Sales by size
        print(f"\nSales by Size:")
        by_size = sales_by_size(transactions_df)
        for item in by_size:
            print(f"  - Size {item['size']}: {item['revenue']:,.2f} THB ({item['quantity']} items)")
        
    except Exception as e:
        print(f"✗ Error running analytics: {str(e)}")
    
    # Summary
    print("\n" + "="*60)
    print("TEST COMPLETE!")
    print("="*60)
    print()
    print("✓ Data loaded successfully from Google Sheets")
    print("✓ CSV files saved to data/ folder")
    print("✓ Analytics working correctly")
    print()
    print("Next steps:")
    print("  1. Check the data/ folder for CSV files")
    print("  2. Open them in Excel/Sheets to inspect")
    print("  3. Start the FastAPI server: python apps/api/main.py")
    print("  4. Test endpoints at http://localhost:8000/docs")
    print()

if __name__ == "__main__":
    main()
