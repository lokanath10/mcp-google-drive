#!/usr/bin/env python3
"""
Script to handle Google Drive OAuth flow and save the refresh token.
Run this once to set up authentication, then the server can use the saved token.
"""

import os
import argparse
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the token file.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def setup_auth(credentials_path: str, token_path: str = 'tokens.json') -> None:
    """Set up Google Drive authentication and save the refresh token.
    
    Args:
        credentials_path: Path to the credentials.json file
        token_path: Path where to save the token (default: tokens.json)
    """
    creds = None
    token_path = Path(token_path)
    
    # Check if token exists and is valid
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            print(f"Error loading token file: {e}")
            token_path.unlink(missing_ok=True)  # Remove corrupted token file

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None

        if not creds:
            print("Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            print("OAuth flow completed successfully!")

        # Save the credentials for future use
        token_path.write_text(creds.to_json())
        print(f"Credentials saved to {token_path}")

def main():
    parser = argparse.ArgumentParser(description='Google Drive Authentication Setup')
    parser.add_argument('--credentials', required=True, help='Path to credentials.json file')
    parser.add_argument('--token', default='tokens.json', help='Path to save the token (default: tokens.json)')
    args = parser.parse_args()

    setup_auth(args.credentials, args.token)

if __name__ == '__main__':
    main() 