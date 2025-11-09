# calendar_reader.py - Fetch events from Google Calendar
from __future__ import print_function
import datetime
import os.path
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from database import insert_event, get_unprocessed_assignments

# Use full calendar scope (same as google_calendar.py)
# This allows both reading and writing with the same token
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Authenticate with Google Calendar and return the service object."""
    creds = None

    # Check multiple possible locations for token
    # Prefer token_write.json (has full permissions) over token.json (might be readonly)
    token_paths = ['token_write.json', 'token.json', './token_write.json', './token.json',
                   'backend/token_write.json', 'backend/token.json']
    credentials_paths = ['credentials.json', './credentials.json', 'backend/credentials.json']

    token_path = None
    credentials_path = None

    for path in token_paths:
        if os.path.exists(path):
            token_path = path
            break

    for path in credentials_paths:
        if os.path.exists(path):
            credentials_path = path
            break

    # Try to load existing token
    if token_path and os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            # Check if scopes match (in case token is from old readonly version)
            if creds and hasattr(creds, 'scopes') and set(creds.scopes) != set(SCOPES):
                creds = None
            else:
                pass
        except Exception as e:
            creds = None

    # Check if we need to refresh or re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                # Save refreshed token - smart path resolution
                if token_path:
                    save_path = token_path
                else:
                    # Determine if we're in the backend directory or root
                    if os.path.exists('credentials.json'):
                        save_path = 'token_write.json'
                    else:
                        save_path = 'backend/token_write.json'

                with open(save_path, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                creds = None

        # If still no valid credentials, re-authenticate
        if not creds or not creds.valid:
            if not credentials_path:
                raise Exception(
                    " credentials.json not found! "
                    "Need it to generate a new token. "
                    "Place credentials.json in the backend/ folder."
                )


            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

            # Save the new token - smart path resolution
            if token_path:
                save_path = token_path
            else:
                # Determine if we're in the backend directory or root
                if os.path.exists('credentials.json'):
                    save_path = 'token_write.json'
                else:
                    save_path = 'backend/token_write.json'

            with open(save_path, 'w') as token:
                token.write(creds.to_json())

    if not creds or not creds.valid:
        raise Exception(" Could not get valid credentials")

    service = build('calendar', 'v3', credentials=creds)
    return service

def list_and_store_events(days_ahead=90):
    """
    Fetch upcoming events from primary calendar and store them in MongoDB.
    Args:
        days_ahead: How many days ahead to fetch events (default 90)
    """
    try:
        service = get_calendar_service()
        calendar_id = 'primary'

        now = datetime.datetime.utcnow()
        future = now + datetime.timedelta(days=days_ahead)
        
        now_str = now.isoformat() + 'Z'
        future_str = future.isoformat() + 'Z'

        
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now_str,
                timeMax=future_str,
                maxResults=100,
                singleEvents=True,
                orderBy='startTime'
            )
            .execute()
        )

        events = events_result.get('items', [])
        
        if not events:
            return

        
        assignments_found = 0
        
        for event in events:
            summary = event.get('summary', 'No Title')
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            # Insert to MongoDB (with error handling)
            try:
                event_id = insert_event({
                    "details": summary,
                    "datetime": start,
                    "google_event_id": event.get('id'),
                    "description": event.get('description', ''),
                    "location": event.get('location', '')
                })
                
                # Check if it's an assignment
                from database import detect_if_assignment
                if detect_if_assignment(summary):
                    assignments_found += 1
                else:
                    pass
            
            except Exception as db_error:
                continue
        
        
        # Show unprocessed assignments
        unprocessed = get_unprocessed_assignments()
        if unprocessed:
            for assignment in unprocessed:
                pass
        
        return True
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    list_and_store_events()

