"""
Aggregation module for WUUF Analytics Backend
Handles data aggregation and summary calculations
"""
import pandas as pd
from typing import Dict, List, Any


def sales_overview(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate overall sales summary metrics.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        dict: Summary metrics including total revenue, cost, profit, orders, quantity, and AOV
    """
    if df.empty:
        return {
            'total_revenue': 0.0,
            'total_cost': 0.0,
            'total_profit': 0.0,
            'total_orders': 0,
            'total_quantity': 0,
            'average_order_value': 0.0
        }
    
    total_revenue = float(df['Line_Subtotal'].sum())
    total_cost = float(df['COGS_THB'].sum())
    total_profit = float(df['Line_Profit'].sum())
    total_orders = int(df['Order_ID'].nunique())
    total_quantity = int(df['Qty'].sum())
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    
    return {
        'total_revenue': round(total_revenue, 2),
        'total_cost': round(total_cost, 2),
        'total_profit': round(total_profit, 2),
        'total_orders': total_orders,
        'total_quantity': total_quantity,
        'average_order_value': round(average_order_value, 2)
    }


def daily_sales(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Calculate daily sales metrics grouped by Order_Date.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        list: Daily metrics with date, revenue, cost, profit, quantity, and orders
    """
    if df.empty:
        return []
    
    # Group by Order_Date
    daily_df = df.groupby(df['Order_Date'].dt.date).agg({
        'Line_Subtotal': 'sum',
        'COGS_THB': 'sum',
        'Line_Profit': 'sum',
        'Qty': 'sum',
        'Order_ID': 'nunique'
    }).reset_index()
    
    # Rename columns
    daily_df.columns = ['date', 'revenue', 'cost', 'profit', 'quantity', 'orders']
    
    # Convert to list of dicts
    result = []
    for _, row in daily_df.iterrows():
        result.append({
            'date': row['date'].isoformat(),
            'revenue': round(float(row['revenue']), 2),
            'cost': round(float(row['cost']), 2),
            'profit': round(float(row['profit']), 2),
            'quantity': int(row['quantity']),
            'orders': int(row['orders'])
        })
    
    # Sort by date
    result.sort(key=lambda x: x['date'])
    
    return result


def sales_by_collection(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Calculate sales metrics grouped by Collection.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        list: Collection metrics with collection, revenue, cost, profit, quantity, and orders
    """
    if df.empty:
        return []
    
    # Group by Collection
    collection_df = df.groupby('Collection').agg({
        'Line_Subtotal': 'sum',
        'COGS_THB': 'sum',
        'Line_Profit': 'sum',
        'Qty': 'sum',
        'Order_ID': 'nunique'
    }).reset_index()
    
    # Rename columns
    collection_df.columns = ['collection', 'revenue', 'cost', 'profit', 'quantity', 'orders']
    
    # Convert to list of dicts
    result = []
    for _, row in collection_df.iterrows():
        result.append({
            'collection': row['collection'],
            'revenue': round(float(row['revenue']), 2),
            'cost': round(float(row['cost']), 2),
            'profit': round(float(row['profit']), 2),
            'quantity': int(row['quantity']),
            'orders': int(row['orders'])
        })
    
    # Sort by revenue descending
    result.sort(key=lambda x: x['revenue'], reverse=True)
    
    return result


def sales_by_breed(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Calculate sales metrics grouped by Dog_Breed.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        list: Breed metrics with breed, revenue, cost, profit, quantity, and orders
    """
    if df.empty:
        return []
    
    # Filter out null breeds
    breed_df = df[df['Dog_Breed'].notna()].copy()
    
    if breed_df.empty:
        return []
    
    # Group by Dog_Breed
    breed_df = breed_df.groupby('Dog_Breed').agg({
        'Line_Subtotal': 'sum',
        'COGS_THB': 'sum',
        'Line_Profit': 'sum',
        'Qty': 'sum',
        'Order_ID': 'nunique'
    }).reset_index()
    
    # Rename columns
    breed_df.columns = ['breed', 'revenue', 'cost', 'profit', 'quantity', 'orders']
    
    # Convert to list of dicts
    result = []
    for _, row in breed_df.iterrows():
        result.append({
            'breed': row['breed'],
            'revenue': round(float(row['revenue']), 2),
            'cost': round(float(row['cost']), 2),
            'profit': round(float(row['profit']), 2),
            'quantity': int(row['quantity']),
            'orders': int(row['orders'])
        })
    
    # Sort by revenue descending
    result.sort(key=lambda x: x['revenue'], reverse=True)
    
    return result


def sales_by_size(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Calculate sales metrics grouped by Size.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        list: Size metrics with size, revenue, cost, profit, quantity, and orders
    """
    if df.empty:
        return []
    
    # Filter out null sizes
    size_df = df[df['Size'].notna()].copy()
    
    if size_df.empty:
        return []
    
    # Group by Size
    size_df = size_df.groupby('Size').agg({
        'Line_Subtotal': 'sum',
        'COGS_THB': 'sum',
        'Line_Profit': 'sum',
        'Qty': 'sum',
        'Order_ID': 'nunique'
    }).reset_index()
    
    # Rename columns
    size_df.columns = ['size', 'revenue', 'cost', 'profit', 'quantity', 'orders']
    
    # Convert to list of dicts
    result = []
    for _, row in size_df.iterrows():
        result.append({
            'size': row['size'],
            'revenue': round(float(row['revenue']), 2),
            'cost': round(float(row['cost']), 2),
            'profit': round(float(row['profit']), 2),
            'quantity': int(row['quantity']),
            'orders': int(row['orders'])
        })
    
    # Define size order for sorting
    size_order = {'XS': 1, 'S': 2, 'M': 3, 'L': 4, 'XL': 5, 'XXL': 6, '2XL': 6, '3XL': 7}
    
    # Sort by size order, then by size name
    result.sort(key=lambda x: (size_order.get(x['size'], 999), x['size']))
    
    return result


def customer_repeat_rate(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate customer repeat purchase rate.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        dict: Repeat rate metrics including repeat/new customer counts and percentages
    """
    if df.empty:
        return {
            'total_customers': 0,
            'repeat_customers': 0,
            'new_customers': 0,
            'repeat_rate': 0.0,
            'average_orders_per_customer': 0.0
        }
    
    # Count orders per customer
    customer_orders = df.groupby('Customer_Name')['Order_ID'].nunique().reset_index()
    customer_orders.columns = ['customer', 'order_count']
    
    total_customers = len(customer_orders)
    repeat_customers = len(customer_orders[customer_orders['order_count'] > 1])
    new_customers = total_customers - repeat_customers
    repeat_rate = (repeat_customers / total_customers * 100) if total_customers > 0 else 0.0
    avg_orders = customer_orders['order_count'].mean()
    
    return {
        'total_customers': total_customers,
        'repeat_customers': repeat_customers,
        'new_customers': new_customers,
        'repeat_rate': round(repeat_rate, 2),
        'average_orders_per_customer': round(avg_orders, 2)
    }


def customer_lifetime_value(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Calculate customer lifetime value metrics.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        list: Customer CLV metrics with aggregated spending data including Instagram handle
    """
    if df.empty:
        return []
    
    # Aggregate by customer
    agg_dict = {
        'Line_Subtotal': 'sum',
        'Line_Profit': 'sum',
        'Order_ID': 'nunique',
        'Qty': 'sum',
        'Order_Date': ['min', 'max']
    }
    
    # Add Instagram if available
    if 'Instagram' in df.columns:
        agg_dict['Instagram'] = 'first'
    
    # Add Phone if available
    if 'Phone' in df.columns:
        agg_dict['Phone'] = 'first'
    
    clv_df = df.groupby('Customer_Name').agg(agg_dict).reset_index()
    
    # Flatten column names - build dynamically
    column_names = ['customer', 'total_revenue', 'total_profit', 'total_orders', 'total_quantity', 'first_order', 'last_order']
    if 'Instagram' in df.columns:
        column_names.append('instagram')
    if 'Phone' in df.columns:
        column_names.append('phone')
    
    clv_df.columns = column_names
    
    # Calculate average order value
    clv_df['avg_order_value'] = clv_df['total_revenue'] / clv_df['total_orders']
    
    # Calculate customer lifetime (days)
    clv_df['lifetime_days'] = (clv_df['last_order'] - clv_df['first_order']).dt.days
    
    # Convert to list of dicts
    result = []
    for _, row in clv_df.iterrows():
        # Handle NaN values in lifetime_days
        lifetime_days = 0 if pd.isna(row['lifetime_days']) else int(row['lifetime_days'])
        
        customer_data = {
            'customer': row['customer'],
            'total_revenue': round(float(row['total_revenue']), 2),
            'total_profit': round(float(row['total_profit']), 2),
            'total_orders': int(row['total_orders']),
            'total_quantity': int(row['total_quantity']),
            'avg_order_value': round(float(row['avg_order_value']), 2),
            'first_order_date': row['first_order'].isoformat(),
            'last_order_date': row['last_order'].isoformat(),
            'lifetime_days': lifetime_days
        }
        
        # Add Instagram if available
        if 'instagram' in row.index:
            instagram = row['instagram'] if pd.notna(row['instagram']) and row['instagram'] != '' else None
            customer_data['instagram'] = instagram
        
        # Add Phone if available
        if 'phone' in row.index:
            phone = row['phone'] if pd.notna(row['phone']) and row['phone'] != '' else None
            customer_data['phone'] = phone
        
        result.append(customer_data)
    
    # Sort by total revenue descending
    result.sort(key=lambda x: x['total_revenue'], reverse=True)
    
    return result


def top_customers(df: pd.DataFrame, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get top customers by revenue.
    
    Args:
        df: Transactions dataframe
        limit: Number of top customers to return
        
    Returns:
        list: Top customers with revenue, orders, and quantity
    """
    if df.empty:
        return []
    
    # Aggregate by customer
    top_df = df.groupby('Customer_Name').agg({
        'Line_Subtotal': 'sum',
        'Line_Profit': 'sum',
        'Order_ID': 'nunique',
        'Qty': 'sum'
    }).reset_index()
    
    # Rename columns
    top_df.columns = ['customer', 'total_revenue', 'total_profit', 'total_orders', 'total_quantity']
    
    # Sort by revenue and get top N
    top_df = top_df.nlargest(limit, 'total_revenue')
    
    # Convert to list of dicts
    result = []
    for idx, row in top_df.iterrows():
        result.append({
            'rank': len(result) + 1,
            'customer': row['customer'],
            'total_revenue': round(float(row['total_revenue']), 2),
            'total_profit': round(float(row['total_profit']), 2),
            'total_orders': int(row['total_orders']),
            'total_quantity': int(row['total_quantity'])
        })
    
    return result


def customer_acquisition_by_channel(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Analyze customer acquisition by channel.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        list: Customer acquisition metrics by channel
    """
    if df.empty:
        return []
    
    # Get first order date for each customer
    first_orders = df.groupby('Customer_Name').agg({
        'Order_Date': 'min',
        'Channel': 'first'
    }).reset_index()
    
    # Count customers by channel
    channel_df = first_orders.groupby('Channel').agg({
        'Customer_Name': 'count'
    }).reset_index()
    
    channel_df.columns = ['channel', 'new_customers']
    
    # Calculate percentage
    total_customers = channel_df['new_customers'].sum()
    channel_df['percentage'] = (channel_df['new_customers'] / total_customers * 100) if total_customers > 0 else 0
    
    # Convert to list of dicts
    result = []
    for _, row in channel_df.iterrows():
        result.append({
            'channel': row['channel'],
            'new_customers': int(row['new_customers']),
            'percentage': round(float(row['percentage']), 2)
        })
    
    # Sort by new customers descending
    result.sort(key=lambda x: x['new_customers'], reverse=True)
    
    return result


def size_distribution(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Calculate size distribution with percentages.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        list: Size distribution with counts and percentages
    """
    if df.empty:
        return []
    
    # Filter out null sizes
    size_df = df[df['Size'].notna()].copy()
    
    if size_df.empty:
        return []
    
    # Count by size
    size_counts = size_df.groupby('Size').agg({
        'Qty': 'sum'
    }).reset_index()
    
    size_counts.columns = ['size', 'quantity']
    
    # Calculate percentage
    total_quantity = size_counts['quantity'].sum()
    size_counts['percentage'] = (size_counts['quantity'] / total_quantity * 100) if total_quantity > 0 else 0
    
    # Convert to list of dicts
    result = []
    for _, row in size_counts.iterrows():
        result.append({
            'size': row['size'],
            'quantity': int(row['quantity']),
            'percentage': round(float(row['percentage']), 2)
        })
    
    # Define size order for sorting
    size_order = {'XS': 1, 'S': 2, 'M': 3, 'L': 4, 'XL': 5, 'XXL': 6, '2XL': 6, '3XL': 7, '4XL': 8}
    
    # Sort by size order
    result.sort(key=lambda x: (size_order.get(x['size'], 999), x['size']))
    
    return result


def color_preferences_by_breed(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Analyze color preferences by dog breed.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        list: Color preferences grouped by breed
    """
    if df.empty:
        return []
    
    # Filter out null values
    color_df = df[(df['Dog_Breed'].notna()) & (df['Shirt_Color'].notna())].copy()
    
    if color_df.empty:
        return []
    
    # Group by breed and color
    breed_color = color_df.groupby(['Dog_Breed', 'Shirt_Color']).agg({
        'Qty': 'sum',
        'Line_Subtotal': 'sum'
    }).reset_index()
    
    breed_color.columns = ['breed', 'color', 'quantity', 'revenue']
    
    # Get total per breed for percentage
    breed_totals = breed_color.groupby('breed')['quantity'].sum().to_dict()
    
    # Calculate percentage
    breed_color['percentage'] = breed_color.apply(
        lambda row: (row['quantity'] / breed_totals[row['breed']] * 100) if breed_totals[row['breed']] > 0 else 0,
        axis=1
    )
    
    # Convert to list of dicts
    result = []
    for _, row in breed_color.iterrows():
        result.append({
            'breed': row['breed'],
            'color': row['color'],
            'quantity': int(row['quantity']),
            'revenue': round(float(row['revenue']), 2),
            'percentage': round(float(row['percentage']), 2)
        })
    
    # Sort by breed, then by quantity descending
    result.sort(key=lambda x: (x['breed'], -x['quantity']))
    
    return result


def monthly_trends(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Calculate month-over-month sales trends.
    
    Args:
        df: Transactions dataframe
        
    Returns:
        list: Monthly metrics with growth rates
    """
    if df.empty:
        return []
    
    # Add year-month column
    monthly_df = df.copy()
    monthly_df['year_month'] = monthly_df['Order_Date'].dt.to_period('M')
    
    # Group by month
    monthly_agg = monthly_df.groupby('year_month').agg({
        'Line_Subtotal': 'sum',
        'COGS_THB': 'sum',
        'Line_Profit': 'sum',
        'Qty': 'sum',
        'Order_ID': 'nunique',
        'Customer_Name': 'nunique'
    }).reset_index()
    
    monthly_agg.columns = ['month', 'revenue', 'cost', 'profit', 'quantity', 'orders', 'customers']
    
    # Convert period to string
    monthly_agg['month'] = monthly_agg['month'].astype(str)
    
    # Calculate month-over-month growth
    monthly_agg['revenue_growth'] = monthly_agg['revenue'].pct_change() * 100
    monthly_agg['orders_growth'] = monthly_agg['orders'].pct_change() * 100
    
    # Convert to list of dicts
    result = []
    for _, row in monthly_agg.iterrows():
        result.append({
            'month': row['month'],
            'revenue': round(float(row['revenue']), 2),
            'cost': round(float(row['cost']), 2),
            'profit': round(float(row['profit']), 2),
            'quantity': int(row['quantity']),
            'orders': int(row['orders']),
            'customers': int(row['customers']),
            'revenue_growth': round(float(row['revenue_growth']), 2) if pd.notna(row['revenue_growth']) else None,
            'orders_growth': round(float(row['orders_growth']), 2) if pd.notna(row['orders_growth']) else None
        })
    
    return result
