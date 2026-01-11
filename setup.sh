#!/bin/bash

# Setup script for Wikipedia Quiz App

echo "🚀 Setting up Wikipedia Quiz App..."

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install backend dependencies
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your credentials"
fi

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend

# Install frontend dependencies
npm install

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
fi

cd ..

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit backend/.env and add your DATABASE_URL and GOOGLE_API_KEY"
echo "2. Create PostgreSQL database: CREATE DATABASE wiki_quiz_db;"
echo "3. Start backend: cd backend && python main.py"
echo "4. Start frontend: cd frontend && npm run dev"
echo ""
echo "🌐 Access the app at http://localhost:3000"
