# Data Structure

Complete reference for Google Sheets data structure required by WUUF Analytics Backend.

---

## Overview

The backend loads data from **3 Google Sheets** and joins them to create a unified transaction dataset.

**Sheet ID**: `1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE`

---

## Required Sheets

Three sheets must exist with exact names (case-sensitive):

1. `Orders` - Customer order information
2. `Order_Items` - Line items for each order
3. `Products` - Product catalog

---

## Sheet 1: Orders

Customer order master data.

### Required Columns

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| `Order_ID` | string | Unique order identifier | `ORD-2025-001` |
| `Order_Date` | date | Order date | `2025-11-07` |
| `Channel` | string | Sales channel | `Instagram` |
| `Customer_Name` | string | Customer full name | `กมลรัตน์ ศรีสังข์สุข` |
| `Instagram` | string | Customer Instagram handle | `ple19` |
| `Phone` | string | Customer phone number | `091-003-4999` or `0910034999` |

### Data Format Details

**Order_Date**:
- Format: Any date format Google Sheets recognizes
- Will be converted to ISO datetime

**Phone**:
- Can include dashes: `091-003-4999`
- Dashes auto-removed by backend
- Leading zero auto-added if 9 digits
- Final format: `0910034999` (10 digits)

**Instagram**:
- Optional (can be empty)
- Without @ symbol
- Example: `ple19` not `@ple19`

**Channel**:
- Common values: `Instagram`, `Direct Sales`, `Shopee`
- Case-sensitive

### Example Data

| Order_ID | Order_Date | Channel | Customer_Name | Instagram | Phone |
|----------|------------|---------|---------------|-----------|-------|
| ORD-001 | 2025-11-07 | Instagram | กมลรัตน์ ศรีสังข์สุข | ple19 | 091-003-4999 |
| ORD-002 | 2025-11-08 | Direct Sales | นายรัชภูมิ สีหะเตโช | leela9718 | 0802573964 |

---

## Sheet 2: Order_Items

Line items for each order.

### Required Columns

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| `Order_ID` | string | Links to Orders sheet | `ORD-2025-001` |
| `SKU` | string | Product SKU | `WUUF-005-BK-M` |
| `Shirt_Color` | string | Product color | `Black` |
| `Size` | string | Shirt size | `M` |
| `Qty` | integer | Quantity ordered | `2` |
| `Unit_Price_THB` | number | Price per unit in THB | `690.00` |
| `Line_Subtotal` | number | Line total (Qty × Price) | `1380.00` |
| `COGS_THB` | number | Cost of goods sold in THB | `345.00` |
| `Line_Profit` | number | Profit (Subtotal - COGS) | `1035.00` |

### Data Format Details

**SKU Format**:
- Pattern: `WUUF-XXX-YY-Z`
- Collection extracted: `WUUF-XXX`
- Example: `WUUF-005-BK-M` → Collection: `WUUF-005`

**Size Values**:
- Standard: `XS`, `S`, `M`, `L`, `XL`, `2XL`, `3XL`, `4XL`
- Case-sensitive
- No spaces

**Shirt_Color**:
- Common values: `Black`, `Navy`, `White`, `Grey`
- Capitalized first letter

**Calculations**:
- `Line_Subtotal` = `Qty` × `Unit_Price_THB`
- `Line_Profit` = `Line_Subtotal` - `COGS_THB`

### Example Data

| Order_ID | SKU | Shirt_Color | Size | Qty | Unit_Price_THB | Line_Subtotal | COGS_THB | Line_Profit |
|----------|-----|-------------|------|-----|----------------|---------------|----------|-------------|
| ORD-001 | WUUF-005-BK-M | Black | M | 2 | 690 | 1380 | 690 | 690 |
| ORD-001 | WUUF-005-NV-L | Navy | L | 1 | 690 | 690 | 345 | 345 |

---

## Sheet 3: Products

Product catalog master data.

### Required Columns

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| `SKU` | string | Product SKU (primary key) | `WUUF-005-BK-M` |
| `Product_Name` | string | Product display name | `WUUF Dachshund Shirt Black M` |
| `Dog_Breed` | string | Target dog breed | `Dachshund` |

### Data Format Details

**Dog_Breed**:
- Common values: `Dachshund`, `GoldenRetriever`, `BorderCollie`
- CamelCase format
- No spaces in breed names

**Product_Name**:
- Descriptive name for product
- Can include breed, color, size

### Example Data

| SKU | Product_Name | Dog_Breed |
|-----|--------------|-----------|
| WUUF-005-BK-M | WUUF Dachshund Shirt Black M | Dachshund |
| WUUF-006-NV-L | WUUF Golden Shirt Navy L | GoldenRetriever |

---

## Joined Transaction Data

After backend joins all three sheets:

### Final Data Structure

```python
{
  'Order_Date': datetime,        # From Orders
  'Order_ID': str,               # From Orders
  'Channel': str,                # From Orders
  'Customer_Name': str,          # From Orders
  'Instagram': str,              # From Orders (optional)
  'Phone': str,                  # From Orders (cleaned)
  'SKU': str,                    # From Order_Items
  'Collection': str,             # Extracted from SKU
  'Product_Name': str,           # From Products
  'Dog_Breed': str,              # From Products
  'Shirt_Color': str,            # From Order_Items
  'Size': str,                   # From Order_Items
  'Qty': int,                    # From Order_Items
  'Unit_Price_THB': float,       # From Order_Items
  'Line_Subtotal': float,        # From Order_Items
  'COGS_THB': float,             # From Order_Items
  'Line_Profit': float           # From Order_Items
}
```

### Join Logic

1. **Order_Items → Orders**: 
   - Join on `Order_ID`
   - Type: Left join
   - Result: Order_Items with customer info

2. **Result → Products**:
   - Join on `SKU`
   - Type: Left join
   - Result: Full transaction data

3. **Collection Extraction**:
   - Regex pattern: `WUUF-\d{3}`
   - Applied to `SKU` column
   - Example: `WUUF-005-BK-M` → `WUUF-005`

---

## Data Validation

### Automatic Filtering

Backend automatically filters out:
- Empty template rows
- Rows where key fields are empty:
  - Orders: `Order_ID` is empty
  - Order_Items: `SKU` is empty
  - Products: `SKU` is empty

### Data Cleaning

**Phone Numbers**:
```python
# Input variations
"091-003-4999"  # With dashes
"910034999"     # Missing leading zero (9 digits)
"0910034999"    # Perfect

# Output (all cases)
"0910034999"    # Standardized
```

**Instagram Handles**:
```python
# Keep as-is
"ple19"         # Good
""              # Empty → null in API
```

---

## Common Issues & Solutions

### Issue: "Sheet 'Orders' not found"

**Cause**: Sheet name mismatch (case-sensitive)

**Solution**:
- Exact names: `Orders`, `Order_Items`, `Products`
- Not: `orders`, `Order_items`, `order_items`

### Issue: Missing data after join

**Cause**: `Order_ID` or `SKU` mismatch between sheets

**Solution**:
- Ensure `Order_ID` in Order_Items exists in Orders
- Ensure `SKU` in Order_Items exists in Products
- Check for extra spaces or typos

### Issue: Phone numbers showing incorrectly

**Cause**: Excel/Sheets formatting as number

**Solution**:
- Format column as "Plain text" in Google Sheets
- Backend handles cleaning automatically

### Issue: Dates not recognized

**Cause**: Date format not recognized

**Solution**:
- Use Google Sheets date format
- Or use `YYYY-MM-DD` text format
- Backend parses automatically

---

## Data Entry Best Practices

### 1. Use Data Validation

Set up dropdown lists in Google Sheets:
- **Channel**: Instagram, Direct Sales, Shopee
- **Size**: S, M, L, XL, 2XL, 3XL, 4XL
- **Dog_Breed**: Dachshund, GoldenRetriever, BorderCollie

### 2. Consistent Formatting

- **Phone**: Either format works (dashes or not)
- **Breed**: Always CamelCase
- **Size**: Always uppercase
- **Color**: Capitalize first letter

### 3. Required vs Optional

**Required (must not be empty)**:
- Order_ID
- SKU
- Order_Date
- Customer_Name
- Channel
- Qty, Unit_Price_THB, COGS_THB

**Optional (can be empty)**:
- Instagram
- Phone (though recommended)

---

## Example Google Sheets Setup

### Orders Sheet

```
| Order_ID | Order_Date | Channel    | Customer_Name  | Instagram  | Phone        |
|----------|------------|------------|----------------|------------|--------------|
| ORD-001  | 11/7/2025  | Instagram  | Name 1         | user1      | 091-003-4999 |
| ORD-002  | 11/8/2025  | Shopee     | Name 2         | user2      | 0802573964   |
```

### Order_Items Sheet

```
| Order_ID | SKU           | Shirt_Color | Size | Qty | Unit_Price_THB | Line_Subtotal | COGS_THB | Line_Profit |
|----------|---------------|-------------|------|-----|----------------|---------------|----------|-------------|
| ORD-001  | WUUF-005-BK-M | Black       | M    | 2   | 690            | 1380          | 690      | 690         |
| ORD-002  | WUUF-006-NV-L | Navy        | L    | 1   | 690            | 690           | 345      | 345         |
```

### Products Sheet

```
| SKU           | Product_Name              | Dog_Breed    |
|---------------|---------------------------|--------------|
| WUUF-005-BK-M | Dachshund Shirt Black M   | Dachshund    |
| WUUF-006-NV-L | Golden Shirt Navy L       | GoldenRetriever |
```

---

## Sharing & Permissions

### Service Account Access

1. **Share the spreadsheet** with:
   ```
   wuuf-817@gold-totem-478004-q0.iam.gserviceaccount.com
   ```

2. **Permission level**: 
   - Viewer (read-only) - Recommended
   - Editor (read-write) - If needed

3. **Verification**:
   - Test: `curl http://localhost:8000/test-connection`
   - Should see: "Successfully loaded X transactions"

---

## Performance Considerations

### Row Limits

- **Current**: ~100 transactions
- **Recommended max**: 10,000 rows per sheet
- **Performance**: Fast (<1s) for typical datasets

### Optimization Tips

1. **Archive old data**: Move old orders to separate sheet
2. **Use formulas**: Auto-calculate Line_Subtotal, Line_Profit
3. **Data validation**: Prevent invalid entries
4. **Named ranges**: Make formulas clearer

---

## Migration Notes

### Moving from Other Systems

**From Excel**:
1. Export as CSV
2. Import to Google Sheets
3. Verify column names match
4. Format Phone column as text

**From Database**:
1. Export as CSV with exact column names
2. Import to Google Sheets  
3. Share with service account
4. Test connection

---

**Last Updated**: November 29, 2025
