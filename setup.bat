@echo off
echo Setting up Wikipedia Quiz App...

REM Backend setup
echo Setting up backend...
cd backend

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install backend dependencies
pip install -r requirements.txt

REM Copy environment file
if not exist .env (
    copy .env.example .env
    echo Please edit backend\.env and add your credentials
)

cd ..

REM Frontend setup
echo Setting up frontend...
cd frontend

REM Install frontend dependencies
call npm install

REM Copy environment file
if not exist .env (
    copy .env.example .env
)

cd ..

echo Setup complete!
echo.
echo Next steps:
echo 1. Edit backend\.env and add your DATABASE_URL and GOOGLE_API_KEY
echo 2. Create PostgreSQL database: CREATE DATABASE wiki_quiz_db;
echo 3. Start backend: cd backend ^&^& python main.py
echo 4. Start frontend: cd frontend ^&^& npm run dev
echo.
echo Access the app at http://localhost:3000

pause
