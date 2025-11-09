#!/bin/bash
# Bash script to create .env file

ENV_CONTENT="# ============================================
# AGENTIC AI STUDY COMPANION - CONFIGURATION
# ============================================

USER_EMAIL=doe839319@gmail.com
SENDER_EMAIL=doe839319@gmail.com
SENDER_PASSWORD=qcokkdvzyhskelwo

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

MONGODB_CONNECTION_STRING=mongodb+srv://prosus-db-user:yLFIMGwT48qUKxDG@prosus-db-user.wfei3mu.mongodb.net/?retryWrites=true&w=majority

SUPABASE_URL=https://lcpexhkqaqftaqdtgebp.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxjcGV4aGtxYXFmdGFxZHRnZWJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2MTcwNDIsImV4cCI6MjA3ODE5MzA0Mn0.z6pY_kCftjr1hT6zW7qCVEYHc4D0X8HLAuk_6N2IbcY"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_PATH="$SCRIPT_DIR/.env"

echo "$ENV_CONTENT" > "$ENV_PATH"

echo -e "\033[32m✓ Created .env file at: $ENV_PATH\033[0m"
echo ""
echo -e "\033[36m📋 Configuration:\033[0m"
echo "   USER_EMAIL: doe839319@gmail.com"
echo "   SENDER_EMAIL: doe839319@gmail.com"
echo "   SENDER_PASSWORD: qcokkdvzyhskelwo (16 characters)"
echo ""
echo -e "\033[32m✓ Ready to use!\033[0m"
