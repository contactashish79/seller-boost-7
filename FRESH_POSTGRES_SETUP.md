# Fresh PostgreSQL Setup - Windows

## Complete Local Setup (15 minutes)

### Step 1: Install PostgreSQL

**Option A: Cloud PostgreSQL (Easiest - 5 minutes)**

1. Go to https://supabase.com/
2. Click "Start your project"
3. Create account (free)
4. Click "New project"
5. Copy the "Connection string" from Settings → Database
6. Done! Skip to Step 3

**Option B: Local PostgreSQL (10 minutes)**

1. Download: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Run installer (choose latest version)
3. During setup:
   - Password: Set and remember it!
   - Port: 5432 (default)
   - Click Next through everything
4. Finish installation

### Step 2: Create Database (Local only)

```cmd
:: Open Command Prompt
psql -U postgres

:: Enter your password when prompted

:: Create database
CREATE DATABASE amazon_aplus;

:: Confirm
\l

:: Exit
\q
```

### Step 3: Setup Project

**Navigate to your project:**
```cmd
cd C:\your-project-folder\backend
```

**Create .env file:**
```cmd
copy .env.example .env
```

**Edit `.env` file with Notepad:**

**For Supabase (Cloud):**
```
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-ID].supabase.co:5432/postgres
BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
JWT_SECRET=my-super-secret-key-12345

# Optional - for AI features
OPENAI_API_KEY=your-openai-key-here
GOOGLE_API_KEY=your-google-key-here
DISABLE_AI=false
```

**For Local PostgreSQL:**
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/amazon_aplus
BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
JWT_SECRET=my-super-secret-key-12345

# Optional - for AI features  
OPENAI_API_KEY=your-openai-key-here
GOOGLE_API_KEY=your-google-key-here
DISABLE_AI=false
```

**Don't have AI keys yet?** Set:
```
DISABLE_AI=true
```

### Step 4: Install Dependencies

```cmd
:: Make sure you're in backend folder
cd backend

:: Create virtual environment (if not exists)
python -m venv venv

:: Activate
venv\Scripts\activate

:: Install
pip install -r requirements.txt
```

### Step 5: Run Backend

```cmd
:: Still in backend folder with venv activated
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
✓ Database tables created successfully
✓ PostgreSQL: Connected
✓ Uploads folder: C:\...\backend\uploads
✓ OpenAI: Not configured
✓ Google AI: Not configured
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Run Frontend

**Open NEW Command Prompt:**

```cmd
cd C:\your-project-folder\frontend

:: Install (first time only)
yarn install

:: Start
yarn start
```

Browser opens to: **http://localhost:3000** 🎉

---

## What Works

✅ **User Authentication** - Signup/Login
✅ **Projects** - Create, view, delete
✅ **Image Upload** - Upload product photos  
✅ **Background Removal** - Remove white backgrounds
✅ **Image Enhancement** - 2x upscaling
✅ **File Storage** - Images saved in `backend/uploads/`
✅ **PostgreSQL** - All data in database

❌ **AI Background Gen** - Requires Google AI key
❌ **AI Content Gen** - Requires OpenAI key

---

## Add AI Features (Optional)

### Get API Keys:

**OpenAI (for A+ content text):**
- https://platform.openai.com/api-keys
- $5 minimum credit
- Cost: ~$0.01-0.05 per description

**Google AI (for image generation):**
- https://makersuite.google.com/app/apikey
- Free tier available
- Cost: ~$0.10-0.30 per image

### Add to `.env`:
```
OPENAI_API_KEY=sk-proj-your-actual-key
GOOGLE_API_KEY=your-actual-key
DISABLE_AI=false
```

### Restart backend:
- Press Ctrl+C in backend terminal
- Run again: `python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000`

---

## Test Your App

1. Open http://localhost:3000
2. Click "Sign In" → "Create Account"
3. Enter email/password
4. Click "New Project"
5. Upload a product image
6. Try "Remove BG" button
7. Try "Enhance" button
8. Check `backend/uploads/` folder - images are there!

---

## File Structure

```
your-project/
├── backend/
│   ├── server.py (✓ Clean PostgreSQL version)
│   ├── requirements.txt (✓ No emergentintegrations)
│   ├── .env (your config)
│   ├── venv/ (virtual environment)
│   └── uploads/ (images saved here!)
└── frontend/
    ├── src/
    ├── package.json
    └── .env
```

---

## Troubleshooting

### "Could not connect to database"

**For Supabase:**
- Check connection string is correct
- Make sure you copied the full string
- Check password has no special characters causing issues

**For Local:**
```cmd
:: Check PostgreSQL is running
sc query postgresql-x64-16

:: If not running, start it
net start postgresql-x64-16
```

### "psycopg2 not found"
```cmd
pip install psycopg2-binary
```

### "Port 8000 in use"
```cmd
:: Find what's using it
netstat -ano | findstr :8000

:: Kill it (replace PID)
taskkill /PID [number] /F
```

### "ModuleNotFoundError"
```cmd
:: Make sure venv is activated
venv\Scripts\activate

:: Reinstall
pip install -r requirements.txt
```

---

## Success Checklist

✅ PostgreSQL installed (or Supabase account created)
✅ Database created (or connection string copied)
✅ `.env` file configured with DATABASE_URL
✅ Dependencies installed (`pip install -r requirements.txt`)
✅ Backend running (http://localhost:8000)
✅ Frontend running (http://localhost:3000)
✅ Can signup and login
✅ Can create projects
✅ Can upload images
✅ Images appear in `backend/uploads/` folder

---

## What's Next?

**Working?** 
- Test all features
- Add AI keys when ready
- Start building your Amazon listings!

**Issues?**
- Check the troubleshooting section
- Make sure DATABASE_URL is correct
- Verify PostgreSQL/Supabase is accessible

**Questions?**
Ask me:
- "PostgreSQL connection not working"
- "How to get Supabase connection string"
- "How to add AI features"

---

## Quick Commands Reference

```cmd
:: Start Backend
cd backend
venv\Scripts\activate
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000

:: Start Frontend (new window)
cd frontend
yarn start

:: Check Backend Status
curl http://localhost:8000/api/

:: View Database
psql -U postgres -d amazon_aplus
\dt  (show tables)
SELECT * FROM users;
\q  (quit)
```

---

Ready to start? Follow the steps above!
