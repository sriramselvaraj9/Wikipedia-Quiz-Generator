# GitHub Setup Guide

Follow these steps to push your Wikipedia Quiz App to GitHub and deploy to Vercel.

## ✅ Current Status

Your project is ready with:
- ✅ All code files created
- ✅ Git initialized
- ✅ Initial commit made
- ✅ Ready to push to GitHub

## 📤 Step 1: Create GitHub Repository

### Option A: GitHub Website (Easiest)

1. Go to [GitHub](https://github.com/)
2. Click the **"+"** icon (top right) → **"New repository"**
3. Repository settings:
   - **Name**: `wiki-quiz-app` (or your preferred name)
   - **Description**: `AI-powered Wikipedia quiz generator using FastAPI, React, and Google Gemini`
   - **Visibility**: Public or Private
   - **⚠️ IMPORTANT**: Do NOT initialize with README, .gitignore, or license
4. Click **"Create repository"**

### Option B: GitHub CLI

```bash
gh repo create wiki-quiz-app --public --source=. --remote=origin
```

## 📤 Step 2: Push to GitHub

After creating the repository on GitHub, you'll see instructions. Use these commands:

```bash
cd "d:\Projects\Wiki Quiz App deep"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/wiki-quiz-app.git

# Verify remote was added
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### If you get authentication error:

**For HTTPS (Recommended):**
1. You'll be prompted for credentials
2. Use your GitHub username
3. For password, use a Personal Access Token (not your GitHub password):
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with `repo` scope
   - Copy and use this as password

**For SSH:**
```bash
# Change to SSH remote
git remote set-url origin git@github.com:YOUR_USERNAME/wiki-quiz-app.git

# Add SSH key if not already done
ssh-keygen -t ed25519 -C "your_email@example.com"
# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

## 🔍 Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all files:
   ```
   📁 backend/
   📁 frontend/
   📁 sample_data/
   📁 screenshots/
   📄 README.md
   📄 DEPLOYMENT.md
   📄 QUICKSTART.md
   📄 vercel.json
   ... and more
   ```

## 🚀 Step 4: Deploy to Vercel

### Automatic Deployment (Recommended)

1. Go to [Vercel](https://vercel.com/)
2. Click **"Add New..." → "Project"**
3. **Import Git Repository**:
   - Connect your GitHub account if needed
   - Select `wiki-quiz-app` repository
4. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./`
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`
5. **Environment Variables** (click "Add" for each):
   ```
   DATABASE_URL=your_postgresql_connection_string
   GOOGLE_API_KEY=your_gemini_api_key
   ```
6. Click **"Deploy"**
7. Wait 2-3 minutes for deployment

### Your App is Live! 🎉

After deployment completes:
- You'll get a URL like: `https://wiki-quiz-app.vercel.app`
- Frontend will be accessible at the root
- Backend API at `/api/*` endpoints

## 🗄️ Step 5: Set Up Database

### Option 1: Vercel Postgres

1. In your Vercel project dashboard
2. Go to **Storage** tab
3. Click **"Create Database"** → Select **Postgres**
4. Copy the connection string
5. Add to Environment Variables:
   ```
   DATABASE_URL=<paste connection string>
   ```

### Option 2: External Database (Supabase/Neon)

1. Create account at [Supabase](https://supabase.com/) or [Neon](https://neon.tech/)
2. Create new project
3. Copy PostgreSQL connection string
4. Add to Vercel Environment Variables

## 📝 Step 6: Update Repository with Deployment URL

After successful deployment, update your README:

```bash
cd "d:\Projects\Wiki Quiz App deep"

# Edit README.md and add at the top:
```markdown
# Wikipedia Quiz App

🌐 **Live Demo**: https://your-app.vercel.app

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/wiki-quiz-app)
```

```bash
# Commit and push changes
git add README.md
git commit -m "docs: add live demo link"
git push origin main
```

## 🧪 Step 7: Test Deployment

1. Visit your Vercel URL
2. Test generating a quiz:
   - Enter: `https://en.wikipedia.org/wiki/Alan_Turing`
   - Click "Generate Quiz"
   - Wait ~30 seconds
   - Quiz should appear!
3. Test history:
   - Click "Past Quizzes" tab
   - Should see your quiz
4. Test details modal:
   - Click "Details" button
   - Quiz should open in modal

## 🎨 Step 8: Add Screenshots (Optional)

Take screenshots of your app and add to repository:

```bash
# Create screenshots folder if it doesn't exist
# Take screenshots and save them as:
# - screenshots/generate_quiz.png
# - screenshots/history.png
# - screenshots/quiz_display.png
# - screenshots/modal.png

git add screenshots/
git commit -m "docs: add application screenshots"
git push origin main
```

## 🔧 Troubleshooting

### "Repository not found"
- Check repository URL is correct
- Verify you have access to the repository

### "Permission denied"
- For HTTPS: Use Personal Access Token instead of password
- For SSH: Add SSH key to GitHub

### "Push rejected"
- Pull first: `git pull origin main`
- Then push: `git push origin main`

### Vercel deployment fails
- Check build logs in Vercel dashboard
- Verify all environment variables are set
- Ensure DATABASE_URL and GOOGLE_API_KEY are correct

## 📋 Next Steps

1. ✅ Add project description on GitHub
2. ✅ Add topics/tags: `wikipedia`, `quiz`, `ai`, `fastapi`, `react`, `gemini`
3. ✅ Create GitHub README badges (optional)
4. ✅ Set up GitHub Actions for CI/CD (optional)
5. ✅ Share your project!

## 🌟 Optional Enhancements

### Add Badges to README

Add at the top of README.md:
```markdown
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![React](https://img.shields.io/badge/React-18-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
```

### Set Up GitHub Actions

Create `.github/workflows/test.yml` for automated testing

### Enable GitHub Pages

For documentation or project website

## 🆘 Need Help?

- **GitHub Issues**: Best for bugs and feature requests
- **GitHub Discussions**: For questions and community help
- **Vercel Support**: For deployment issues

---

## Summary Commands

```bash
# 1. Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/wiki-quiz-app.git

# 2. Push to GitHub
git branch -M main
git push -u origin main

# 3. Future updates
git add .
git commit -m "Your commit message"
git push origin main
```

**🎉 Congratulations! Your project is now on GitHub and deployed to Vercel!**

Share your live app URL and GitHub repository with others!
