#!/usr/bin/env python3
"""Remove all emojis from Python files."""

import re
import sys
from pathlib import Path

def remove_emojis(text):
    """Remove all emoji characters from text."""
    # Emoji pattern - covers most common emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def remove_standalone_pass_in_text(content):
    """Remove standalone pass statements that were incorrectly added in text blocks."""
    lines = content.split('\n')
    fixed_lines = []
    in_string = False
    string_char = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Simple heuristic: if line is just "    pass" and not in code context, remove it
        # This is tricky - we'll keep pass statements that are properly indented in code
        # but remove ones that appear to be in string literals
        if stripped == 'pass':
            # Check if previous line suggests we're in a multi-line string or text block
            if i > 0:
                prev_line = lines[i-1].strip()
                # If previous line ends with text (not :), this pass is likely erroneous
                if prev_line and not prev_line.endswith(':') and not prev_line.endswith('\\'):
                    # Skip this pass
                    continue

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python remove_emojis.py <file1.py> [file2.py] ...")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        path = Path(filepath)
        if not path.exists():
            print(f"File not found: {filepath}")
            continue

        print(f"Removing emojis from {filepath}...")
        content = path.read_text(encoding='utf-8')
        cleaned = remove_emojis(content)
        cleaned = remove_standalone_pass_in_text(cleaned)
        path.write_text(cleaned, encoding='utf-8')
        print(f"  Done!")

if __name__ == '__main__':
    main()
