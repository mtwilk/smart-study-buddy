#!/bin/bash
# Script to find and remove AgentStatus component

echo "Searching for AgentStatus component..."

# Find the file
AGENT_FILES=$(find . -name "AgentStatus.tsx" -o -name "AgentStatus.ts" 2>/dev/null | grep -v node_modules | grep -v .git)

if [ -z "$AGENT_FILES" ]; then
    echo "No AgentStatus component files found."
else
    echo "Found AgentStatus files:"
    echo "$AGENT_FILES"
    echo ""
    echo "Removing files..."
    echo "$AGENT_FILES" | while read -r file; do
        rm -f "$file"
        echo "  Removed: $file"
    done
fi

# Find and remove imports
echo ""
echo "Searching for AgentStatus imports..."

FILES_WITH_IMPORTS=$(grep -r "from.*AgentStatus" src/ 2>/dev/null | grep -v node_modules | cut -d: -f1 | sort -u)

if [ -z "$FILES_WITH_IMPORTS" ]; then
    echo "No imports found."
else
    echo "Found imports in:"
    echo "$FILES_WITH_IMPORTS"
    echo ""
    echo "Removing imports and usage..."

    for file in $FILES_WITH_IMPORTS; do
        echo "  Processing: $file"
        # Remove import line
        sed -i "/import.*AgentStatus/d" "$file"
        # Remove JSX usage (component tag)
        sed -i "/<AgentStatus/d" "$file"
        echo "    Cleaned imports and usage"
    done
fi

echo ""
echo "Done! AgentStatus component has been removed."
echo "Please review the changes and commit them."
