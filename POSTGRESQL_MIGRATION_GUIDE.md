# PostgreSQL Migration Guide - Windows

## Why PostgreSQL + Local File Storage?

**Benefits:**
- ✅ Much faster (images not in database)
- ✅ More efficient storage
- ✅ Better for production
- ✅ PostgreSQL is industry standard
- ✅ Easier backups

## Step 1: Install PostgreSQL

### Option A: Download Installer (Recommended for Windows)

1. Download PostgreSQL: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Run installer (choose latest version)
3. During installation:
   - **Password**: Set a password (remember it!)
   - **Port**: 5432 (default)
   - **Locale**: Default
4. Finish installation

### Option B: Use PostgreSQL Cloud (Easiest)

**Supabase (Free, Recommended):**
1. Sign up: https://supabase.com/
2. Create new project
3. Get connection string from Settings → Database
4. Use this connection string in your `.env`

**Other options:**
- Neon: https://neon.tech/ (free tier)
- ElephantSQL: https://www.elephantsql.com/ (free tier)

## Step 2: Create Database

### If using Local PostgreSQL:

Open Command Prompt:
```cmd
:: Connect to PostgreSQL
psql -U postgres

:: Create database
CREATE DATABASE amazon_aplus;

:: Exit
\q
```

### If using Cloud:
Database is already created, just use the connection string!

## Step 3: Update Your Code

### Backend Setup:

1. **Rename server file:**
```cmd
cd backend
move server.py server_mongodb_old.py
move server_postgres.py server.py
```

2. **Update requirements:**
```cmd
move requirements.txt requirements_mongodb_old.txt
move requirements_postgres.txt requirements.txt
```

3. **Install dependencies:**
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

4. **Update `.env` file:**

**For Local PostgreSQL:**
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/amazon_aplus
BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
EMERGENT_LLM_KEY=sk-emergent-8A0Cd959cD2D61aE83
JWT_SECRET=your-secret-key-change-in-production-abc123xyz789
```

**For Supabase/Cloud:**
```
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT].supabase.co:5432/postgres
BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
EMERGENT_LLM_KEY=sk-emergent-8A0Cd959cD2D61aE83
JWT_SECRET=your-secret-key-change-in-production-abc123xyz789
```

## Step 4: Frontend Update

Update `frontend\.env`:
```
REACT_APP_BACKEND_URL=http://localhost:8000
```

No other frontend changes needed!

## Step 5: Test It!

1. **Start Backend:**
```cmd
cd backend
venv\Scripts\activate
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Database tables created successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

2. **Start Frontend:**
```cmd
cd frontend
yarn start
```

3. **Test:**
- Sign up at http://localhost:3000
- Create a project
- Upload an image
- Check `backend/uploads/` folder - images are saved there!

## File Structure

After migration:
```
backend/
├── server.py (PostgreSQL version)
├── requirements.txt (with PostgreSQL)
├── .env (with DATABASE_URL)
├── uploads/ (images saved here!)
│   ├── user123_original_abc.jpg
│   ├── user123_processed_xyz.png
│   └── user123_enhanced_def.png
├── server_mongodb_old.py (backup)
└── requirements_mongodb_old.txt (backup)
```

## Key Changes in New Version

### Database:
- **Before**: MongoDB storing base64 images
- **After**: PostgreSQL storing file paths

### Images:
- **Before**: `"image": "data:image/png;base64,iVBORw0..."`
- **After**: `"image_url": "/uploads/user123_image.png"`

### Storage:
- **Before**: All in database (slow, large)
- **After**: Files in `/backend/uploads/`, URLs in database

## Troubleshooting

### "psycopg2 not found"
```cmd
pip install psycopg2-binary
```

### "Could not connect to PostgreSQL"
- Check PostgreSQL is running:
  ```cmd
  sc query postgresql-x64-16
  ```
- Or use cloud PostgreSQL (Supabase) instead

### "Database amazon_aplus does not exist"
```cmd
psql -U postgres
CREATE DATABASE amazon_aplus;
\q
```

### "Permission denied on uploads folder"
The app automatically creates the folder. If issues:
```cmd
cd backend
mkdir uploads
```

## Production Deployment

For production:
1. Use cloud PostgreSQL (Supabase, Neon, AWS RDS)
2. Use cloud storage (AWS S3, Cloudflare R2) for images
3. Update BASE_URL to your production domain

**Need help with production setup?** Ask me:
- "Deploy to production with PostgreSQL"
- "Setup AWS S3 for images"

## Migrate Existing Data (Optional)

If you have existing MongoDB data to migrate:

```python
# migration script
# Ask me: "Create MongoDB to PostgreSQL migration script"
```

## Comparison: MongoDB vs PostgreSQL

| Feature | MongoDB (Old) | PostgreSQL (New) |
|---------|---------------|------------------|
| Image Storage | Base64 in DB | Files on disk |
| Database Size | Very large | Small |
| Performance | Slower | Faster |
| Industry Use | NoSQL apps | Most production apps |
| Backups | Complex | Simple |

## Next Steps

1. Test all features work
2. Check `backend/uploads/` has images
3. Ready for production deployment!

**Questions?** Ask me:
- "PostgreSQL not connecting"
- "How to use Supabase"
- "Migrate existing data"
- "Deploy to production"
