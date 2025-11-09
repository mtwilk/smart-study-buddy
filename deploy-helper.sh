#!/bin/bash

# Railway Deployment Helper Script
# This script helps you prepare your project for Railway deployment

echo "🚀 Railway Deployment Helper"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "backend/api.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "✅ Project structure verified"
echo ""

# Check if required files exist
echo "📋 Checking deployment files..."
if [ -f "backend/Procfile" ]; then
    echo "✅ Procfile exists"
else
    echo "❌ Procfile missing"
fi

if [ -f "backend/runtime.txt" ]; then
    echo "✅ runtime.txt exists"
else
    echo "❌ runtime.txt missing"
fi

if [ -f "backend/requirements.txt" ]; then
    echo "✅ requirements.txt exists"
else
    echo "❌ requirements.txt missing"
fi

echo ""

# Check for sensitive files
echo "🔒 Checking for sensitive files..."
if [ -f "backend/.env" ]; then
    echo "⚠️  .env file exists - make sure it's in .gitignore"
fi

if [ -f "backend/credentials.json" ]; then
    echo "⚠️  credentials.json exists - this should NOT be committed"
    echo "   You'll need to set this up separately on Railway"
fi

if [ -f "backend/token.json" ]; then
    echo "⚠️  token.json exists - this should NOT be committed"
    echo "   You'll need to set this up separately on Railway"
fi

echo ""

# Check git status
echo "📦 Checking git status..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "✅ Git repository detected"
    
    # Check if there are uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "⚠️  You have uncommitted changes:"
        git status --short
        echo ""
        echo "💡 Commit these changes before deploying:"
        echo "   git add ."
        echo "   git commit -m 'Prepare for Railway deployment'"
        echo "   git push origin main"
    else
        echo "✅ No uncommitted changes"
    fi
else
    echo "❌ Not a git repository - initialize git first"
fi

echo ""
echo "📝 Next Steps for Railway Deployment:"
echo "======================================"
echo ""
echo "1. Push your code to GitHub:"
echo "   git push origin main"
echo ""
echo "2. Go to Railway.app and create a new project"
echo "   https://railway.app/new"
echo ""
echo "3. Select 'Deploy from GitHub repo'"
echo ""
echo "4. Set Root Directory to: backend"
echo ""
echo "5. Add these environment variables in Railway:"
echo "   - SUPABASE_URL"
echo "   - SUPABASE_KEY"
echo "   - OPENAI_API_KEY"
echo "   - MONGODB_URI"
echo "   - USER_EMAIL"
echo "   - FRONTEND_URL (set after Cloudflare deployment)"
echo "   - SENDGRID_API_KEY (optional)"
echo "   - SENDGRID_FROM_EMAIL (optional)"
echo ""
echo "6. Generate a Railway domain in Settings -> Networking"
echo ""
echo "7. Set up Google Calendar credentials (see DEPLOYMENT.md)"
echo ""
echo "8. Deploy frontend to Cloudflare Pages (see DEPLOYMENT.md)"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
