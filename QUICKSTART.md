# Quick Start Guide

Get the Wikipedia Quiz App running in 5 minutes!

## 🚀 Super Quick Start

### Prerequisites
- Python 3.9+ installed
- Node.js 18+ installed
- PostgreSQL installed and running
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### Step 1: Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone <your-repo-url>
cd "Wiki Quiz App deep"

# Run setup script
# Windows:
setup.bat

# Linux/Mac:
chmod +x setup.sh
./setup.sh
```

### Step 2: Configure Environment (1 minute)

**Edit `backend/.env`:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/wiki_quiz_db
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Step 3: Create Database (30 seconds)

```bash
# Open PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE wiki_quiz_db;

# Exit
\q
```

### Step 4: Run the App (1 minute)

**Terminal 1 - Start Backend:**
```bash
cd backend
# Activate venv first
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
python main.py
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

### Step 5: Test It! (30 seconds)

1. Open browser: `http://localhost:3000`
2. Enter test URL: `https://en.wikipedia.org/wiki/Alan_Turing`
3. Click "Generate Quiz"
4. Wait 20-30 seconds
5. Enjoy your AI-generated quiz! 🎉

## 📝 Manual Setup (Detailed)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac

# Edit .env with your credentials
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment (optional)
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac
```

### Database Setup

```bash
# Method 1: Command line
psql -U postgres -c "CREATE DATABASE wiki_quiz_db;"

# Method 2: PostgreSQL shell
psql -U postgres
CREATE DATABASE wiki_quiz_db;
\q

# Tables will be created automatically when you first run the backend
```

## 🧪 Testing

### Test URLs
Try these Wikipedia articles:

1. **Short & Simple:**
   - https://en.wikipedia.org/wiki/Python_(programming_language)

2. **Medium Complexity:**
   - https://en.wikipedia.org/wiki/Alan_Turing
   - https://en.wikipedia.org/wiki/Albert_Einstein

3. **High Complexity:**
   - https://en.wikipedia.org/wiki/Artificial_intelligence
   - https://en.wikipedia.org/wiki/World_War_II

### Expected Results
- ✅ Scraping: 2-5 seconds
- ✅ Quiz generation: 15-30 seconds
- ✅ Total: ~20-35 seconds
- ✅ Questions: 8-10 with varying difficulty
- ✅ All questions answerable from article

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named..."
```bash
# Reactivate virtual environment and reinstall
pip install -r requirements.txt
```

### "Connection to database failed"
```bash
# Check PostgreSQL is running
# Windows:
net start postgresql-x64-14

# Linux:
sudo systemctl start postgresql

# Mac:
brew services start postgresql
```

### "GOOGLE_API_KEY not found"
- Ensure you've added it to `backend/.env`
- Get a free key at: https://makersuite.google.com/app/apikey

### "Port 8000 already in use"
```bash
# Find and kill the process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Frontend can't connect to backend
- Verify backend is running on http://localhost:8000
- Check `frontend/.env` has correct VITE_API_URL
- Clear browser cache

## 📱 Features to Try

1. **Generate Quiz** (Tab 1)
   - Enter Wikipedia URL
   - Click "Generate Quiz"
   - View questions with explanations

2. **Take Quiz Mode**
   - Switch to "Take Quiz Mode"
   - Answer questions
   - Submit and see your score

3. **History** (Tab 2)
   - View all past quizzes
   - Click "Details" to view quiz
   - Delete unwanted quizzes

4. **Caching**
   - Generate quiz from same URL
   - Notice it loads instantly (cached!)
   - Use "Force regenerate" to create new quiz

## 🚀 Next Steps

1. ✅ Read the full [README.md](README.md)
2. ✅ Check [DEPLOYMENT.md](DEPLOYMENT.md) for Vercel deployment
3. ✅ Explore sample data in [sample_data/](sample_data/)
4. ✅ Customize prompts in `backend/quiz_generator.py`
5. ✅ Star the repo and share! ⭐

## 💡 Tips

- **Faster Testing**: Use the example URLs in the UI
- **Better Quizzes**: Try articles with clear sections
- **Debugging**: Check browser console and terminal logs
- **Performance**: Close other applications for faster LLM responses

## 🆘 Still Having Issues?

1. Check the main [README.md](README.md) for detailed docs
2. Review [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
3. Open an issue on GitHub
4. Check if backend logs show errors

---

**Happy Quiz Generating! 🎓✨**
