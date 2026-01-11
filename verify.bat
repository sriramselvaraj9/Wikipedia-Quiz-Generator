@echo off
echo ========================================
echo Wikipedia Quiz App - Project Verification
echo ========================================
echo.

REM Check if files exist
echo [1/6] Checking project structure...
if exist "backend\main.py" (
    echo   [OK] Backend main.py found
) else (
    echo   [ERROR] Backend main.py missing
)

if exist "frontend\src\App.jsx" (
    echo   [OK] Frontend App.jsx found
) else (
    echo   [ERROR] Frontend App.jsx missing
)

if exist "README.md" (
    echo   [OK] README.md found
) else (
    echo   [ERROR] README.md missing
)

if exist "vercel.json" (
    echo   [OK] vercel.json found
) else (
    echo   [ERROR] vercel.json missing
)

echo.
echo [2/6] Checking backend files...
cd backend
if exist "venv" (
    echo   [OK] Virtual environment exists
) else (
    echo   [WARN] Virtual environment not created yet
    echo   Run: python -m venv venv
)

if exist ".env" (
    echo   [OK] .env file exists
) else (
    echo   [WARN] .env file not configured
    echo   Run: copy .env.example .env
)

cd ..

echo.
echo [3/6] Checking frontend setup...
cd frontend
if exist "node_modules" (
    echo   [OK] Node modules installed
) else (
    echo   [WARN] Node modules not installed
    echo   Run: npm install
)

if exist ".env" (
    echo   [OK] .env file exists
) else (
    echo   [WARN] .env file not configured
    echo   Run: copy .env.example .env
)

cd ..

echo.
echo [4/6] Checking sample data...
if exist "sample_data\alan_turing.json" (
    echo   [OK] Sample data present
) else (
    echo   [ERROR] Sample data missing
)

echo.
echo [5/6] Checking Git status...
if exist ".git" (
    echo   [OK] Git initialized
    git status --short
) else (
    echo   [ERROR] Git not initialized
    echo   Run: git init
)

echo.
echo [6/6] Project summary...
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. Configure backend\.env with:
echo    - DATABASE_URL (PostgreSQL connection string)
echo    - GOOGLE_API_KEY (Get from https://makersuite.google.com/app/apikey)
echo.
echo 2. Create PostgreSQL database:
echo    psql -U postgres -c "CREATE DATABASE wiki_quiz_db;"
echo.
echo 3. Install dependencies:
echo    cd backend
echo    venv\Scripts\activate
echo    pip install -r requirements.txt
echo.
echo 4. Install frontend dependencies:
echo    cd frontend
echo    npm install
echo.
echo 5. Test locally:
echo    Terminal 1: cd backend ^&^& python main.py
echo    Terminal 2: cd frontend ^&^& npm run dev
echo    Browser: http://localhost:3000
echo.
echo 6. Push to GitHub:
echo    git remote add origin https://github.com/YOUR_USERNAME/wiki-quiz-app.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 7. Deploy to Vercel:
echo    - Go to https://vercel.com/
echo    - Import your GitHub repository
echo    - Set environment variables
echo    - Deploy!
echo.
echo ========================================
echo For detailed instructions, see:
echo - QUICKSTART.md (5-minute setup)
echo - GITHUB_SETUP.md (Push to GitHub)
echo - DEPLOYMENT.md (Deploy to Vercel)
echo ========================================
echo.

pause
