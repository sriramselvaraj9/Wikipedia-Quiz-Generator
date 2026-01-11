# Deployment Guide - Vercel

This guide will help you deploy the Wikipedia Quiz App to Vercel.

## Prerequisites

- [Vercel Account](https://vercel.com/signup)
- [GitHub Account](https://github.com/signup)
- PostgreSQL Database (choose one):
  - [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres)
  - [Supabase](https://supabase.com/) (Free tier available)
  - [Neon](https://neon.tech/) (Free tier available)
  - [Railway](https://railway.app/) (Free tier available)
- [Google Gemini API Key](https://makersuite.google.com/app/apikey)

## Step 1: Prepare Your Repository

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Wikipedia Quiz App"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/wiki-quiz-app.git
   git push -u origin main
   ```

## Step 2: Set Up PostgreSQL Database

### Option A: Vercel Postgres (Recommended)

1. Go to your Vercel dashboard
2. Navigate to Storage tab
3. Create a new Postgres database
4. Copy the connection string

### Option B: Supabase (Free Alternative)

1. Go to [Supabase](https://supabase.com/)
2. Create new project
3. Go to Settings → Database
4. Copy the "Connection string" (Pooling mode recommended)
5. Replace `[YOUR-PASSWORD]` with your database password

### Option C: Neon (Serverless Postgres)

1. Go to [Neon](https://neon.tech/)
2. Create new project
3. Copy the connection string from dashboard

Example connection string format:
```
postgresql://username:password@host:port/database
```

## Step 3: Deploy to Vercel

### Method 1: Vercel Dashboard (Easiest)

1. **Import Project:**
   - Go to [Vercel Dashboard](https://vercel.com/new)
   - Click "Import Project"
   - Import your GitHub repository

2. **Configure Build Settings:**
   - Framework Preset: Other
   - Root Directory: `./`
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`

3. **Set Environment Variables:**
   Go to Project Settings → Environment Variables and add:
   
   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete (~2-3 minutes)

### Method 2: Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Add Environment Variables:**
   ```bash
   vercel env add DATABASE_URL
   # Paste your PostgreSQL connection string
   
   vercel env add GOOGLE_API_KEY
   # Paste your Gemini API key
   ```

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

## Step 4: Verify Deployment

1. **Check Backend:**
   - Visit: `https://your-app.vercel.app/api/`
   - Should return API information

2. **Test Frontend:**
   - Visit: `https://your-app.vercel.app`
   - Should see the quiz generation page

3. **Test Database Connection:**
   - Try generating a quiz
   - Check if it appears in history

## Step 5: Post-Deployment Configuration

### Enable CORS (if needed)

Edit `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app"],  # Your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Update Frontend API URL

Create `frontend/.env.production`:
```
VITE_API_URL=https://your-app.vercel.app
```

## Troubleshooting

### Issue: "Database connection failed"

**Solution:**
1. Verify DATABASE_URL is correct
2. Check if database allows connections from Vercel IPs
3. For Supabase, use the pooling connection string
4. Ensure database exists

### Issue: "LLM generation timeout"

**Solution:**
1. Increase Vercel function timeout (Pro plan required for >10s)
2. Reduce article content size in `scraper.py`
3. Use shorter prompts

### Issue: "Build failed"

**Solution:**
1. Check build logs in Vercel dashboard
2. Ensure all dependencies are in requirements.txt/package.json
3. Verify Python version compatibility

### Issue: "Frontend can't connect to backend"

**Solution:**
1. Check VITE_API_URL environment variable
2. Verify API routes in vercel.json
3. Check browser console for CORS errors

## Performance Optimization

### 1. Enable Caching
The app already includes caching - duplicate URLs won't be re-scraped.

### 2. Database Indexes
Run this SQL on your database:
```sql
CREATE INDEX idx_url ON quiz_records(url);
CREATE INDEX idx_created_at ON quiz_records(created_at DESC);
```

### 3. API Rate Limiting
Consider implementing rate limiting for production:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/generate-quiz")
@limiter.limit("5/minute")
async def generate_quiz(...):
    ...
```

## Monitoring

### Vercel Analytics
Enable in Project Settings → Analytics

### Logging
View logs: `vercel logs <deployment-url>`

### Database Monitoring
Check your PostgreSQL provider's dashboard for:
- Connection count
- Query performance
- Storage usage

## Cost Estimates

### Free Tier Limits:
- **Vercel**: 100GB bandwidth/month, unlimited deployments
- **Vercel Postgres**: 256MB storage, 60 hours compute
- **Supabase**: 500MB database, 2GB bandwidth
- **Gemini API**: 60 requests/minute free tier

### Upgrade Considerations:
- High traffic (>100K requests/month)
- Large database (>1GB)
- Longer function execution times
- More API requests

## Security Best Practices

1. **Never commit .env files**
2. **Use environment variables for all secrets**
3. **Enable HTTPS only** (Vercel does this by default)
4. **Implement rate limiting**
5. **Validate all inputs**
6. **Keep dependencies updated**

## Backup Strategy

### Database Backups:
- **Vercel Postgres**: Automatic daily backups
- **Supabase**: Point-in-time recovery
- **Neon**: Automatic backups

### Manual Backup:
```bash
pg_dump $DATABASE_URL > backup.sql
```

## Scaling Considerations

When your app grows:

1. **Upgrade database** tier for more connections
2. **Add Redis caching** for faster responses
3. **Implement CDN** for static assets
4. **Use queue system** for long-running tasks
5. **Load balancing** (Vercel handles automatically)

## Support & Resources

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Next Steps After Deployment

1. ✅ Test all features thoroughly
2. ✅ Set up monitoring and alerts
3. ✅ Configure custom domain (optional)
4. ✅ Enable analytics
5. ✅ Share your app!

---

**Congratulations! Your Wikipedia Quiz App is now live! 🎉**
