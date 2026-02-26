@echo off
echo ========================================
echo PostgreSQL Migration Script
echo Amazon A+ Content Generator
echo ========================================
echo.

echo This will:
echo  1. Backup your current MongoDB version
echo  2. Switch to PostgreSQL version
echo  3. Setup local file storage
echo.
pause

echo.
echo Step 1: Backing up current version...
cd backend
if exist server.py (
    copy /Y server.py server_mongodb_backup.py
    echo [OK] Backed up server.py
)
if exist requirements.txt (
    copy /Y requirements.txt requirements_mongodb_backup.txt
    echo [OK] Backed up requirements.txt
)

echo.
echo Step 2: Installing PostgreSQL version...
if exist server_postgres.py (
    copy /Y server_postgres.py server.py
    echo [OK] Installed new server.py
) else (
    echo [ERROR] server_postgres.py not found!
    echo Please make sure you have the PostgreSQL files.
    pause
    exit /b 1
)

if exist requirements_postgres.txt (
    copy /Y requirements_postgres.txt requirements.txt
    echo [OK] Installed new requirements.txt
) else (
    echo [ERROR] requirements_postgres.txt not found!
    pause
    exit /b 1
)

echo.
echo Step 3: Installing dependencies...
call venv\Scripts\activate
pip install -q -r requirements.txt
echo [OK] Dependencies installed

echo.
echo Step 4: Creating uploads directory...
if not exist uploads mkdir uploads
echo [OK] Uploads directory ready

cd ..

echo.
echo ========================================
echo Migration Complete!
echo ========================================
echo.
echo Next Steps:
echo  1. Install PostgreSQL:
echo     - Download: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
echo     - Or use Supabase: https://supabase.com/ (free cloud)
echo.
echo  2. Create database:
echo     psql -U postgres
echo     CREATE DATABASE amazon_aplus;
echo     \q
echo.
echo  3. Update backend\.env:
echo     DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/amazon_aplus
echo     BASE_URL=http://localhost:8000
echo.
echo  4. Start backend:
echo     start-backend.bat
echo.
echo  5. Start frontend:
echo     start-frontend.bat
echo.
echo See POSTGRESQL_MIGRATION_GUIDE.md for detailed instructions
echo.
pause
