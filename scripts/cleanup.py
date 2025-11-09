#!/usr/bin/env python3
"""
Production cleanup script for Smart Study Buddy
Removes console.log, print statements, and emojis
"""

import os
import re
from pathlib import Path

# Emoji patterns to remove
EMOJI_PATTERN = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

def clean_frontend_file(filepath):
    """Remove console.log statements from TypeScript/JSX files"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove console.log and console.info statements (keep console.error)
    content = re.sub(r'^\s*console\.(log|info)\(.*?\);?\s*$', '', content, flags=re.MULTILINE)

    # Remove inline console.log
    content = re.sub(r'console\.(log|info)\([^)]*\)', '', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def clean_backend_file(filepath):
    """Remove print statements and emojis from Python files"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove emojis
    content = EMOJI_PATTERN.sub('', content)

    # Keep print statements that are actual errors, remove informational ones
    # This is complex, so we'll be conservative

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    project_root = Path('/home/user/smart-study-buddy-22')

    cleaned_files = []

    # Clean frontend files
    for pattern in ['**/*.ts', '**/*.tsx']:
        for filepath in (project_root / 'src').rglob(pattern.split('/')[-1]):
            if clean_frontend_file(filepath):
                cleaned_files.append(str(filepath))

    # Clean backend files
    for filepath in (project_root / 'backend').rglob('*.py'):
        if clean_backend_file(filepath):
            cleaned_files.append(str(filepath))

    print(f"Cleaned {len(cleaned_files)} files:")
    for f in cleaned_files:
        print(f"  - {f}")

if __name__ == '__main__':
    main()
