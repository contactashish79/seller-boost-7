@echo off
echo ========================================
echo Fresh PostgreSQL Setup
echo Amazon A+ Content Generator
echo ========================================
echo.

:: Check Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Python not found!
    echo Install from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found

:: Check Node
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [X] Node.js not found!
    echo Install from: https://nodejs.org/
    pause
    exit /b 1
)
echo [OK] Node.js found

echo.
echo ========================================
echo Choose PostgreSQL Option:
echo ========================================
echo 1. I'm using Supabase (cloud - easiest)
echo 2. I have local PostgreSQL installed
echo 3. Exit
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="3" exit /b 0

echo.
echo ========================================
echo Setting up Backend...
echo ========================================
cd backend

:: Create venv if needed
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate
call venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo [OK] Dependencies installed

:: Setup .env
if not exist .env (
    echo.
    echo Creating .env file...
    
    if "%choice%"=="1" (
        echo.
        echo === SUPABASE SETUP ===
        echo 1. Go to: https://supabase.com/
        echo 2. Create a project
        echo 3. Go to Settings - Database
        echo 4. Copy the "Connection string" (URI format)
        echo.
        set /p db_url="Paste your Supabase connection string: "
    ) else (
        echo.
        set /p db_pass="Enter your PostgreSQL password: "
        set "db_url=postgresql://postgres:!db_pass!@localhost:5432/amazon_aplus"
        
        echo.
        echo Creating database...
        psql -U postgres -c "CREATE DATABASE amazon_aplus;" 2>nul
    )
    
    (
        echo DATABASE_URL=!db_url!
        echo BASE_URL=http://localhost:8000
        echo CORS_ORIGINS=http://localhost:3000
        echo JWT_SECRET=my-secret-key-%RANDOM%%RANDOM%
        echo OPENAI_API_KEY=your-openai-key-here
        echo GOOGLE_API_KEY=your-google-key-here
        echo DISABLE_AI=true
    ) > .env
    
    echo [OK] .env created
)

cd ..

echo.
echo ========================================
echo Setting up Frontend...
echo ========================================
cd frontend

:: Check if node_modules exists
if not exist node_modules (
    echo Installing frontend dependencies...
    call yarn install
    echo [OK] Frontend dependencies installed
)

:: Create frontend .env if needed
if not exist .env (
    echo REACT_APP_BACKEND_URL=http://localhost:8000 > .env
    echo [OK] Frontend .env created
)

cd ..

:: Create start scripts
echo.
echo Creating start scripts...

(
    echo @echo off
    echo cd backend
    echo call venv\Scripts\activate
    echo echo.
    echo echo Starting Backend on http://localhost:8000
    echo echo.
    echo python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
    echo pause
) > start-backend.bat

(
    echo @echo off
    echo cd frontend  
    echo echo.
    echo echo Starting Frontend on http://localhost:3000
    echo echo.
    echo yarn start
    echo pause
) > start-frontend.bat

echo [OK] Start scripts created

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Start Backend:
echo    Double-click: start-backend.bat
echo.
echo 2. Start Frontend (new window):
echo    Double-click: start-frontend.bat
echo.
echo 3. Open: http://localhost:3000
echo.
echo.
echo AI Features (Optional):
echo   - Get OpenAI key: https://platform.openai.com/api-keys
echo   - Get Google AI key: https://makersuite.google.com/app/apikey
echo   - Add to backend\.env
echo   - Set DISABLE_AI=false
echo.
echo See FRESH_POSTGRES_SETUP.md for detailed guide
echo.
pause
