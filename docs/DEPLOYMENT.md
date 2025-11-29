# Deployment Guide

Complete guide for deploying WUUF Analytics Backend to Railway and running locally.

---

## Table of Contents

1. [Railway Deployment](#railway-deployment)
2. [Local Development](#local-development)
3. [Environment Variables](#environment-variables)
4. [Google Sheets Setup](#google-sheets-setup)
5. [Troubleshooting](#troubleshooting)

---

## Railway Deployment

### Prerequisites

- GitHub account
- Railway account (https://railway.app)
- Google Service Account JSON

### Step 1: Prepare Repository

1. **Push to GitHub**:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Ensure files exist**:
   - `Procfile` - Railway start command
   - `requirements.txt` - Python dependencies
   - `.env.example` - Environment template

### Step 2: Create Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `wuuf-analytics-backend` repository
5. Railway auto-detects Python and installs dependencies

### Step 3: Configure Environment Variables

In Railway dashboard > Variables tab, add:

```bash
# Required
GOOGLE_SHEET_ID=1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE

# Service Account (paste entire JSON as single line)
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"gold-totem-478004-q0","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"wuuf-817@gold-totem-478004-q0.iam.gserviceaccount.com",...}

# Optional
PORT=8000
```

**Important**: For `GOOGLE_SERVICE_ACCOUNT_JSON`:
- Copy entire contents of `gold-totem-478004-q0-9501779d48ad.json`
- Remove all newlines (make it one line)
- Paste as variable value

### Step 4: Deploy

1. Railway auto-deploys on push to `main`
2. Check deployment logs for errors
3. Get deployment URL from Railway dashboard
4. Test: `curl https://your-app.railway.app/`

### Step 5: Configure Domain (Optional)

1. Railway dashboard > Settings
2. Add custom domain or use Railway subdomain
3. Update CORS settings if needed

---

## Local Development

### Prerequisites

- Python 3.9+
- pip
- Google Service Account JSON file

### Setup Instructions

1. **Clone Repository**:
```bash
git clone https://github.com/northpr/wuuf-analytics-backend.git
cd wuuf-analytics-backend
```

2. **Create Virtual Environment**:
```bash
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set Environment Variables**:

Create `.env` file:
```bash
GOOGLE_SHEET_ID=1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE
GOOGLE_SERVICE_ACCOUNT_FILE=gold-totem-478004-q0-9501779d48ad.json
PORT=8000
```

Or export manually:
```bash
export GOOGLE_SHEET_ID=1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE
export GOOGLE_SERVICE_ACCOUNT_FILE=gold-totem-478004-q0-9501779d48ad.json
```

5. **Add Service Account JSON**:

Place `gold-totem-478004-q0-9501779d48ad.json` in project root.

6. **Run Server**:
```bash
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Test**:
```bash
curl http://localhost:8000/
curl http://localhost:8000/test-connection
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_SHEET_ID` | Google Sheets spreadsheet ID | `1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE` |
| `GOOGLE_SERVICE_ACCOUNT_JSON` or `GOOGLE_SERVICE_ACCOUNT_FILE` | Service account credentials | JSON string or file path |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8000` |

### Environment-Specific Config

**Local Development**:
```bash
GOOGLE_SERVICE_ACCOUNT_FILE=gold-totem-478004-q0-9501779d48ad.json
```

**Railway/Production**:
```bash
GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
```

---

## Google Sheets Setup

### Step 1: Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Enable Google Sheets API
4. Create Service Account:
   - IAM & Admin > Service Accounts
   - Create Service Account
   - Grant "Editor" role
   - Create JSON key

### Step 2: Share Google Sheet

1. Open your Google Sheet
2. Click "Share"
3. Add service account email:
   ```
   wuuf-817@gold-totem-478004-q0.iam.gserviceaccount.com
   ```
4. Grant "Editor" or "Viewer" permissions

### Step 3: Get Sheet ID

From Google Sheets URL:
```
https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
```

Example:
```
https://docs.google.com/spreadsheets/d/1zv1Ww6ad8QbKPNQV1EoI8CtBqm6cozww0DfHm4lR_fE/edit
                                         ↑
                                    This is the ID
```

### Step 4: Required Sheet Structure

Ensure these sheets exist with correct names (case-sensitive):
- `Orders`
- `Order_Items`
- `Products`

See [DATA_STRUCTURE.md](./DATA_STRUCTURE.md) for column requirements.

---

## Troubleshooting

### Issue: "Service account file not found"

**Solution**:
- Check file path in environment variable
- Ensure file exists in project root
- For Railway, use `GOOGLE_SERVICE_ACCOUNT_JSON` instead

### Issue: "Spreadsheet not found"

**Solution**:
- Verify `GOOGLE_SHEET_ID` is correct
- Ensure sheet is shared with service account email
- Check sheet ID doesn't have extra characters

### Issue: "Sheet 'Orders' not found"

**Solution**:
- Sheet names are case-sensitive
- Ensure sheets are named exactly: `Orders`, `Order_Items`, `Products`
- Check for trailing spaces in sheet names

### Issue: "Module not found" errors

**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Port already in use

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 [PID]

# Or use different port
uvicorn apps.api.main:app --port 8001
```

### Issue: CORS errors in browser

**Solution**:
Update `apps/api/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Cache not refreshing

**Solution**:
- Cache refreshes every 5 minutes automatically
- Restart server to clear cache immediately
- Or implement manual refresh endpoint

---

## Production Checklist

Before deploying to production:

- [ ] Update CORS to specific origins
- [ ] Set secure environment variables
- [ ] Test all endpoints
- [ ] Verify Google Sheets connection
- [ ] Set up monitoring/logging
- [ ] Configure custom domain
- [ ] Enable HTTPS
- [ ] Consider rate limiting
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Document API for team

---

## Monitoring

### Health Checks

```bash
# Check API health
curl https://your-app.railway.app/

# Test connection
curl https://your-app.railway.app/test-connection
```

### Logs

**Railway**:
- Dashboard > Deployments > View Logs

**Local**:
- Server logs in terminal
- Check for Google Sheets API errors

---

## Updating Deployment

### Railway Auto-Deploy

1. Make changes locally
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```
3. Railway auto-deploys (watch logs)

### Manual Deploy

```bash
# Railway CLI
railway up
```

---

## Rollback

If deployment fails:

1. Railway Dashboard > Deployments
2. Find previous successful deployment
3. Click "Redeploy"

Or revert Git commit:
```bash
git revert HEAD
git push origin main
```

---

## Cost Optimization

### Railway Free Tier

- $5 free credit/month
- Sleeps after inactivity
- Good for development/small projects

### Caching Strategy

- 5-minute cache reduces Google Sheets API calls
- Adjust in `shared/data_loader.py`:
```python
CACHE_DURATION_MINUTES = 5  # Increase to reduce API calls
```

---

**Last Updated**: November 29, 2025
