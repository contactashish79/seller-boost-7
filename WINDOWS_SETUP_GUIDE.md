# Amazon A+ Content Generator - Windows Setup Guide

## Prerequisites Installation

### 1. Install Node.js
1. Download from: https://nodejs.org/ (LTS version)
2. Run installer, click "Next" through all steps
3. Verify installation:
   ```cmd
   node --version
   npm --version
   ```

### 2. Install Python
1. Download from: https://www.python.org/downloads/ (3.9 or higher)
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify:
   ```cmd
   python --version
   ```

### 3. Install MongoDB
1. Download from: https://www.mongodb.com/try/download/community
2. Select "Windows" and "MSI" package
3. Run installer, choose "Complete" installation
4. Install as Windows Service (recommended)
5. MongoDB will start automatically

Or use MongoDB Atlas (cloud, free):
- Sign up at https://www.mongodb.com/cloud/atlas
- Create free cluster
- Get connection string

### 4. Install Yarn
Open Command Prompt as Administrator:
```cmd
npm install -g yarn
```

## Setup Your Downloaded Code

### Step 1: Extract and Open Folder
1. Extract your downloaded code to a folder (e.g., `C:\Projects\amazon-aplus`)
2. Open Command Prompt
3. Navigate to folder:
   ```cmd
   cd C:\Projects\amazon-aplus
   ```

### Step 2: Backend Setup

Open Command Prompt in your project folder:

```cmd
cd backend

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt
```

Create `backend\.env` file with this content:
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=amazon_aplus_generator
CORS_ORIGINS=http://localhost:3000
EMERGENT_LLM_KEY=sk-emergent-8A0Cd959cD2D61aE83
JWT_SECRET=your-secret-key-change-in-production-abc123xyz789
```

**If using MongoDB Atlas (cloud)**, change `MONGO_URL` to your Atlas connection string:
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
```

### Step 3: Frontend Setup

Open a **NEW** Command Prompt window:

```cmd
cd C:\Projects\amazon-aplus\frontend

:: Install dependencies
yarn install
```

Create `frontend\.env` file with this content:
```
REACT_APP_BACKEND_URL=http://localhost:8000
```

## Running the Application

### Terminal 1: Start Backend

```cmd
cd C:\Projects\amazon-aplus\backend
venv\Scripts\activate
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend (New Window)

```cmd
cd C:\Projects\amazon-aplus\frontend
yarn start
```

Browser will automatically open to: **http://localhost:3000**

## Quick Start Scripts (Windows)

### Create `start-backend.bat`
Create file `start-backend.bat` in project root:
```batch
@echo off
cd backend
call venv\Scripts\activate
echo Starting Backend on http://localhost:8000
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
pause
```

### Create `start-frontend.bat`
Create file `start-frontend.bat` in project root:
```batch
@echo off
cd frontend
echo Starting Frontend on http://localhost:3000
yarn start
pause
```

### Usage:
1. Double-click `start-backend.bat`
2. Double-click `start-frontend.bat`
3. Open browser to http://localhost:3000

## Troubleshooting

### "Python not recognized"
- Reinstall Python and check "Add Python to PATH"
- Or manually add to PATH: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`

### "MongoDB connection failed"
**Option A: Check local MongoDB**
1. Open Services (Win + R, type `services.msc`)
2. Find "MongoDB Server"
3. Right-click → Start

**Option B: Use MongoDB Atlas (easier)**
1. Sign up at https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Update `backend\.env` with Atlas connection string

### "Port 3000 already in use"
```cmd
:: Find process using port 3000
netstat -ano | findstr :3000

:: Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

### "Port 8000 already in use"
```cmd
:: Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Backend errors about "emergentintegrations"
Make sure you're in the virtual environment:
```cmd
cd backend
venv\Scripts\activate
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

### Frontend won't compile
Delete and reinstall:
```cmd
cd frontend
rmdir /s /q node_modules
del yarn.lock
yarn install
```

## File Structure Check

Your folder should look like:
```
amazon-aplus/
├── backend/
│   ├── server.py
│   ├── requirements.txt
│   ├── .env
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── pages/
│   │   └── components/
│   ├── package.json
│   ├── .env
│   └── node_modules/
├── start-backend.bat
└── start-frontend.bat
```

## Testing Your Setup

1. Backend test:
   ```cmd
   curl http://localhost:8000/api/
   ```
   Should return: `{"message":"Amazon A+ Content Generator API"}`

2. Open frontend: http://localhost:3000
3. Sign up with any email/password
4. Create a project and test features!

## Using Your AI Features

The app uses Emergent's Universal Key (included in code):
- Deducts from your Emergent account credits
- Works for both text (GPT-5.2) and image generation (Gemini)
- Manage balance at: Emergent Dashboard → Profile → Universal Key

## Next Steps

Once running locally:
1. Test all features (upload, AI generation, etc.)
2. Customize design/features as needed
3. Deploy to production when ready (ask me: "Deploy to production")

## Need Help?

Common issues:
- MongoDB: Use MongoDB Atlas (cloud) instead of local
- Python PATH: Reinstall Python with PATH checked
- Ports busy: Change ports in code or kill processes

Ask me:
- "MongoDB Atlas setup"
- "Change to different ports"
- "Fix [specific error]"
