@echo off
echo ========================================
echo Amazon A+ Content Generator Setup
echo Windows Version
echo ========================================
echo.

:: Check Node.js
echo Checking Node.js...
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Node.js not found!
    echo Please install from: https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo [OK] Node.js installed

:: Check Python
echo.
echo Checking Python...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Python not found!
    echo Please install from: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo [OK] Python installed

:: Check MongoDB (optional since Atlas can be used)
echo.
echo Checking MongoDB...
sc query MongoDB >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] MongoDB service not found
    echo You can either:
    echo   1. Install MongoDB locally: https://www.mongodb.com/try/download/community
    echo   2. Use MongoDB Atlas cloud free tier
    echo.
) else (
    echo [OK] MongoDB service found
)

:: Install Yarn if needed
echo.
echo Checking Yarn...
where yarn >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Yarn...
    call npm install -g yarn
)
echo [OK] Yarn ready

:: Setup Backend
echo.
echo ========================================
echo Setting up Backend...
echo ========================================
cd backend

:: Create virtual environment
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Activate and install
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

:: Create .env if doesn't exist
if not exist .env (
    echo Creating backend .env file...
    (
        echo MONGO_URL=mongodb://localhost:27017
        echo DB_NAME=amazon_aplus_generator
        echo CORS_ORIGINS=http://localhost:3000
        echo EMERGENT_LLM_KEY=sk-emergent-8A0Cd959cD2D61aE83
        echo JWT_SECRET=your-secret-key-change-in-production-abc123xyz789
    ) > .env
    echo [OK] Backend .env created
)

cd ..

:: Setup Frontend
echo.
echo ========================================
echo Setting up Frontend...
echo ========================================
cd frontend

echo Installing Node dependencies (this may take a few minutes)...
call yarn install

:: Create .env if doesn't exist
if not exist .env (
    echo Creating frontend .env file...
    (
        echo REACT_APP_BACKEND_URL=http://localhost:8000
    ) > .env
    echo [OK] Frontend .env created
)

cd ..

:: Create start scripts
echo.
echo Creating start scripts...

:: Backend start script
(
    echo @echo off
    echo cd backend
    echo call venv\Scripts\activate
    echo echo.
    echo echo ========================================
    echo echo Starting Backend Server
    echo echo URL: http://localhost:8000
    echo echo ========================================
    echo echo.
    echo python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
    echo pause
) > start-backend.bat

:: Frontend start script
(
    echo @echo off
    echo cd frontend
    echo echo.
    echo echo ========================================
    echo echo Starting Frontend Server
    echo echo URL: http://localhost:3000
    echo echo ========================================
    echo echo.
    echo yarn start
    echo pause
) > start-frontend.bat

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo   1. Make sure MongoDB is running
echo      - Check Services or use MongoDB Atlas
echo.
echo   2. Start Backend:
echo      - Double-click: start-backend.bat
echo      - Or run: start-backend.bat
echo.
echo   3. Start Frontend (in new window):
echo      - Double-click: start-frontend.bat
echo      - Or run: start-frontend.bat
echo.
echo   4. Open browser to: http://localhost:3000
echo.
echo.
echo Quick MongoDB Options:
echo   - Local: net start MongoDB (as Administrator)
echo   - Cloud: Get free MongoDB Atlas at mongodb.com/cloud/atlas
echo.
echo Need help? See WINDOWS_SETUP_GUIDE.md
echo.
pause
