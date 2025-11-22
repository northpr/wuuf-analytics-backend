# WUUF Analytics Backend

FastAPI backend for WUUF transaction analytics from Google Sheets. This backend loads transaction data from three Google Sheets, joins them, applies filters, and provides analytics endpoints for sales data visualization.

## Features

- 📊 Load data from Google Sheets (Orders, Order_Items, Products)
- 🔗 Automatic data joining and transformation
- 🎯 Flexible filtering (date range, size, collection, breed, channel)
- 📈 Multiple analytics endpoints (overview, daily, by-collection, by-breed, by-size)
- ⚡ Data caching (5-minute cache to reduce API calls)
- 🚀 Ready for Railway deployment
- 📝 Auto-generated API documentation (Swagger UI)

## Project Structure

```
wuuf-analytics-backend/
├── apps/
│   └── api/
│       ├── main.py              # FastAPI entry point
│       └── routers/
│           └── sales.py         # Sales endpoints
├── shared/
│   ├── data_loader.py           # Google Sheets loader + join logic
│   ├── filters.py               # Filtering functionality
│   └── aggregations.py          # Analytics calculations
├── gold-totem-478004-q0-9501779d48ad.json  # Service account credentials
├── requirements.txt             # Python dependencies
├── Procfile                     # Railway deployment config
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Prerequisites

1. **Google Cloud Project** with Google Sheets API enabled
2. **Service Account** with JSON credentials
3. **Python 3.9+**
4. **Google Sheet** with three worksheets: Orders, Order_Items, Products

## Google Sheets Setup

### 1. Create Google Cloud Project & Enable API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable "Google Sheets API":
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### 2. Create Service Account

1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Fill in details:
   - Name: `wuuf-analytics` (or any name)
   - Description: `Service account for WUUF analytics backend`
4. Click "Create and Continue"
5. Skip role assignment (click "Continue")
6. Click "Done"

### 3. Generate JSON Key

1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select "JSON" format
5. Click "Create"
6. Save the downloaded JSON file as `gold-totem-478004-q0-9501779d48ad.json` in the project root

### 4. Share Google Sheet

**IMPORTANT:** You must share your Google Sheet with the service account email!

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE/edit
2. Click the "Share" button (top right)
3. Add the service account email (found in the JSON file under `client_email`):
   ```
   wuuf-817@gold-totem-478004-q0.iam.gserviceaccount.com
   ```
4. Set permission to "Viewer"
5. Click "Send"

### 5. Verify Sheet Structure

Ensure your Google Sheet has these three worksheets with exact column names:

**Sheet: Orders**
- Order_ID (string)
- Order_Date (date)
- Channel (string)
- Customer_Name (string)
- Instagram (string)
- Phone (string)
- Address (string)

**Sheet: Order_Items**
- Order_ID (string)
- Line# (number)
- SKU (string)
- Qty (number)
- Unit_Price_THB (number)
- Line_Subtotal (number)
- COGS_THB (number)
- Line_Profit (number)
- Shirt_Color (string)
- Size (string)

**Sheet: Products**
- SKU (string)
- Product_Name (string)
- T_Shirt_Color (string)
- Size (string)
- Price_THB (number)
- Cost_THB (number)
- Active (boolean)
- Dog_Breed (string)
- Print_File_Link (string)
- Mockup_Link (string)

## Local Development Setup

### 1. Clone Repository

```bash
cd /path/to/project
# Files should already be in: /Users/pataweeratanaruengwatna/Desktop/Code/wuuf-analyrics-backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file (optional, defaults are already set):

```bash
cp .env.example .env
```

Edit `.env` if needed:
```
GOOGLE_SHEET_ID=1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE
GOOGLE_SERVICE_ACCOUNT_FILE=gold-totem-478004-q0-9501779d48ad.json
PORT=8000
```

### 5. Run Development Server

```bash
# Option 1: Using uvicorn with proper module path
PYTHONPATH=. uvicorn apps.api.main:app --reload --port 8000

# Option 2: Using python directly
python apps/api/main.py
```

### 6. Access API

- **API Base URL:** http://localhost:8000
- **Interactive Docs (Swagger UI):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## API Endpoints

### Health & Info

- `GET /` - API information and endpoint list
- `GET /health` - Health check with cache status

### Sales Analytics

All endpoints support optional query parameters for filtering:
- `start_date` (YYYY-MM-DD) - Filter by start date
- `end_date` (YYYY-MM-DD) - Filter by end date
- `size` - Filter by exact size
- `collection` - Filter by exact collection
- `breed` - Filter by exact dog breed
- `channel` - Filter by exact channel

#### Endpoints

1. **GET /sales/overview**
   - Overall sales summary metrics
   - Returns: total_revenue, total_cost, total_profit, total_orders, total_quantity, average_order_value

2. **GET /sales/daily**
   - Daily sales metrics grouped by date
   - Returns: List of daily metrics (date, revenue, cost, profit, quantity, orders)

3. **GET /sales/by-collection**
   - Sales metrics grouped by collection
   - Returns: List of collection metrics sorted by revenue (descending)

4. **GET /sales/by-breed**
   - Sales metrics grouped by dog breed
   - Returns: List of breed metrics sorted by revenue (descending)

5. **GET /sales/by-size**
   - Sales metrics grouped by size
   - Returns: List of size metrics sorted by size order

6. **GET /sales/filter-options**
   - Get available filter options from dataset
   - Returns: Available sizes, collections, breeds, channels, and date range

### Customer Analytics

7. **GET /sales/customer-repeat-rate**
   - Calculate customer repeat purchase rate
   - Returns: total_customers, repeat_customers, new_customers, repeat_rate, average_orders_per_customer

8. **GET /sales/customer-lifetime-value**
   - Calculate customer lifetime value for all customers
   - Returns: List of customers with total revenue, profit, orders, lifetime metrics

9. **GET /sales/top-customers**
   - Get top customers by revenue (default: top 10)
   - Query parameter: `limit` (1-100, default: 10)
   - Returns: Ranked list of top customers

10. **GET /sales/customer-acquisition**
    - Analyze customer acquisition by channel
    - Returns: New customer counts and percentages by channel

### Product Insights

11. **GET /sales/size-distribution**
    - Calculate size distribution with percentages
    - Returns: List of sizes with quantity and percentage breakdown

12. **GET /sales/color-preferences**
    - Analyze color preferences by dog breed
    - Returns: Breed-color combinations with quantity, revenue, and percentage

### Growth Analytics

13. **GET /sales/monthly-trends**
    - Calculate month-over-month sales trends and growth rates
    - Returns: Monthly metrics with revenue, orders, customers, and growth percentages

### Example API Calls

```bash
# Get overall sales overview
curl http://localhost:8000/sales/overview

# Get sales filtered by date range
curl "http://localhost:8000/sales/overview?start_date=2024-01-01&end_date=2024-12-31"

# Get sales filtered by channel and size
curl "http://localhost:8000/sales/daily?channel=Instagram&size=M"

# Get sales by collection filtered by breed
curl "http://localhost:8000/sales/by-collection?breed=Corgi"

# Get available filter options
curl http://localhost:8000/sales/filter-options

# Customer Analytics
# Get customer repeat rate
curl http://localhost:8000/sales/customer-repeat-rate

# Get top 5 customers
curl "http://localhost:8000/sales/top-customers?limit=5"

# Get customer acquisition by channel
curl http://localhost:8000/sales/customer-acquisition

# Get customer lifetime value
curl http://localhost:8000/sales/customer-lifetime-value

# Product Insights
# Get size distribution
curl http://localhost:8000/sales/size-distribution

# Get color preferences by breed
curl http://localhost:8000/sales/color-preferences

# Growth Analytics
# Get monthly trends
curl http://localhost:8000/sales/monthly-trends

# Combined filters example
curl "http://localhost:8000/sales/monthly-trends?channel=Instagram&breed=Dachshund"
```

## Railway Deployment

### 1. Install Railway CLI (optional)

```bash
npm install -g @railway/cli
# or
brew install railway
```

### 2. Login to Railway

```bash
railway login
```

### 3. Initialize Project

```bash
railway init
```

### 4. Set Environment Variables

In Railway dashboard or via CLI:

```bash
# Set Google Sheet ID
railway variables set GOOGLE_SHEET_ID=1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE

# Set service account JSON (paste entire JSON content as one line)
railway variables set GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":"gold-totem-478004-q0",...}'
```

**Important:** For `GOOGLE_SERVICE_ACCOUNT_JSON`, copy the entire content of your JSON file and paste it as a single-line string.

### 5. Deploy

```bash
railway up
```

Or connect your GitHub repository in Railway dashboard for automatic deployments.

### 6. Access Deployed API

Railway will provide a public URL like: `https://your-app.railway.app`

- API Docs: `https://your-app.railway.app/docs`
- Health Check: `https://your-app.railway.app/health`

## Data Caching

The backend implements a 5-minute cache to reduce Google Sheets API calls:

- First request loads fresh data from Google Sheets
- Subsequent requests within 5 minutes use cached data
- Cache automatically refreshes after 5 minutes
- Cache info included in all API responses

To force refresh cache, restart the server or wait for cache expiration.

## Troubleshooting

### Error: "Service account file not found"

- Ensure `gold-totem-478004-q0-9501779d48ad.json` is in the project root
- Check file permissions

### Error: "Worksheet not found"

- Verify sheet names are exactly: `Orders`, `Order_Items`, `Products`
- Check spelling and capitalization

### Error: "Permission denied" or "403 Forbidden"

- Ensure you've shared the Google Sheet with the service account email
- Verify the service account has at least "Viewer" permission

### Error: "API key not valid"

- Check that Google Sheets API is enabled in Google Cloud Console
- Verify service account JSON is valid and not corrupted

### Empty Data / No Results

- Check that your Google Sheet has data in all three worksheets
- Verify column names match exactly (case-sensitive)
- Check data types (dates should be formatted as dates, numbers as numbers)

## Development Notes

### SKU Collection Extraction

Collections are extracted from SKU using pattern `WUUF-XXX`:
- Example: `WUUF-001-WH-M` → Collection: `WUUF-001`
- Uses regex pattern: `r"(WUUF-\d{3})"`
- Falls back to first two parts joined by hyphen

### Date Filtering

- Dates are parsed flexibly (ISO format recommended: YYYY-MM-DD)
- End date includes the entire day (23:59:59)
- Invalid dates are logged and skipped (no error thrown)

### Size Ordering

Sizes are sorted in order: XS, S, M, L, XL, XXL/2XL, 3XL

## Security Notes

- **Never commit** `gold-totem-478004-q0-9501779d48ad.json` to version control
- The file is already in `.gitignore`
- For Railway, use environment variable instead of file
- Service account should only have "Viewer" permission on the sheet

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify Google Sheets setup and permissions
3. Check API documentation at `/docs`
4. Review server logs for error details

## License

Private project - All rights reserved
