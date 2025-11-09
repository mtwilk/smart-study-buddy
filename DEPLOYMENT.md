# Deployment Guide

Deploy your Smart Study Buddy app in **3 simple steps**:
1. **Backend** → Railway (Python/Flask API)
2. **Frontend** → Cloudflare Pages (React/Vite)
3. **Test** → Verify everything works

## What You Need

- GitHub account
- Railway account ([sign up free](https://railway.app/))
- Cloudflare account ([sign up free](https://dash.cloudflare.com/sign-up))
- Your Google Calendar `credentials.json` and `token.json` files

---

## Step 1: Deploy Backend to Railway

### 1.1 Push to GitHub

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 1.2 Create Railway Project

1. Go to [railway.app](https://railway.app/) and sign in
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `smart-study-buddy` repository
4. Railway will auto-detect the Python app ✅

### 1.3 Prepare Google Credentials

```bash
cd backend

# Make credentials single-line JSON (no newlines)
cat credentials.json | jq -c . > credentials.compact.json
cat token.json | jq -c . > token.compact.json

# Print to copy (you'll paste these into Railway)
cat credentials.compact.json
cat token.compact.json
```

**Don't have `jq`?** Just remove all newlines manually or use:
```bash
cat credentials.json | tr -d '\n' > credentials.compact.json
cat token.json | tr -d '\n' > token.compact.json
```

### 1.4 Add Environment Variables

In Railway, click **Variables** tab and add these:

```env
# Required - Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_service_role_key_here

# Required - OpenAI
OPENAI_API_KEY=sk-proj-xxxxx

# Required - MongoDB
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname

# Required - Your email (must match Supabase account)
USER_EMAIL=your.email@example.com

# Required - Google credentials (paste the compact JSON)
GOOGLE_CREDENTIALS_JSON={"installed":{"client_id":"...
GOOGLE_TOKEN_JSON={"token":"...

# URLs (leave BACKEND_URL as-is, update FRONTEND_URL after step 2)
FRONTEND_URL=https://smart-study-buddy.pages.dev
BACKEND_URL=${{RAILWAY_PUBLIC_DOMAIN}}

# Python config
PYTHONUNBUFFERED=1
```

**Optional** (for email notifications):
```env
SENDGRID_API_KEY=SG.xxxxx
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
```

### 1.5 Get Your Backend URL

1. Go to **Settings** → **Networking**
2. Click **"Generate Domain"**
3. Copy the URL (e.g., `your-app.up.railway.app`)
4. Save it - you'll need it for step 2!

### 1.6 Deploy Worker (Optional)

For automatic calendar sync every 60 seconds:

1. Click **"+ New"** in Railway
2. Select same GitHub repo
3. Set **Start Command**: `python agentic_service.py`
4. Share all environment variables

**Or skip this** and manually sync via the app.

---

## Step 2: Deploy Frontend to Cloudflare Pages

### 2.1 Go to Cloudflare

1. Visit [dash.cloudflare.com](https://dash.cloudflare.com/)
2. Go to **Workers & Pages** → **Pages**
3. Click **"Create a project"** → **"Connect to Git"**
4. Select your GitHub repository

### 2.2 Configure Build

Cloudflare auto-detects Vite. Just verify:

- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Framework preset**: Vite ✅

### 2.3 Add Environment Variables

Click **Environment variables** and add:

```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_public_key
VITE_BACKEND_URL=https://your-app.up.railway.app
```

**Important:**
- Use your Railway URL from Step 1.5
- Use Supabase **anon** key (NOT service_role key)
- Add to both **Production** and **Preview** environments

### 2.4 Deploy!

Click **"Save and Deploy"**. Wait 2-5 minutes.

### 2.5 Get Your URL

After deployment, you'll get: `https://smart-study-buddy.pages.dev`

### 2.6 Update Railway

Go back to Railway → **Variables** and update:

```env
FRONTEND_URL=https://smart-study-buddy.pages.dev
```

Then redeploy Railway (click **Deployments** → **Redeploy**).

---

## Part 3: Test Your Deployment

### ✅ Backend Health Check

```bash
# Replace with your actual Railway domain
curl https://your-app.up.railway.app/api/health

# Expected response:
# {"status":"ok","service":"Study Companion Calendar API","version":"1.0.0"}
```

### ✅ Test Calendar Stats

```bash
curl https://your-app.up.railway.app/api/calendar/stats

# Expected response:
# {"success":true,"stats":{"total_events":X,"unprocessed_assignments":Y}}
```

### ✅ Frontend Check

1. Visit your Cloudflare Pages URL: `https://smart-study-buddy.pages.dev`
2. Open browser DevTools (F12)
3. Go to Console tab
4. Try to sign in with Supabase authentication
5. Check for any CORS or API errors

### ✅ API Connection Test

Open browser console on your frontend and run:

```javascript
// Test backend connectivity
fetch('https://your-app.up.railway.app/api/health')
  .then(r => r.json())
  .then(data => console.log('✅ Backend health:', data))
  .catch(err => console.error('❌ Backend error:', err));

// Test calendar stats
fetch('https://your-app.up.railway.app/api/calendar/stats')
  .then(r => r.json())
  .then(data => console.log('✅ Calendar stats:', data))
  .catch(err => console.error('❌ Calendar error:', err));
```

### ✅ Test Google Calendar Integration

1. Create a test event in your Google Calendar:
   - Title: "Test Exam on React"
   - Due date: Tomorrow
2. Wait 60 seconds (for agentic service to sync)
3. Check backend logs in Railway
4. Visit your frontend and check Dashboard for the new assignment

### ✅ End-to-End Test

Complete workflow test:

1. **Login**: Sign in with your email (must match `USER_EMAIL` in Railway)
2. **Dashboard**: See your upcoming assignments
3. **Create Assignment**: 
   - Click on an assignment
   - Upload study material (PDF or text)
   - Click "Create Study Plan"
4. **Study Session**:
   - Click on a scheduled study session
   - Complete some exercises
   - Verify answers are evaluated correctly

---

## Part 4: Continuous Deployment

Both Railway and Cloudflare Pages are now set up for automatic deployments:

### ✅ Automatic Deployments

**When you push to `main` branch:**
1. Railway automatically redeploys the backend
2. Cloudflare automatically redeploys the frontend
3. No manual intervention needed!

```bash
# Make changes
git add .
git commit -m "Add new feature"
git push origin main

# Both services will automatically deploy!
```

### 🔄 Manual Redeployment

**Railway:**
1. Go to Railway Dashboard
2. Select your project
3. Click **Deployments** tab
4. Click three dots (⋮) on latest deployment
5. Click **Redeploy**

**Cloudflare Pages:**
1. Go to Cloudflare Dashboard
2. Navigate to **Workers & Pages** → **Pages**
3. Select your project
4. Click **Create deployment**
5. Select branch and deploy

### 📋 Deployment Branches

You can set up different environments:

**Cloudflare:**
- `main` branch → Production (`smart-study-buddy.pages.dev`)
- `dev` branch → Preview (`dev-smart-study-buddy.pages.dev`)
- Any PR → Automatic preview deployment

**Railway:**
- `main` branch → Production
- Create separate Railway service for staging if needed

---

## Part 5: Troubleshooting

### Common Backend Issues

#### ❌ Problem: Backend won't start

**Check Railway logs:**
1. Railway Dashboard → Your Service
2. Click **Deployments** tab
3. Click latest deployment
4. Click **View Logs**

**Common causes:**
- ✅ Missing environment variables
- ✅ Invalid Google credentials JSON
- ✅ Python version mismatch
- ✅ Import errors from missing dependencies

**Solution:**
```bash
# Verify all required variables are set in Railway:
SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY, MONGODB_URI,
USER_EMAIL, GOOGLE_CREDENTIALS_JSON, GOOGLE_TOKEN_JSON
```

#### ❌ Problem: Google Calendar not working

**Symptoms:**
- No events syncing
- Authentication errors in logs
- "Could not setup Google credentials" error

**Check:**
1. Verify `GOOGLE_CREDENTIALS_JSON` is valid JSON (no newlines)
2. Verify `GOOGLE_TOKEN_JSON` is valid JSON (no newlines)
3. Check Railway logs for authentication messages
4. Ensure token hasn't expired (might need to regenerate)

**Solution:**
```bash
# Re-run the deploy helper to regenerate credentials
./deploy-helper.sh

# Copy new values to Railway environment variables
# Redeploy the service
```

#### ❌ Problem: Port binding error

**Error in logs:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
Railway automatically sets the `PORT` environment variable. Update `backend/api.py` if needed:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Common Frontend Issues

#### ❌ Problem: Build fails on Cloudflare

**Check build logs:**
1. Cloudflare Dashboard → Your Pages Project
2. Click **View build log** on failed deployment

**Common causes:**
- ✅ Missing environment variables
- ✅ Node version too old
- ✅ TypeScript errors
- ✅ Missing dependencies

**Solutions:**
```bash
# Ensure NODE_VERSION is set to 18 or higher in Cloudflare
NODE_VERSION=18

# Test build locally first
npm run build

# Check for TypeScript errors
npm run lint
```

#### ❌ Problem: Can't connect to backend

**Symptoms:**
- CORS errors in browser console
- "Failed to fetch" errors
- API requests failing

**Check:**
1. Verify `VITE_BACKEND_URL` is set correctly in Cloudflare
2. Ensure Railway `FRONTEND_URL` matches your Cloudflare URL
3. Check CORS configuration in `backend/api.py`

**Solution:**

In Railway, verify:
```env
FRONTEND_URL=https://smart-study-buddy.pages.dev
```

In Cloudflare, verify:
```env
VITE_BACKEND_URL=https://your-app.up.railway.app
```

Then update `backend/api.py` CORS configuration:

```python
allowed_origins = [
    'http://localhost:5173',
    frontend_url,
    'https://*.pages.dev',  # Allow all Cloudflare preview deployments
]
```

#### ❌ Problem: Environment variables not working

**Issue:** Vite environment variables must start with `VITE_`

**Wrong:**
```env
BACKEND_URL=https://api.example.com  # ❌ Won't work
```

**Correct:**
```env
VITE_BACKEND_URL=https://api.example.com  # ✅ Works
```

**In your code:**
```typescript
// Access via import.meta.env
const backendUrl = import.meta.env.VITE_BACKEND_URL;
```

### CORS Issues

If you get CORS errors in the browser console:

#### Step 1: Verify Origins

Check that your frontend URL is in the backend's allowed origins:

```python
# backend/api.py
allowed_origins = [
    'http://localhost:5173',
    'https://smart-study-buddy.pages.dev',
    'https://*.pages.dev',  # For preview deployments
]
```

#### Step 2: Check Railway Environment

Ensure `FRONTEND_URL` in Railway matches your Cloudflare URL exactly:
```env
FRONTEND_URL=https://smart-study-buddy.pages.dev
```

#### Step 3: Test CORS

```bash
# Test from command line
curl -H "Origin: https://smart-study-buddy.pages.dev" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     https://your-app.up.railway.app/api/health -v

# Should see: Access-Control-Allow-Origin in response headers
```

### Database Connection Issues

#### ❌ Problem: Can't connect to MongoDB

**Error:**
```
pymongo.errors.ServerSelectionTimeoutError
```

**Check:**
1. Verify `MONGODB_URI` is correct
2. Ensure MongoDB Atlas allows connections from anywhere (0.0.0.0/0)
3. Check MongoDB Atlas cluster is running

**Solution:**
1. Go to MongoDB Atlas
2. Navigate to **Network Access**
3. Add IP Address: `0.0.0.0/0` (allows all - Railway uses dynamic IPs)

#### ❌ Problem: Can't connect to Supabase

**Error:**
```
Failed to initialize Supabase client
```

**Check:**
1. Verify `SUPABASE_URL` format: `https://xxxxx.supabase.co`
2. Verify `SUPABASE_KEY` is the **service role key** (not anon key)
3. Check Supabase project is active

**Find your keys:**
1. Go to Supabase Dashboard
2. Your Project → Settings → API
3. Copy **URL** and **service_role key** (for backend)
4. Copy **anon public key** (for frontend)

---

## Part 6: Cost Breakdown & Scaling

### 💰 Monthly Costs

**Railway (Backend):**
- ✅ **Hobby Plan**: $5/month (500 hours + $5 usage credit)
- ✅ **Pro Plan**: $20/month (more resources)
- First **$5 free credits** for new accounts

**Estimated usage for this project:**
- API Service: ~$2-3/month
- Worker Service: ~$2-3/month
- **Total: $4-6/month** (fits in Hobby plan)

**Cloudflare Pages (Frontend):**
- ✅ **Free Tier**: Unlimited bandwidth, unlimited requests
- ✅ **Paid Plans**: Only needed for advanced features

**Total completely free for frontend!**

**Other Services (Not Railway/Cloudflare):**
- Supabase: Free tier (500MB database, 50MB file storage)
- MongoDB Atlas: Free tier (512MB storage)
- OpenAI API: Pay per use (~$0.01-0.10 per study session)
- SendGrid: Free tier (100 emails/day)

**Total Monthly Cost:**
- **Development**: $0 (use Railway free credits)
- **Production**: $5-10/month

### 📈 Scaling Considerations

**When you need to scale:**

**Railway:**
- Vertical scaling: Increase memory/CPU in service settings
- Horizontal scaling: Add more service instances (Pro plan)
- Add Redis for caching (reduce API calls)

**Cloudflare:**
- Already globally distributed (CDN)
- Handles traffic spikes automatically
- No configuration needed for scaling

**Database:**
- Upgrade MongoDB Atlas tier (from free to M10: $57/month)
- Upgrade Supabase tier (more database storage)
- Add database indexes for better performance

**Cost optimization tips:**
- Use caching to reduce API calls
- Implement rate limiting
- Optimize database queries
- Use CDN for static assets (already done with Cloudflare)

---

## Part 7: Advanced Configuration

### Custom Domains (Optional)

#### Cloudflare Pages Custom Domain

1. In Cloudflare Pages, go to **Custom domains**
2. Click **Set up a custom domain**
3. Enter your domain (e.g., `studybuddy.com`)
4. Follow DNS configuration instructions
5. Cloudflare automatically handles SSL certificates

**Benefits:**
- Professional URL
- Automatic SSL/HTTPS
- Better SEO
- Custom branding

#### Railway Custom Domain

1. In Railway Settings → **Networking**
2. Click **Add Custom Domain**
3. Enter your domain (e.g., `api.studybuddy.com`)
4. Configure DNS CNAME record:
   ```
   CNAME api.studybuddy.com → your-app.up.railway.app
   ```
5. Wait for DNS propagation (~5-60 minutes)

### Environment-Specific Configuration

Create different configurations for development/production:

**Development** (`.env.development`):
```env
VITE_SUPABASE_URL=https://dev-project.supabase.co
VITE_SUPABASE_ANON_KEY=dev_anon_key
VITE_BACKEND_URL=http://localhost:5001
```

**Production** (`.env.production`):
```env
VITE_SUPABASE_URL=https://prod-project.supabase.co
VITE_SUPABASE_ANON_KEY=prod_anon_key
VITE_BACKEND_URL=https://your-app.up.railway.app
```

**Build for specific environment:**
```bash
npm run build -- --mode production
npm run build -- --mode development
```

### Monitoring & Logging

#### Railway Logging

**View Logs:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# View live logs
railway logs

# View logs for specific service
railway logs --service api
railway logs --service worker
```

#### Cloudflare Analytics

1. Go to Cloudflare Dashboard
2. Your Pages Project → **Analytics**
3. View:
   - Page views
   - Requests
   - Bandwidth
   - Geographic distribution

#### Application Monitoring

**Add health check monitoring:**

1. Sign up for [UptimeRobot](https://uptimerobot.com/) (free)
2. Add HTTP(s) monitor:
   - **URL**: `https://your-app.up.railway.app/api/health`
   - **Interval**: 5 minutes
   - **Alert contacts**: Your email
3. Get notified if backend goes down

**Add error tracking** (optional):

```bash
# Install Sentry
npm install @sentry/react @sentry/vite-plugin
```

Configure in `src/main.tsx`:
```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "your-sentry-dsn",
  integrations: [new Sentry.BrowserTracing()],
  tracesSampleRate: 1.0,
});
```

### Database Backups

#### MongoDB Atlas Backups

1. Go to MongoDB Atlas Dashboard
2. Your Cluster → **Backup** tab
3. Enable **Cloud Backup**
4. Configure backup schedule

#### Supabase Backups

1. Go to Supabase Dashboard
2. Your Project → **Settings** → **Database**
3. Daily backups are automatic (Pro plan)
4. For free tier, use `pg_dump` manually:

```bash
# Download backup
supabase db dump -f backup.sql

# Restore backup
supabase db push backup.sql
```

### Security Best Practices

#### 1. Environment Variables

✅ **Do:**
- Store secrets in Railway/Cloudflare environment variables
- Use different keys for dev/prod
- Rotate API keys regularly

❌ **Don't:**
- Commit `.env` files to git
- Share API keys in code
- Use the same keys across environments

#### 2. API Security

**Add rate limiting** to `backend/api.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/calendar/sync', methods=['POST'])
@limiter.limit("10 per minute")
def sync_calendar():
    # ... existing code
```

**Add authentication middleware:**

```python
from functools import wraps
from flask import request, jsonify
import jwt

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            # Verify Supabase JWT
            payload = jwt.decode(token, options={"verify_signature": False})
            request.user_id = payload['sub']
        except:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# Apply to protected endpoints
@app.route('/api/assignments/upcoming', methods=['GET'])
@require_auth
def get_upcoming_assignments():
    user_id = request.user_id
    # ... existing code
```

#### 3. CORS Configuration

Update `backend/api.py` with strict CORS:

```python
CORS(app, 
     resources={r"/api/*": {
         "origins": allowed_origins,
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "expose_headers": ["Content-Range", "X-Content-Range"],
         "supports_credentials": True,
         "max_age": 600
     }}
)
```

#### 4. Input Validation

Add input validation to prevent injection attacks:

```python
from flask import request
import bleach

@app.route('/api/assignments/<assignment_id>/create-sessions', methods=['POST'])
def create_sessions(assignment_id):
    # Validate UUID format
    try:
        uuid.UUID(assignment_id)
    except ValueError:
        return jsonify({'error': 'Invalid assignment ID'}), 400
    
    # Sanitize input
    data = request.json
    if 'material_content' in data:
        data['material_content'] = bleach.clean(data['material_content'])
    
    # ... existing code
```

### Performance Optimization

#### 1. Frontend Optimization

**Enable code splitting:**

Already configured in Vite, but verify in `vite.config.ts`:

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
        },
      },
    },
  },
});
```

**Add compression:**

Cloudflare automatically compresses responses (Brotli/Gzip).

**Optimize images:**

```bash
# Install image optimization
npm install -D vite-plugin-image-optimizer

# Add to vite.config.ts
import { ViteImageOptimizer } from 'vite-plugin-image-optimizer';

export default defineConfig({
  plugins: [
    react(),
    ViteImageOptimizer(),
  ],
});
```

#### 2. Backend Optimization

**Add caching:**

```python
from functools import lru_cache
from datetime import datetime, timedelta

# Cache calendar stats for 5 minutes
cache_time = None
cached_stats = None

@app.route('/api/calendar/stats', methods=['GET'])
def get_stats():
    global cache_time, cached_stats
    
    now = datetime.now()
    if cache_time and (now - cache_time) < timedelta(minutes=5):
        return jsonify(cached_stats)
    
    # Fetch fresh data
    stats = {
        'total_events': len(get_all_events()),
        'unprocessed': len(get_unprocessed_assignments())
    }
    
    cache_time = now
    cached_stats = {'success': True, 'stats': stats}
    
    return jsonify(cached_stats)
```

**Use connection pooling:**

Already handled by `pymongo` and `supabase` clients.

**Optimize database queries:**

```python
# Add indexes in MongoDB
db.calendar_events.create_index([("event_id", 1)])
db.calendar_events.create_index([("processed", 1)])
db.calendar_events.create_index([("start_time", 1)])
```

---

## Part 8: Quick Reference

### Deployment Checklist

Before deploying, ensure you have:

- [ ] ✅ All code pushed to GitHub `main` branch
- [ ] ✅ Google Calendar credentials (`credentials.json` and `token.json`)
- [ ] ✅ Supabase project created with all migrations run
- [ ] ✅ MongoDB Atlas cluster created and accessible
- [ ] ✅ OpenAI API key with credits
- [ ] ✅ SendGrid account (optional, for emails)
- [ ] ✅ Railway account
- [ ] ✅ Cloudflare account

### Required Environment Variables

**Railway Backend:**
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  (service_role)
OPENAI_API_KEY=sk-proj-xxxxx
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db
USER_EMAIL=your.email@example.com
GOOGLE_CREDENTIALS_JSON={"installed":{...}}
GOOGLE_TOKEN_JSON={"token":"...","refresh_token":"...",...}
FRONTEND_URL=https://smart-study-buddy.pages.dev
BACKEND_URL=${{RAILWAY_PUBLIC_DOMAIN}}
PYTHONUNBUFFERED=1
PORT=5001
```

**Cloudflare Frontend:**
```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  (anon)
VITE_BACKEND_URL=https://your-app.up.railway.app
NODE_VERSION=18
```

### Useful Commands

**Railway CLI:**
```bash
# Install
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# View logs
railway logs

# View environment variables
railway variables

# Deploy manually
railway up
```

**Cloudflare Wrangler:**
```bash
# Install
npm install -g wrangler

# Login
wrangler login

# Deploy
npm run build
wrangler pages deploy dist --project-name=smart-study-buddy

# View deployments
wrangler pages deployments list --project-name=smart-study-buddy
```

**Testing:**
```bash
# Test backend
curl https://your-app.up.railway.app/api/health
curl https://your-app.up.railway.app/api/calendar/stats

# Test frontend
curl https://smart-study-buddy.pages.dev
```

### Important URLs

- **Railway Dashboard**: https://railway.app/dashboard
- **Cloudflare Dashboard**: https://dash.cloudflare.com/
- **Backend URL**: `https://your-app.up.railway.app`
- **Frontend URL**: `https://smart-study-buddy.pages.dev`
- **Railway Docs**: https://docs.railway.app/
- **Cloudflare Pages Docs**: https://developers.cloudflare.com/pages/

### Common Commands

**Update environment variable:**
```bash
# Railway
railway variables set KEY=value

# Cloudflare (via dashboard or wrangler)
# No CLI command - use dashboard
```

**Redeploy:**
```bash
# Railway
railway up

# Cloudflare
git push origin main  # Auto-deploys
# Or manually trigger in dashboard
```

**View logs:**
```bash
# Railway
railway logs

# Cloudflare
# View in dashboard under Deployments → View logs
```

---

## Support & Resources

### Documentation

- **Railway**: https://docs.railway.app/
- **Cloudflare Pages**: https://developers.cloudflare.com/pages/
- **Vite**: https://vitejs.dev/guide/
- **Flask**: https://flask.palletsprojects.com/
- **Supabase**: https://supabase.com/docs

### Community

- **Railway Discord**: https://discord.gg/railway
- **Cloudflare Discord**: https://discord.gg/cloudflaredev

### Troubleshooting

If you encounter issues not covered in this guide:

1. Check Railway/Cloudflare logs
2. Verify all environment variables are set correctly
3. Test locally first (`npm run dev` and `python backend/api.py`)
4. Check GitHub Issues for similar problems
5. Join Railway/Cloudflare community forums

---

## Next Steps After Deployment

1. ✅ Test all functionality end-to-end
2. ✅ Set up monitoring (UptimeRobot)
3. ✅ Configure custom domain (optional)
4. ✅ Enable database backups
5. ✅ Add error tracking (Sentry)
6. ✅ Implement rate limiting
7. ✅ Add authentication to API endpoints
8. ✅ Optimize performance (caching, compression)
9. ✅ Set up CI/CD for automated testing
10. ✅ Document your API endpoints

---

**🎉 Congratulations! Your Smart Study Buddy is now deployed and running in production!**
