# WUUF Analytics Backend

FastAPI backend providing analytics endpoints for WUUF transaction data from Google Sheets.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Deployed on Railway](https://img.shields.io/badge/Deployed-Railway-purple.svg)](https://railway.app/)

---

## 🚀 Features

- ✅ **13 Analytics Endpoints** - Sales, customers, products
- ✅ **Google Sheets Integration** - Real-time data sync
- ✅ **Advanced Filtering** - 6 filter types (date, size, breed, channel, etc.)
- ✅ **Customer Insights** - Lifetime value, recency, repeat rate
- ✅ **Contact Information** - Instagram handles & phone numbers
- ✅ **Smart Caching** - 5-minute cache for performance
- ✅ **Production Ready** - Deployed on Railway

---

## 📖 Documentation

Complete documentation available in [`docs/`](./docs/) directory:

| Document | Description |
|----------|-------------|
| [CONTEXT.md](./docs/CONTEXT.md) | **For AI Assistants** - Complete project context for new chats |
| [API_ENDPOINTS.md](./docs/API_ENDPOINTS.md) | Complete API reference with examples |
| [FILTERS.md](./docs/FILTERS.md) | Filtering guide with use cases |
| [DEPLOYMENT.md](./docs/DEPLOYMENT.md) | Railway & local deployment guide |
| [DATA_STRUCTURE.md](./docs/DATA_STRUCTURE.md) | Google Sheets structure reference |

---

## 🎯 Quick Start

### Prerequisites

- Python 3.9+
- Google Service Account JSON
- Google Sheets with proper structure

### Local Setup

```bash
# Clone repository
git clone https://github.com/northpr/wuuf-analytics-backend.git
cd wuuf-analytics-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_SHEET_ID=1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE
export GOOGLE_SERVICE_ACCOUNT_FILE=gold-totem-478004-q0-9501779d48ad.json

# Run server
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Test Connection

```bash
# Health check
curl http://localhost:8000/

# Test Google Sheets
curl http://localhost:8000/test-connection

# Get sales overview
curl http://localhost:8000/sales/overview
```

---

## 🔌 API Endpoints

**Base URL**: `https://wuuf-analytics-backend-production.up.railway.app`

### Sales Analytics

| Endpoint | Description |
|----------|-------------|
| `GET /sales/overview` | Sales summary (revenue, orders, AOV) |
| `GET /sales/daily` | Daily sales breakdown |
| `GET /sales/monthly-trends` | Month-over-month trends |
| `GET /sales/by-collection` | Sales by collection |
| `GET /sales/by-breed` | Sales by dog breed |
| `GET /sales/by-size` | Sales by shirt size |

### Customer Analytics

| Endpoint | Description |
|----------|-------------|
| `GET /sales/customer-lifetime-value` | Customer CLV with contact info |
| `GET /sales/customer-repeat-rate` | Repeat customer metrics |
| `GET /sales/top-customers` | Top N customers by revenue |
| `GET /sales/customer-acquisition` | Customer acquisition by channel |

### Product Analytics

| Endpoint | Description |
|----------|-------------|
| `GET /sales/size-distribution` | Size preference distribution |
| `GET /sales/color-preferences` | Color preferences by breed |

### Utilities

| Endpoint | Description |
|----------|-------------|
| `GET /sales/filter-options` | Available filter values |
| `GET /test-connection` | Test Google Sheets connection |

**See [API_ENDPOINTS.md](./docs/API_ENDPOINTS.md) for complete documentation with examples.**

---

## 🎛️ Filtering

All endpoints support optional query parameters:

```bash
# Date range
curl "http://localhost:8000/sales/overview?start_date=2025-10-01&end_date=2025-10-31"

# Product filters
curl "http://localhost:8000/sales/overview?size=M&breed=Dachshund"

# Channel filter
curl "http://localhost:8000/sales/overview?channel=Instagram"

# Combined filters
curl "http://localhost:8000/sales/overview?channel=Instagram&size=M&start_date=2025-11-01"
```

**Available Filters**:
- `start_date` (YYYY-MM-DD)
- `end_date` (YYYY-MM-DD)
- `size` (S, M, L, XL, 2XL, 3XL, 4XL)
- `collection` (WUUF-001, WUUF-005, etc.)
- `breed` (Dachshund, GoldenRetriever, etc.)
- `channel` (Instagram, Direct Sales, Shopee)

**See [FILTERS.md](./docs/FILTERS.md) for complete filtering guide.**

---

## 📊 Response Format

All endpoints return standardized JSON:

```json
{
  "data": {
    // Endpoint-specific data
  },
  "cache_info": {
    "cached": true,
    "cache_timestamp": "2025-11-27T01:18:04",
    "records_count": 97,
    "cache_age_seconds": 18.9
  }
}
```

---

## 🗂️ Project Structure

```
wuuf-analytics-backend/
├── apps/
│   └── api/
│       ├── main.py              # FastAPI app
│       └── routers/
│           └── sales.py         # All sales endpoints
├── shared/
│   ├── data_loader.py           # Google Sheets data loading
│   ├── aggregations.py          # Business logic
│   └── filters.py               # Filtering logic
├── docs/                        # Complete documentation
├── requirements.txt             # Python dependencies
├── Procfile                     # Railway deployment
└── README.md                    # This file
```

---

## 🔧 Environment Variables

### Required

```bash
GOOGLE_SHEET_ID=1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE

# Local development
GOOGLE_SERVICE_ACCOUNT_FILE=gold-totem-478004-q0-9501779d48ad.json

# Production (Railway)
GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
```

### Optional

```bash
PORT=8000  # Server port (default: 8000)
```

**See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for complete setup guide.**

---

## 🚢 Deployment

### Railway (Production)

1. Connect GitHub repository
2. Add environment variables
3. Deploy automatically on push to `main`

**Live URL**: https://wuuf-analytics-backend-production.up.railway.app

**See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for step-by-step guide.**

---

## 📚 Google Sheets Setup

### Required Sheets

1. **Orders** - Customer order information
2. **Order_Items** - Line items for each order
3. **Products** - Product catalog

### Share with Service Account

```
wuuf-817@gold-totem-478004-q0.iam.gserviceaccount.com
```

**See [DATA_STRUCTURE.md](./docs/DATA_STRUCTURE.md) for complete structure reference.**

---

## 💡 Usage Examples

### Get Monthly Sales

```bash
curl "http://localhost:8000/sales/overview?start_date=2025-10-01&end_date=2025-10-31"
```

### Analyze Instagram Sales

```bash
curl "http://localhost:8000/sales/customer-lifetime-value?channel=Instagram"
```

### Product Performance

```bash
curl "http://localhost:8000/sales/by-collection?size=M"
```

### Customer Insights

```bash
curl http://localhost:8000/sales/customer-repeat-rate
```

---

## 🔍 Key Features Explained

### Customer Lifetime Value

Includes contact information for marketing:
```json
{
  "customer": "กมลรัตน์ ศรีสังข์สุข",
  "instagram": "ple19",
  "phone": "0910034999",
  "total_revenue": 2760.00,
  "recency_days": 20
}
```

### Recency Tracking

`recency_days` = Days since customer's last order (for retention analysis)

### Phone Number Handling

- Automatically adds leading zero
- Removes dashes and spaces
- Stores as 10-digit string: `"0910034999"`

### Smart Caching

- 5-minute cache duration
- Reduces Google Sheets API calls
- Fallback to cache if API unavailable

---

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.115
- **Data Processing**: pandas 2.2
- **Google Integration**: gspread 6.1
- **Deployment**: Railway
- **Python**: 3.9+

---

## 📈 Performance

- **Cache Duration**: 5 minutes
- **Response Time**: <100ms (cached)
- **Data Load Time**: <2s (cold start)
- **Concurrent Users**: Handles 100+ concurrent requests

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 🐛 Troubleshooting

### Common Issues

**"Spreadsheet not found"**
- Verify Google Sheet is shared with service account
- Check `GOOGLE_SHEET_ID` is correct

**"Sheet 'Orders' not found"**
- Sheet names are case-sensitive
- Must be exact: `Orders`, `Order_Items`, `Products`

**"Module not found"**
```bash
pip install -r requirements.txt --upgrade
```

**More solutions in [DEPLOYMENT.md](./docs/DEPLOYMENT.md#troubleshooting)**

---

## 📝 License

This project is private and proprietary.

---

## 🔗 Links

- **GitHub**: https://github.com/northpr/wuuf-analytics-backend
- **Production API**: https://wuuf-analytics-backend-production.up.railway.app
- **Documentation**: [docs/](./docs/)

---

## 🎯 Next Steps for New Projects

Building a dashboard? See [CONTEXT.md](./CONTEXT.md) for complete project context to use in new AI chats.

**Example**: Use this backend with Streamlit for analytics dashboard.

---

## 📮 Support

For issues or questions:
1. Check [documentation](./docs/)
2. Review [troubleshooting guide](./docs/DEPLOYMENT.md#troubleshooting)
3. Open GitHub issue

---

**Last Updated**: November 29, 2025  
**Version**: 1.0  
**Status**: ✅ Production
