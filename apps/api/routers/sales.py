"""
Sales analytics router for WUUF Analytics Backend
Provides endpoints for sales data and analytics
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from shared.data_loader import load_transactions, get_cache_info
from shared.filters import apply_filters, get_filter_options
from shared.aggregations import (
    sales_overview,
    daily_sales,
    sales_by_collection,
    sales_by_breed,
    sales_by_size,
    customer_repeat_rate,
    customer_lifetime_value,
    top_customers,
    customer_acquisition_by_channel,
    size_distribution,
    color_preferences_by_breed,
    monthly_trends
)

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/overview")
async def get_sales_overview(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Get overall sales overview metrics.
    
    Returns:
        - total_revenue: Total revenue
        - total_cost: Total cost
        - total_profit: Total profit
        - total_orders: Number of unique orders
        - total_quantity: Total quantity sold
        - average_order_value: Average order value
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate overview
        overview = sales_overview(df)
        
        return {
            "data": overview,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/daily")
async def get_daily_sales(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Get daily sales metrics grouped by date.
    
    Returns:
        List of daily metrics with date, revenue, cost, profit, quantity, and orders
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate daily sales
        daily = daily_sales(df)
        
        return {
            "data": daily,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-collection")
async def get_sales_by_collection(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Get sales metrics grouped by collection.
    
    Returns:
        List of collection metrics with collection name, revenue, cost, profit, quantity, and orders
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate sales by collection
        by_collection = sales_by_collection(df)
        
        return {
            "data": by_collection,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-breed")
async def get_sales_by_breed(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Get sales metrics grouped by dog breed.
    
    Returns:
        List of breed metrics with breed name, revenue, cost, profit, quantity, and orders
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate sales by breed
        by_breed = sales_by_breed(df)
        
        return {
            "data": by_breed,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-size")
async def get_sales_by_size(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Get sales metrics grouped by size.
    
    Returns:
        List of size metrics with size, revenue, cost, profit, quantity, and orders
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate sales by size
        by_size = sales_by_size(df)
        
        return {
            "data": by_size,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/filter-options")
async def get_available_filter_options():
    """
    Get available filter options from the current dataset.
    Useful for populating dropdowns in the frontend.
    
    Returns:
        Available options for sizes, collections, breeds, channels, and date range
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Get filter options
        options = get_filter_options(df)
        
        return {
            "data": options,
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer-repeat-rate")
async def get_customer_repeat_rate(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Calculate customer repeat purchase rate.
    
    Returns:
        - total_customers: Total unique customers
        - repeat_customers: Number of customers with >1 order
        - new_customers: Number of customers with 1 order
        - repeat_rate: Percentage of repeat customers
        - average_orders_per_customer: Average number of orders per customer
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate repeat rate
        repeat_rate = customer_repeat_rate(df)
        
        return {
            "data": repeat_rate,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer-lifetime-value")
async def get_customer_lifetime_value(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Calculate customer lifetime value for all customers.
    
    Returns:
        List of customers with their total revenue, profit, orders, and lifetime metrics
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate CLV
        clv = customer_lifetime_value(df)
        
        return {
            "data": clv,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-customers")
async def get_top_customers(
    limit: int = Query(10, description="Number of top customers to return", ge=1, le=100),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Get top customers by revenue.
    
    Returns:
        List of top customers ranked by total revenue
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Get top customers
        top = top_customers(df, limit)
        
        return {
            "data": top,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel,
                "limit": limit
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer-acquisition")
async def get_customer_acquisition(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Analyze customer acquisition by channel.
    
    Returns:
        List of channels with new customer counts and percentages
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate acquisition
        acquisition = customer_acquisition_by_channel(df)
        
        return {
            "data": acquisition,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/size-distribution")
async def get_size_distribution(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Calculate size distribution with percentages.
    
    Returns:
        List of sizes with quantity and percentage breakdown
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate distribution
        distribution = size_distribution(df)
        
        return {
            "data": distribution,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/color-preferences")
async def get_color_preferences(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Analyze color preferences by dog breed.
    
    Returns:
        List of breed-color combinations with quantity, revenue, and percentage
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate preferences
        preferences = color_preferences_by_breed(df)
        
        return {
            "data": preferences,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monthly-trends")
async def get_monthly_trends(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    collection: Optional[str] = Query(None, description="Filter by collection"),
    breed: Optional[str] = Query(None, description="Filter by dog breed"),
    channel: Optional[str] = Query(None, description="Filter by channel")
):
    """
    Calculate month-over-month sales trends and growth rates.
    
    Returns:
        List of monthly metrics with revenue, orders, customers, and growth percentages
    """
    try:
        # Load transactions
        df = load_transactions()
        
        # Apply filters
        df = apply_filters(df, start_date, end_date, size, collection, breed, channel)
        
        # Calculate trends
        trends = monthly_trends(df)
        
        return {
            "data": trends,
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "size": size,
                "collection": collection,
                "breed": breed,
                "channel": channel
            },
            "cache_info": get_cache_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
