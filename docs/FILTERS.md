# Filtering Guide

Complete guide to using filters in WUUF Analytics Backend.

---

## Overview

All sales analytics endpoints support **6 optional query parameters** for filtering data:

1. `start_date` - Date range start
2. `end_date` - Date range end
3. `size` - Shirt size
4. `collection` - Product collection
5. `breed` - Dog breed
6. `channel` - Sales channel

---

## Filter Parameters

### Date Range Filters

#### `start_date`

Filter transactions from this date onwards (inclusive).

**Format**: `YYYY-MM-DD` (ISO 8601)

**Example**:
```bash
curl "http://localhost:8000/sales/overview?start_date=2025-10-01"
```

**Behavior**:
- Inclusive (includes orders on this date)
- Orders with `Order_Date >= start_date`
- Invalid dates are ignored with warning

---

#### `end_date`

Filter transactions up to this date (inclusive).

**Format**: `YYYY-MM-DD` (ISO 8601)

**Example**:
```bash
curl "http://localhost:8000/sales/overview?end_date=2025-10-31"
```

**Behavior**:
- Inclusive (includes entire day: 23:59:59)
- Orders with `Order_Date <= end_date + 1 day - 1 second`
- Invalid dates are ignored with warning

---

### Product Filters

#### `size`

Filter by shirt size (exact match, case-sensitive).

**Available Values**: `S`, `M`, `L`, `XL`, `2XL`, `3XL`, `4XL`

**Example**:
```bash
curl "http://localhost:8000/sales/overview?size=M"
```

**Behavior**:
- Exact string match
- Case-sensitive: `M` ≠ `m`
- Only returns orders containing this size

---

#### `collection`

Filter by product collection (exact match).

**Available Values**: `WUUF-001`, `WUUF-002`, `WUUF-005`, `WUUF-006`, `WUUF-007`, etc.

**Example**:
```bash
curl "http://localhost:8000/sales/overview?collection=WUUF-005"
```

**Behavior**:
- Exact string match
- Collection extracted from SKU
- Format: `WUUF-XXX`

---

#### `breed`

Filter by dog breed (exact match).

**Available Values**: `Dachshund`, `GoldenRetriever`, `BorderCollie`, etc.

**Example**:
```bash
curl "http://localhost:8000/sales/overview?breed=Dachshund"
```

**Behavior**:
- Exact string match
- Case-sensitive: `Dachshund` ≠ `dachshund`
- Based on product dog breed

---

### Sales Channel Filter

#### `channel`

Filter by sales channel (exact match).

**Available Values**: `Instagram`, `Direct Sales`, `Shopee`, etc.

**Example**:
```bash
curl "http://localhost:8000/sales/overview?channel=Instagram"
```

**Behavior**:
- Exact string match
- Case-sensitive
- Based on order channel

---

## Combining Filters

### Multiple Filters (AND Logic)

All filters use **AND logic** - ALL conditions must match.

**Example**: Instagram sales of size M Dachshund products in October
```bash
curl "http://localhost:8000/sales/overview?channel=Instagram&size=M&breed=Dachshund&start_date=2025-10-01&end_date=2025-10-31"
```

**Result**: Only returns orders that match **ALL** criteria:
- ✅ Channel = Instagram
- ✅ Size = M
- ✅ Breed = Dachshund
- ✅ Date between Oct 1-31, 2025

---

## Getting Available Filter Values

Use `/sales/filter-options` to get all current values:

```bash
curl http://localhost:8000/sales/filter-options
```

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
  }
}
```

**Use Case**: Populate dropdown filters in dashboard UI.

---

## Filter Examples by Use Case

### Monthly Analysis

Get sales for specific month:
```bash
curl "http://localhost:8000/sales/overview?start_date=2025-10-01&end_date=2025-10-31"
```

### Product Performance

Analyze specific collection:
```bash
curl "http://localhost:8000/sales/by-size?collection=WUUF-005"
```

### Channel Analysis

Compare channels for specific breed:
```bash
# Instagram
curl "http://localhost:8000/sales/overview?breed=Dachshund&channel=Instagram"

# Direct Sales
curl "http://localhost:8000/sales/overview?breed=Dachshund&channel=Direct Sales"
```

### Size Preferences by Breed

Get size distribution for Dachshund:
```bash
curl "http://localhost:8000/sales/size-distribution?breed=Dachshund"
```

### Customer Analysis

Get CLV for customers who bought in Q4:
```bash
curl "http://localhost:8000/sales/customer-lifetime-value?start_date=2025-10-01&end_date=2025-12-31"
```

### Daily Performance

Track daily sales for current month:
```bash
curl "http://localhost:8000/sales/daily?start_date=2025-11-01&end_date=2025-11-30"
```

---

## Filter Behavior Details

### Empty Results

If no records match the filters, endpoints return empty data:

```json
{
  "data": [],
  "cache_info": { ... }
}
```

or for overview:
```json
{
  "data": {
    "total_revenue": 0.0,
    "total_cost": 0.0,
    "total_profit": 0.0,
    "total_orders": 0,
    "total_quantity": 0,
    "average_order_value": 0.0
  },
  "cache_info": { ... }
}
```

---

### Invalid Filters

**Invalid Date Format**:
```bash
curl "http://localhost:8000/sales/overview?start_date=invalid"
```
- Warning logged
- Filter ignored
- No error returned

**Non-existent Value**:
```bash
curl "http://localhost:8000/sales/overview?breed=NonExistentBreed"
```
- Returns empty results
- No error

**Case Mismatch**:
```bash
# Wrong (lowercase)
curl "http://localhost:8000/sales/overview?breed=dachshund"  # Empty results

# Correct (proper case)
curl "http://localhost:8000/sales/overview?breed=Dachshund"  # Works
```

---

## Implementation Details

### Filter Function

Located in `shared/filters.py`:

```python
def apply_filters(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    size: Optional[str] = None,
    collection: Optional[str] = None,
    breed: Optional[str] = None,
    channel: Optional[str] = None
) -> pd.DataFrame
```

### How It Works

1. **Date Filtering**: Converts strings to datetime, filters by `Order_Date`
2. **String Filtering**: Exact match on specified columns
3. **Chaining**: Applies filters sequentially (AND logic)
4. **Error Handling**: Invalid values log warnings but don't break

---

## Best Practices

### 1. Always Check Available Values First

```bash
# Get current options
curl http://localhost:8000/sales/filter-options

# Then use exact values
curl "http://localhost:8000/sales/overview?breed=Dachshund"
```

### 2. Use Date Ranges for Time Analysis

```bash
# Month-to-date
curl "http://localhost:8000/sales/daily?start_date=2025-11-01&end_date=2025-11-30"

# Year-to-date
curl "http://localhost:8000/sales/monthly-trends?start_date=2025-01-01"
```

### 3. Combine Filters for Segmentation

```bash
# High-value segment
curl "http://localhost:8000/sales/customer-lifetime-value?channel=Instagram&breed=Dachshund"

# Product analysis
curl "http://localhost:8000/sales/by-size?collection=WUUF-005&start_date=2025-10-01"
```

### 4. Use Appropriate Endpoints

Choose the right endpoint for your filter needs:
- `by-collection`: Already grouped, no need for collection filter
- `by-breed`: Already grouped, no need for breed filter
- `by-size`: Already grouped, no need for size filter

---

## Dashboard Integration

### Example: Streamlit Filter UI

```python
import streamlit as st
import requests

# Get filter options
options = requests.get(f"{API_URL}/sales/filter-options").json()["data"]

# Create filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
size = st.sidebar.selectbox("Size", ["All"] + options["sizes"])
breed = st.sidebar.selectbox("Breed", ["All"] + options["breeds"])
channel = st.sidebar.selectbox("Channel", ["All"] + options["channels"])

# Build query parameters
params = {}
if start_date:
    params["start_date"] = start_date.isoformat()
if end_date:
    params["end_date"] = end_date.isoformat()
if size != "All":
    params["size"] = size
if breed != "All":
    params["breed"] = breed
if channel != "All":
    params["channel"] = channel

# Fetch filtered data
response = requests.get(f"{API_URL}/sales/overview", params=params)
data = response.json()["data"]
```

---

## Performance Considerations

### Caching

- Filters applied **after** cache retrieval
- Cache shared across all filter combinations
- No performance penalty for different filters

### Response Time

- Filtering is fast (in-memory pandas operations)
- Date filtering: ~1-5ms
- String filtering: ~1-5ms
- Combined filters: Still <10ms

---

## Common Filter Combinations

### Sales Reports

```bash
# Weekly report
curl "http://localhost:8000/sales/overview?start_date=2025-11-18&end_date=2025-11-24"

# Monthly by collection
curl "http://localhost:8000/sales/by-collection?start_date=2025-10-01&end_date=2025-10-31"
```

### Customer Analysis

```bash
# Instagram customers
curl "http://localhost:8000/sales/customer-lifetime-value?channel=Instagram"

# Repeat customers in date range
curl "http://localhost:8000/sales/customer-repeat-rate?start_date=2025-10-01"
```

### Product Analysis

```bash
# Size preference by breed
curl "http://localhost:8000/sales/size-distribution?breed=Dachshund"

# Color preference by collection
curl "http://localhost:8000/sales/color-preferences?collection=WUUF-005"
```

---

**Last Updated**: November 29, 2025
