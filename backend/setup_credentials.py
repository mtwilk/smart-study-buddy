#!/usr/bin/env python3
"""
Setup script to handle Google Calendar credentials from environment variables.
This runs on Railway startup to create the required JSON files.
"""
import os
import json

def setup_google_credentials():
    """
    Create credentials.json and token.json from environment variables.
    Falls back to existing files if env vars not set (for local development).
    """
    
    # Get JSON content from environment variables
    creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    token_json = os.getenv('GOOGLE_TOKEN_JSON')
    
    # If environment variables are set, write them to files
    if creds_json:
        try:
            # Parse to validate JSON
            creds_data = json.loads(creds_json)
            # Write to file
            with open('credentials.json', 'w') as f:
                json.dump(creds_data, f, indent=2)
            print("✓ Created credentials.json from environment variable")
        except json.JSONDecodeError as e:
            print(f"⚠ Warning: GOOGLE_CREDENTIALS_JSON is not valid JSON: {e}")
    else:
        if os.path.exists('credentials.json'):
            print("✓ Using existing credentials.json file")
        else:
            print("⚠ Warning: No credentials.json found and GOOGLE_CREDENTIALS_JSON not set")
    
    if token_json:
        try:
            # Parse to validate JSON
            token_data = json.loads(token_json)
            # Write to file
            with open('token.json', 'w') as f:
                json.dump(token_data, f, indent=2)
            print("✓ Created token.json from environment variable")
        except json.JSONDecodeError as e:
            print(f"⚠ Warning: GOOGLE_TOKEN_JSON is not valid JSON: {e}")
    else:
        if os.path.exists('token.json'):
            print("✓ Using existing token.json file")
        else:
            print("⚠ Warning: No token.json found and GOOGLE_TOKEN_JSON not set")

if __name__ == '__main__':
    setup_google_credentials()
