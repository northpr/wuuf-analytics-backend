# WUUF Analytics Backend - AI Assistant Context

> **Purpose**: This file provides complete context for AI assistants working on new chats/projects related to this backend.

## Project Overview

**FastAPI backend for WUUF transaction analytics** from Google Sheets. Provides 13 analytics endpoints with filtering, caching, and real-time data synchronization.

**Repository**: https://github.com/northpr/wuuf-analytics-backend.git

---

## Tech Stack

- **Framework**: FastAPI (Python 3.9+)
- **Data Processing**: pandas, numpy
- **Google Integration**: gspread, google-auth
- **Deployment**: Railway
- **Data Source**: Google Sheets

---

## Project Structure

```
/wuuf-analytics-backend/
├── apps/
│   └── api/
│       ├── main.py                    # FastAPI app entry point
│       └── routers/
│           └── sales.py               # All 13 sales endpoints
├── shared/
│   ├── data_loader.py                 # Google Sheets data loading
│   ├── aggregations.py                # Business logic & calculations
│   └── filters.py                     # Filtering logic
├── docs/                              # Complete documentation
├── requirements.txt                   # Python dependencies
├── Procfile                           # Railway deployment config
├── .env.example                       # Environment variables template
└── README.md                          # Project overview
```

---

## Key Files & Their Purpose

### `apps/api/main.py`
- FastAPI application initialization
- CORS configuration
- Router registration
- Health check endpoint

### `apps/api/routers/sales.py`
- **13 analytics endpoints**
- All accept optional query parameters for filtering
- Returns JSON with data + cache info
- Standardized response format

### `shared/data_loader.py`
- Loads data from Google Sheets
- Joins Orders, Order_Items, Products tables
- **5-minute cache** to minimize API calls
- Phone number cleaning (adds leading zero for Thai numbers)
- Instagram handle extraction

### `shared/aggregations.py`
- Business logic for all analytics
- Customer lifetime value calculations
- Recency tracking (days since last order)
- Revenue, profit, quantity aggregations
- Date-based metrics (daily, monthly)

### `shared/filters.py`
- 6 filter types: date range, size, collection, breed, channel
- Exact match filtering
- Returns available filter options

---

## API Endpoints (13 Total)

All endpoints support these optional query parameters:
- `start_date` (YYYY-MM-DD)
- `end_date` (YYYY-MM-DD)
- `size` (S, M, L, XL, 2XL, 3XL, 4XL)
- `collection` (WUUF-001, WUUF-002, etc.)
- `breed` (Dachshund, GoldenRetriever, BorderCollie, etc.)
- `channel` (Instagram, Direct Sales, Shopee)

### Endpoints:
1. `GET /` - Health check
2. `GET /test-connection` - Test Google Sheets connection
3. `GET /sales/overview` - Sales summary (revenue, orders, AOV)
4. `GET /sales/daily` - Daily sales breakdown
5. `GET /sales/monthly-trends` - Month-over-month trends
6. `GET /sales/by-collection` - Sales by collection
7. `GET /sales/by-breed` - Sales by dog breed
8. `GET /sales/by-size` - Sales by shirt size
9. `GET /sales/customer-lifetime-value` - Customer CLV with contact info
10. `GET /sales/customer-repeat-rate` - Repeat customer metrics
11. `GET /sales/top-customers` - Top N customers by revenue
12. `GET /sales/customer-acquisition` - Customer acquisition by channel
13. `GET /sales/size-distribution` - Size preference distribution
14. `GET /sales/color-preferences` - Color preferences by breed
15. `GET /sales/filter-options` - Available filter values

---

## Data Model

### Google Sheets Structure

**Sheet ID**: `1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE`

**Required Sheets**:
1. **Orders** - Customer orders
   - Order_ID, Order_Date, Channel, Customer_Name, Instagram, Phone
2. **Order_Items** - Line items
   - Order_ID, SKU, Shirt_Color, Size, Qty, Unit_Price_THB, Line_Subtotal, COGS_THB, Line_Profit
3. **Products** - Product catalog
   - SKU, Product_Name, Dog_Breed

### Joined Transaction Format

After joining all sheets:
```python
{
  'Order_Date': datetime,
  'Order_ID': str,
  'Channel': str,
  'Customer_Name': str,
  'Instagram': str,          # Customer's Instagram handle
  'Phone': str,              # 10-digit Thai phone (0XXXXXXXXX)
  'SKU': str,
  'Collection': str,         # Extracted from SKU (WUUF-XXX)
  'Product_Name': str,
  'Dog_Breed': str,
  'Shirt_Color': str,
  'Size': str,
  'Qty': int,
  'Unit_Price_THB': float,
  'Line_Subtotal': float,
  'COGS_THB': float,
  'Line_Profit': float
}
```

---

## Important Implementation Details

### Phone Number Handling
- Stored as **strings** (not integers)
- **10 digits** with leading zero: `"0910034999"`
- Removes dashes and spaces from source data
- Auto-adds leading zero if 9 digits

### Customer Metrics
- **lifetime_days**: Days between first and last order
- **recency_days**: Days since last order (from today)
- **avg_order_value**: Total revenue / total orders
- **total_quantity**: Sum of all items purchased

### Caching System
- **Duration**: 5 minutes
- **Scope**: Global (all endpoints share cache)
- **Refresh**: Automatic on cache expiration
- **Manual refresh**: Use `force_refresh=true` (if implemented)

### Collections
- Extracted from SKU using regex: `WUUF-\d{3}`
- Example: `WUUF-005-WH-M` → `WUUF-005`

---

## Environment Variables

```bash
# Required
GOOGLE_SHEET_ID=1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE

# One of these (Railway uses JSON, local uses FILE)
GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'  # Railway
GOOGLE_SERVICE_ACCOUNT_FILE=gold-totem-478004-q0-9501779d48ad.json  # Local

# Optional
PORT=8000  # Default port
```

### Service Account Email
`wuuf-817@gold-totem-478004-q0.iam.gserviceaccount.com`

**Important**: Google Sheet must be shared with this service account!

---

## Deployment

### Railway
- **Auto-deploys** from `main` branch
- Uses `Procfile` for start command
- Environment variables set in Railway dashboard
- Production URL: `https://wuuf-analytics-backend-production.up.railway.app`

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_SHEET_ID=1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE
export GOOGLE_SERVICE_ACCOUNT_FILE=gold-totem-478004-q0-9501779d48ad.json

# Run server
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Response Format

All endpoints return this structure:
```json
{
  "data": { ... },           // Endpoint-specific data
  "cache_info": {            // Cache metadata
    "cached": true,
    "cache_timestamp": "2025-11-27T01:18:04.126928",
    "records_count": 97,
    "cache_age_seconds": 18.9
  }
}
```

---

## Common Patterns

### Adding New Endpoint
1. Add function to `shared/aggregations.py`
2. Add route in `apps/api/routers/sales.py`
3. Apply filters using `apply_filters()`
4. Return data with cache info

### Date Filtering
```python
from shared.filters import apply_filters

filtered_df = apply_filters(
    df,
    start_date=start_date,
    end_date=end_date
)
```

### Error Handling
- Google Sheets errors return clear messages
- Uses fallback to cache if refresh fails
- Validates dates before filtering

---

## Dependencies

Key packages in `requirements.txt`:
```
fastapi==0.115.5
uvicorn==0.32.1
pandas==2.2.3
gspread==6.1.4
google-auth==2.37.0
python-dotenv==1.0.1
```

---

## Quick Reference Commands

```bash
# Test API locally
curl http://localhost:8000/

# Test with filters
curl "http://localhost:8000/sales/overview?start_date=2025-10-01&end_date=2025-10-31"

# Get filter options
curl http://localhost:8000/sales/filter-options

# Test Google Sheets connection
curl http://localhost:8000/test-connection
```

---

## Future AI Assistant: Next Steps

When starting a new chat to work on this project:

1. Share this CONTEXT.md file
2. Specify what you want to build (e.g., "Build Streamlit dashboard")
3. Reference specific endpoints needed
4. Ask for architecture recommendations

**Example prompt**:
```
I have a FastAPI backend with 13 analytics endpoints (see CONTEXT.md below).
I need to build a Streamlit dashboard with:
- Overview page showing KPIs
- Sales charts (daily, by collection)
- Customer table with filtering

[Paste CONTEXT.md content]

Can you help me structure the Streamlit project?
```

---

## Contact & Support

- **GitHub**: https://github.com/northpr/wuuf-analytics-backend
- **Deployment**: Railway
- **Data Source**: Google Sheets (read-only)

---

**Last Updated**: November 29, 2025
**Backend Version**: 1.0
**API Endpoints**: 13
