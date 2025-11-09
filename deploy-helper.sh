#!/bin/bash

# Smart Study Buddy - Railway Deployment Helper
# This script prepares your Google Calendar credentials for Railway deployment

set -e

echo "🚀 Smart Study Buddy - Railway Deployment Helper"
echo "================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/credentials.json" ]; then
    echo "❌ Error: backend/credentials.json not found"
    echo "   Please run this script from the project root"
    exit 1
fi

if [ ! -f "backend/token.json" ]; then
    echo "❌ Error: backend/token.json not found"
    echo "   Please run 'python backend/google_calendar.py' first to generate token.json"
    exit 1
fi

echo "✅ Found credential files"
echo ""

# Create compact JSON (single line, no whitespace)
echo "� Preparing credentials..."

cd backend

# Check if jq is installed
if command -v jq &> /dev/null; then
    echo "   Using jq for JSON formatting..."
    cat credentials.json | jq -c . > credentials.compact.json
    cat token.json | jq -c . > token.compact.json
else
    echo "   jq not found, using tr (may have minor formatting issues)..."
    cat credentials.json | tr -d '\n\t ' > credentials.compact.json
    cat token.json | tr -d '\n\t ' > token.compact.json
fi

cd ..

echo "✅ Credentials prepared"
echo ""
echo "================================================"
echo "📋 Copy these values to Railway environment variables:"
echo "================================================"
echo ""
echo "GOOGLE_CREDENTIALS_JSON="
cat backend/credentials.compact.json
echo ""
echo ""
echo "GOOGLE_TOKEN_JSON="
cat backend/token.compact.json
echo ""
echo ""
echo "================================================"
echo "✅ Next steps:"
echo "1. Go to Railway Dashboard → Your Service → Variables"
echo "2. Add GOOGLE_CREDENTIALS_JSON and paste the first value above"
echo "3. Add GOOGLE_TOKEN_JSON and paste the second value above"
echo "4. Add your other environment variables (see DEPLOYMENT.md)"
echo "5. Deploy!"
echo "================================================"
