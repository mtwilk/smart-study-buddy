#!/usr/bin/env python3
"""Fix empty except/if/else/try/for blocks by adding pass statements."""

import re
import sys
from pathlib import Path

def fix_empty_blocks(content):
    """Add 'pass' statements to empty blocks."""
    lines = content.split('\n')
    fixed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)

        # Check if this line starts a block (ends with :)
        stripped = line.strip()
        if stripped.endswith(':') and not stripped.startswith('#'):
            # Get indentation of current line
            current_indent = len(line) - len(line.lstrip())

            # Check next line
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_stripped = next_line.strip()

                # If next line is empty or has same/less indentation (not counting comments)
                if not next_stripped or (not next_stripped.startswith('#') and
                                        len(next_line) - len(next_line.lstrip()) <= current_indent):
                    # Add pass statement with proper indentation
                    pass_line = ' ' * (current_indent + 4) + 'pass'
                    fixed_lines.append(pass_line)

        i += 1

    return '\n'.join(fixed_lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_empty_blocks.py <file1.py> [file2.py] ...")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        path = Path(filepath)
        if not path.exists():
            print(f"File not found: {filepath}")
            continue

        print(f"Fixing {filepath}...")
        content = path.read_text()
        fixed = fix_empty_blocks(content)
        path.write_text(fixed)
        print(f"  Done!")

if __name__ == '__main__':
    main()
