#!/bin/bash
# Bash script to find and fix ALL .env files with wrong Supabase URL
# Run this in the project root: ./fix-all-env-files.sh

echo -e "\033[36m============================================================\033[0m"
echo -e "\033[36m  FINDING AND FIXING ALL .ENV FILES\033[0m"
echo -e "\033[36m============================================================\033[0m"
echo ""

WRONG_URL="dpyvbkrfasiskdrqimhf"
CORRECT_URL="lcpexhkqaqftaqdtgebp"
WRONG_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRweXZia3JmYXNpc2tkcnFpbWhmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2MDEzNzUsImV4cCI6MjA3ODE3NzM3NX0.JGb_M_zbh2Lzrca8O_GY8UtCvMnZocsiUBEbpELsLV8"
CORRECT_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxjcGV4aGtxYXFmdGFxZHRnZWJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2MTcwNDIsImV4cCI6MjA3ODE5MzA0Mn0.z6pY_kCftjr1hT6zW7qCVEYHc4D0X8HLAuk_6N2IbcY"

FILES_FIXED=0
FILES_CHECKED=0

# Find all .env files
echo -e "\033[33mStep 1: Finding all .env files...\033[0m"
ENV_FILES=$(find . -name ".env*" -type f ! -path "*/node_modules/*" ! -path "*/.git/*" 2>/dev/null)
FILE_COUNT=$(echo "$ENV_FILES" | grep -c "^" 2>/dev/null || echo 0)

echo -e "\033[90mFound $FILE_COUNT .env file(s)\033[0m"
echo ""

# Check and fix each file
echo -e "\033[33mStep 2: Checking and fixing files...\033[0m"
while IFS= read -r FILE; do
    if [ -z "$FILE" ]; then
        continue
    fi

    FILES_CHECKED=$((FILES_CHECKED + 1))
    echo -e "\033[90mChecking: $FILE\033[0m"

    CONTENT=$(cat "$FILE")
    NEEDS_FIX=0

    if echo "$CONTENT" | grep -q "$WRONG_URL"; then
        echo -e "  \033[31m✗ Found wrong URL: $WRONG_URL\033[0m"
        CONTENT=$(echo "$CONTENT" | sed "s/$WRONG_URL/$CORRECT_URL/g")
        NEEDS_FIX=1
    fi

    if echo "$CONTENT" | grep -qF "$WRONG_KEY"; then
        echo -e "  \033[31m✗ Found wrong key\033[0m"
        CONTENT=$(echo "$CONTENT" | sed "s|$WRONG_KEY|$CORRECT_KEY|g")
        NEEDS_FIX=1
    fi

    if [ $NEEDS_FIX -eq 1 ]; then
        echo "$CONTENT" > "$FILE"
        echo -e "  \033[32m✓ FIXED!\033[0m"
        FILES_FIXED=$((FILES_FIXED + 1))
    else
        if echo "$CONTENT" | grep -q "$CORRECT_URL"; then
            echo -e "  \033[32m✓ Already correct\033[0m"
        else
            echo -e "  \033[33m⚠ No Supabase URL found (might be a different .env file)\033[0m"
        fi
    fi
    echo ""
done <<< "$ENV_FILES"

# Check supabase/config.toml
echo -e "\033[33mStep 3: Checking supabase/config.toml...\033[0m"
CONFIG_PATH="supabase/config.toml"
if [ -f "$CONFIG_PATH" ]; then
    CONFIG_CONTENT=$(cat "$CONFIG_PATH")
    if echo "$CONFIG_CONTENT" | grep -q "$WRONG_URL"; then
        echo -e "  \033[31m✗ Found wrong project ID in config.toml\033[0m"
        sed -i "s/$WRONG_URL/$CORRECT_URL/g" "$CONFIG_PATH"
        echo -e "  \033[32m✓ FIXED config.toml!\033[0m"
        FILES_FIXED=$((FILES_FIXED + 1))
    elif echo "$CONFIG_CONTENT" | grep -q "$CORRECT_URL"; then
        echo -e "  \033[32m✓ config.toml is correct\033[0m"
    fi
else
    echo -e "  \033[33m⚠ supabase/config.toml not found\033[0m"
fi

echo ""
echo -e "\033[36m============================================================\033[0m"
echo -e "\033[36m  SUMMARY\033[0m"
echo -e "\033[36m============================================================\033[0m"
echo -e "\033[37mFiles checked: $FILES_CHECKED\033[0m"
echo -e "\033[37mFiles fixed: $FILES_FIXED\033[0m"
echo ""

if [ $FILES_FIXED -gt 0 ]; then
    echo -e "\033[32m✓ Fixed $FILES_FIXED file(s)!\033[0m"
    echo ""
    echo -e "\033[33mNEXT STEPS:\033[0m"
    echo -e "\033[37m1. STOP the frontend (Ctrl+C)\033[0m"
    echo -e "\033[37m2. Delete: node_modules/.vite\033[0m"
    echo -e "\033[37m3. Restart: npm run dev\033[0m"
    echo -e "\033[37m4. Test: http://localhost:8080/diagnostic\033[0m"
else
    echo -e "\033[32m✓ All files are already correct!\033[0m"
    echo ""
    echo -e "\033[33mIf diagnostic still shows wrong URL:\033[0m"
    echo -e "\033[37m1. Close terminal and open a NEW one\033[0m"
    echo -e "\033[37m2. Delete node_modules and reinstall:\033[0m"
    echo -e "\033[90m   rm -rf node_modules\033[0m"
    echo -e "\033[90m   npm install\033[0m"
    echo -e "\033[37m3. Restart: npm run dev\033[0m"
fi

echo -e "\033[36m============================================================\033[0m"
