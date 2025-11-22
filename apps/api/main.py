"""
WUUF Analytics Backend - Main FastAPI Application
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.routers import sales
from shared.data_loader import get_cache_info

# Initialize FastAPI app
app = FastAPI(
    title="WUUF Analytics API",
    description="Analytics API for WUUF transaction data from Google Sheets",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sales.router)


@app.get("/", tags=["health"])
async def root():
    """
    Root endpoint - Health check and API information
    """
    return {
        "status": "online",
        "message": "WUUF Analytics API is running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "sales_overview": "/sales/overview",
            "daily_sales": "/sales/daily",
            "sales_by_collection": "/sales/by-collection",
            "sales_by_breed": "/sales/by-breed",
            "sales_by_size": "/sales/by-size",
            "filter_options": "/sales/filter-options"
        }
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint
    """
    cache_info = get_cache_info()
    return {
        "status": "healthy",
        "cache": cache_info
    }


@app.get("/test-connection", tags=["health"])
async def test_connection():
    """
    Test Google Sheets connection and diagnose issues
    """
    import os
    import gspread
    from google.oauth2.service_account import Credentials
    
    result = {
        "steps": [],
        "success": False,
        "error": None
    }
    
    try:
        # Step 1: Check service account file
        creds_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'gold-totem-478004-q0-9501779d48ad.json')
        file_exists = os.path.exists(creds_file)
        result["steps"].append({
            "step": "1. Check service account file",
            "status": "✓" if file_exists else "✗",
            "file_path": creds_file,
            "exists": file_exists
        })
        
        if not file_exists:
            result["error"] = f"Service account file not found: {creds_file}"
            return result
        
        # Step 2: Load credentials
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]
            credentials = Credentials.from_service_account_file(creds_file, scopes=scopes)
            result["steps"].append({
                "step": "2. Load credentials",
                "status": "✓",
                "service_account_email": credentials.service_account_email
            })
        except Exception as e:
            result["steps"].append({
                "step": "2. Load credentials",
                "status": "✗",
                "error": str(e)
            })
            result["error"] = f"Failed to load credentials: {str(e)}"
            return result
        
        # Step 3: Authorize gspread client
        try:
            client = gspread.authorize(credentials)
            result["steps"].append({
                "step": "3. Authorize gspread client",
                "status": "✓"
            })
        except Exception as e:
            result["steps"].append({
                "step": "3. Authorize gspread client",
                "status": "✗",
                "error": str(e)
            })
            result["error"] = f"Failed to authorize: {str(e)}"
            return result
        
        # Step 4: Open spreadsheet
        sheet_id = os.getenv('GOOGLE_SHEET_ID', '1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE')
        try:
            sheet = client.open_by_key(sheet_id)
            result["steps"].append({
                "step": "4. Open spreadsheet",
                "status": "✓",
                "sheet_id": sheet_id,
                "sheet_title": sheet.title
            })
        except gspread.exceptions.SpreadsheetNotFound as e:
            error_msg = f"Spreadsheet not found. The sheet may not be shared with the service account yet. Please share with: {credentials.service_account_email}"
            result["steps"].append({
                "step": "4. Open spreadsheet",
                "status": "✗",
                "error": error_msg,
                "exception_type": "SpreadsheetNotFound",
                "exception_details": str(e)
            })
            result["error"] = error_msg
            return result
        except gspread.exceptions.APIError as e:
            error_msg = f"Google Sheets API error. This often means permissions haven't propagated yet. Error: {str(e)}"
            result["steps"].append({
                "step": "4. Open spreadsheet",
                "status": "✗",
                "error": error_msg,
                "exception_type": "APIError",
                "exception_details": str(e)
            })
            result["error"] = error_msg
            return result
        except Exception as e:
            error_msg = f"Unexpected error: {type(e).__name__} - {str(e)}"
            result["steps"].append({
                "step": "4. Open spreadsheet",
                "status": "✗",
                "error": error_msg,
                "exception_type": type(e).__name__,
                "exception_details": str(e)
            })
            result["error"] = error_msg
            return result
        
        # Step 5: List available worksheets
        try:
            worksheets = sheet.worksheets()
            worksheet_titles = [ws.title for ws in worksheets]
            result["steps"].append({
                "step": "5. List worksheets",
                "status": "✓",
                "available_sheets": worksheet_titles,
                "required_sheets": ["Orders", "Order_Items", "Products"]
            })
            
            # Check if required sheets exist
            required = ["Orders", "Order_Items", "Products"]
            missing = [s for s in required if s not in worksheet_titles]
            
            if missing:
                result["error"] = f"Missing required sheets: {', '.join(missing)}. Available sheets: {', '.join(worksheet_titles)}"
            else:
                result["success"] = True
                result["message"] = "✓ All checks passed! Google Sheets connection is working."
                
        except Exception as e:
            result["steps"].append({
                "step": "5. List worksheets",
                "status": "✗",
                "error": str(e)
            })
            result["error"] = f"Failed to list worksheets: {str(e)}"
            return result
        
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
    
    return result


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
