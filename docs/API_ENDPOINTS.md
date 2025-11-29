# API Endpoints Documentation

Complete reference for all WUUF Analytics Backend endpoints.

**Base URL**: 
- Local: `http://localhost:8000`
- Production: `https://wuuf-analytics-backend-production.up.railway.app`

---

## Table of Contents

1. [Health Check Endpoints](#health-check-endpoints)
2. [Sales Analytics Endpoints](#sales-analytics-endpoints)
3. [Customer Analytics Endpoints](#customer-analytics-endpoints)
4. [Product Analytics Endpoints](#product-analytics-endpoints)
5. [Filter Options Endpoint](#filter-options-endpoint)
6. [Query Parameters](#query-parameters)
7. [Response Format](#response-format)
8. [Error Handling](#error-handling)

---

## Health Check Endpoints

### GET `/`

Health check endpoint.

**Response**:
```json
{
  "message": "WUUF Analytics API",
  "status": "healthy",
  "version": "1.0"
}
```

---

### GET `/test-connection`

Test Google Sheets connection and data loading.

**Response**:
```json
{
  "status": "success",
  "message": "Successfully loaded X transactions",
  "steps": [
    {
      "step": "1. Get Google Sheets client",
      "status": "✓"
    },
    // ... more steps
  ]
}
```

---

## Sales Analytics Endpoints

### GET `/sales/overview`

Get overall sales summary metrics.

**Query Parameters**: All optional filters (see [Query Parameters](#query-parameters))

**Response**:
```json
{
  "data": {
    "total_revenue": 67420.00,
    "total_cost": 35890.00,
    "total_profit": 31530.00,
    "total_orders": 56,
    "total_quantity": 132,
    "average_order_value": 1203.93
  },
  "cache_info": {
    "cached": true,
    "cache_timestamp": "2025-11-27T01:18:04",
    "records_count": 97,
    "cache_age_seconds": 18.9
  }
}
```

**Example with Filters**:
```bash
# Get October 2025 overview
curl "http://localhost:8000/sales/overview?start_date=2025-10-01&end_date=2025-10-31"

# Get Dachshund sales only
curl "http://localhost:8000/sales/overview?breed=Dachshund"

# Multiple filters
curl "http://localhost:8000/sales/overview?channel=Instagram&size=M&start_date=2025-11-01"
```

---

### GET `/sales/daily`

Get daily sales breakdown.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": [
    {
      "date": "2025-09-19",
      "revenue": 1380.00,
      "cost": 690.00,
      "profit": 690.00,
      "quantity": 2,
      "orders": 1
    },
    // ... more days
  ],
  "cache_info": { ... }
}
```

**Example**:
```bash
# Get daily sales for November
curl "http://localhost:8000/sales/daily?start_date=2025-11-01&end_date=2025-11-30"
```

---

### GET `/sales/monthly-trends`

Get month-over-month sales trends with growth rates.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": [
    {
      "month": "2025-09",
      "revenue": 5520.00,
      "cost": 2760.00,
      "profit": 2760.00,
      "quantity": 8,
      "orders": 4,
      "customers": 4,
      "revenue_growth": null,
      "orders_growth": null
    },
    {
      "month": "2025-10",
      "revenue": 27600.00,
      "cost": 13800.00,
      "profit": 13800.00,
      "quantity": 40,
      "orders": 20,
      "customers": 18,
      "revenue_growth": 400.00,
      "orders_growth": 400.00
    }
  ],
  "cache_info": { ... }
}
```

---

### GET `/sales/by-collection`

Get sales metrics grouped by collection.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": [
    {
      "collection": "WUUF-005",
      "revenue": 49680.00,
      "cost": 24840.00,
      "profit": 24840.00,
      "quantity": 72,
      "orders": 36
    },
    // ... more collections
  ],
  "cache_info": { ... }
}
```

**Example**:
```bash
# Get collection sales for size M only
curl "http://localhost:8000/sales/by-collection?size=M"
```

---

### GET `/sales/by-breed`

Get sales metrics grouped by dog breed.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": [
    {
      "breed": "Dachshund",
      "revenue": 33120.00,
      "cost": 16560.00,
      "profit": 16560.00,
      "quantity": 48,
      "orders": 24
    },
    // ... more breeds
  ],
  "cache_info": { ... }
}
```

---

### GET `/sales/by-size`

Get sales metrics grouped by shirt size.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": [
    {
      "size": "S",
      "revenue": 8280.00,
      "cost": 4140.00,
      "profit": 4140.00,
      "quantity": 12,
      "orders": 6
    },
    {
      "size": "M",
      "revenue": 44160.00,
      "cost": 22080.00,
      "profit": 22080.00,
      "quantity": 64,
      "orders": 32
    }
    // ... ordered by size (XS, S, M, L, XL, 2XL, 3XL)
  ],
  "cache_info": { ... }
}
```

---

## Customer Analytics Endpoints

### GET `/sales/customer-lifetime-value`

Get customer lifetime value metrics with contact information.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": [
    {
      "customer": "กมลรัตน์ ศรีสังข์สุข",
      "instagram": "ple19",
      "phone": "0910034999",
      "total_revenue": 2760.00,
      "total_profit": 1900.00,
      "total_orders": 1,
      "total_quantity": 4,
      "avg_order_value": 2760.00,
      "first_order_date": "2025-11-07T00:00:00",
      "last_order_date": "2025-11-07T00:00:00",
      "lifetime_days": 0,
      "recency_days": 20
    }
    // ... sorted by revenue descending
  ],
  "cache_info": { ... }
}
```

**Fields Explained**:
- `instagram`: Customer's Instagram handle (null if not available)
- `phone`: 10-digit Thai phone number with leading zero
- `lifetime_days`: Days between first and last order
- `recency_days`: Days since last order (lower = more recent)

**Example**:
```bash
# Get CLV for Instagram customers only
curl "http://localhost:8000/sales/customer-lifetime-value?channel=Instagram"

# Get CLV for customers who bought in October
curl "http://localhost:8000/sales/customer-lifetime-value?start_date=2025-10-01&end_date=2025-10-31"
```

---

### GET `/sales/customer-repeat-rate`

Get customer repeat purchase metrics.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": {
    "total_customers": 60,
    "repeat_customers": 10,
    "new_customers": 50,
    "repeat_rate": 16.67,
    "average_orders_per_customer": 1.22
  },
  "cache_info": { ... }
}
```

---

### GET `/sales/top-customers`

Get top N customers by revenue.

**Query Parameters**: 
- `limit` (integer, default: 10) - Number of top customers
- All optional filters

**Response**:
```json
{
  "data": [
    {
      "rank": 1,
      "customer": "กมลรัตน์ ศรีสังข์สุข",
      "total_revenue": 2760.00,
      "total_profit": 1900.00,
      "total_orders": 1,
      "total_quantity": 4
    }
    // ... up to limit
  ],
  "cache_info": { ... }
}
```

**Example**:
```bash
# Get top 5 customers
curl "http://localhost:8000/sales/top-customers?limit=5"

# Top customers who bought Dachshund products
curl "http://localhost:8000/sales/top-customers?breed=Dachshund&limit=10"
```

---

### GET `/sales/customer-acquisition`

Get customer acquisition metrics by channel.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": [
    {
      "channel": "Instagram",
      "new_customers": 45,
      "percentage": 75.00
    },
    {
      "channel": "Direct Sales",
      "new_customers": 10,
      "percentage": 16.67
    }
    // ... sorted by new_customers descending
  ],
  "cache_info": { ... }
}
```

---

## Product Analytics Endpoints

### GET `/sales/size-distribution`

Get size preference distribution with percentages.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": [
    {
      "size": "S",
      "quantity": 12,
      "percentage": 9.09
    },
    {
      "size": "M",
      "quantity": 64,
      "percentage": 48.48
    }
    // ... ordered by size (XS, S, M, L, XL, etc.)
  ],
  "cache_info": { ... }
}
```

**Example**:
```bash
# Size distribution for Dachshund products
curl "http://localhost:8000/sales/size-distribution?breed=Dachshund"
```

---

### GET `/sales/color-preferences`

Get color preferences by dog breed.

**Query Parameters**: All optional filters

**Response**:
```json
{
  "data": [
    {
      "breed": "BorderCollie",
      "color": "Navy",
      "quantity": 2,
      "revenue": 1380.00,
      "percentage": 100.00
    },
    {
      "breed": "Dachshund",
      "color": "Black",
      "quantity": 18,
      "revenue": 12420.00,
      "percentage": 37.50
    }
    // ... sorted by breed, then quantity descending
  ],
  "cache_info": { ... }
}
```

---

## Filter Options Endpoint

### GET `/sales/filter-options`

Get all available filter values from the dataset.

**Query Parameters**: None

**Response**:
```json
{
  "data": {
    "sizes": ["2XL", "3XL", "L", "M", "S", "XL"],
    "collections": ["WUUF-001", "WUUF-002", "WUUF-005", "WUUF-006", "WUUF-007"],
    "breeds": ["BorderCollie", "Dachshund", "GoldenRetriever"],
    "channels": ["Direct Sales", "Instagram", "Shopee"],
    "date_range": {
      "min_date": "2025-09-19T00:00:00",
      "max_date": "2025-11-25T00:00:00"
    }
  },
  "cache_info": { ... }
}
```

**Use Case**: Populate dropdown filters in dashboard UI.

---

## Query Parameters

All sales analytics endpoints support these optional query parameters:

| Parameter | Type | Format | Example | Description |
|-----------|------|--------|---------|-------------|
| `start_date` | string | YYYY-MM-DD | 2025-10-01 | Filter from this date (inclusive) |
| `end_date` | string | YYYY-MM-DD | 2025-10-31 | Filter to this date (inclusive) |
| `size` | string | Exact match | M | Filter by shirt size |
| `collection` | string | Exact match | WUUF-005 | Filter by collection |
| `breed` | string | Exact match | Dachshund | Filter by dog breed |
| `channel` | string | Exact match | Instagram | Filter by sales channel |

### Filter Behavior

- **Exact Match**: All filters use exact string matching (case-sensitive)
- **Combined Filters**: Multiple filters use AND logic (all must match)
- **Optional**: All filters are optional
- **Empty Result**: Returns empty data array if no matches

### Date Range Filtering

- Dates are **inclusive** on both ends
- Use ISO format: `YYYY-MM-DD`
- `end_date` includes the entire day (23:59:59)
- Invalid dates are ignored with a warning

### Available Values

Get current available values using `/sales/filter-options` endpoint.

---

## Response Format

All endpoints return a standardized JSON structure:

```json
{
  "data": {
    // Endpoint-specific data (object or array)
  },
  "cache_info": {
    "cached": true,              // Whether data is from cache
    "cache_timestamp": "...",    // ISO timestamp of cache creation
    "records_count": 97,         // Number of records in dataset
    "cache_age_seconds": 18.9    // Seconds since cache was created
  }
}
```

### Cache Information

- **Duration**: 5 minutes
- **Shared**: All endpoints share the same cache
- **Auto-refresh**: Cache refreshes automatically on expiration
- **Fallback**: Uses stale cache if Google Sheets is unavailable

---

## Error Handling

### Common Error Responses

**400 Bad Request** - Invalid filter parameters
```json
{
  "detail": "Invalid date format for start_date"
}
```

**500 Internal Server Error** - Server error
```json
{
  "detail": "Failed to load data from Google Sheets: [error message]"
}
```

**503 Service Unavailable** - Google Sheets unavailable (returns cached data if available)
```json
{
  "detail": "Using cached data due to temporary unavailability"
}
```

---

## Complete Example Workflow

```bash
# 1. Check API health
curl http://localhost:8000/

# 2. Test Google Sheets connection
curl http://localhost:8000/test-connection

# 3. Get available filter options
curl http://localhost:8000/sales/filter-options

# 4. Get overall metrics
curl http://localhost:8000/sales/overview

# 5. Filter by date range
curl "http://localhost:8000/sales/overview?start_date=2025-10-01&end_date=2025-10-31"

# 6. Get daily breakdown for October
curl "http://localhost:8000/sales/daily?start_date=2025-10-01&end_date=2025-10-31"

# 7. Analyze specific segment
curl "http://localhost:8000/sales/by-collection?breed=Dachshund&size=M&channel=Instagram"

# 8. Get customer insights
curl "http://localhost:8000/sales/customer-lifetime-value?start_date=2025-10-01"

# 9. Check repeat rate
curl http://localhost:8000/sales/customer-repeat-rate
```

---

## Rate Limiting

Currently **no rate limiting** is implemented. Consider implementing rate limiting for production use.

---

## CORS Configuration

CORS is enabled for all origins (`*`). Update in `apps/api/main.py` if needed:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

**Last Updated**: November 29, 2025
