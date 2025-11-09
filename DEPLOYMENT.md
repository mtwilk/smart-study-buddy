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

## Need Help?

- **Railway logs**: Railway Dashboard → Deployments → View Logs
- **Cloudflare logs**: Cloudflare Dashboard → Pages → Your Project → View Build Logs
- **Test locally first**: `npm run dev` and `python backend/api.py`
