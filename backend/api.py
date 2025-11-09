# api.py - Flask API for calendar integration
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import (
    get_upcoming_assignments,
    get_all_events,
    get_unprocessed_assignments
)
from assignment_sync import (
    check_and_sync_for_user,
    send_proactive_reminders,
    create_sessions_for_assignment
)
from calendar_reader import list_and_store_events
from agentic_service import agent, start_agent, stop_agent, get_agent_status
from email_service import send_test_email
import traceback
import atexit
import os

# Setup Google Calendar credentials from environment variables (if provided)
try:
    from setup_credentials import setup_google_credentials
    setup_google_credentials()
except Exception as e:
    print(f"Warning: Could not setup Google credentials: {e}")

app = Flask(__name__)

# Configure CORS for both local development and production
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
allowed_origins = [
    'http://localhost:5173',  # Local development
    'http://0.0.0.0:5173',    # Dockerized frontend served via 0.0.0.0
    'http://localhost:8080',  # Vite preview
    frontend_url,  # Production frontend URL from environment variable
]

# Enable CORS with support for credentials
CORS(app, 
     resources={r"/*": {"origins": allowed_origins}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# Stop agent gracefully when Flask shuts down
atexit.register(stop_agent)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'Study Companion Calendar API'})

@app.route('/api/health', methods=['GET'])
def api_health_check():
    """API Health check endpoint for Railway."""
    return jsonify({'status': 'ok', 'service': 'Study Companion Calendar API', 'version': '1.0.0'})

@app.route('/api/calendar/stats', methods=['GET'])
def get_stats():
    """Get quick stats without full sync."""
    try:
        all_events = get_all_events()
        unprocessed = get_unprocessed_assignments()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_events': len(all_events),
                'unprocessed_assignments': len(unprocessed)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/calendar/sync', methods=['POST'])
def sync_calendar():
    """
    Fetch events from Google Calendar and store in MongoDB.
    Body: { "days_ahead": 90 }
    """
    try:
        pass
        
        data = request.json or {}
        days_ahead = data.get('days_ahead', 90)
        
        
        success = list_and_store_events(days_ahead)
        
        if success:
            # Get stats
            all_events = get_all_events()
            unprocessed = get_unprocessed_assignments()
            
            
            return jsonify({
                'success': True,
                'message': 'Calendar synced successfully',
                'stats': {
                    'total_events': len(all_events),
                    'unprocessed_assignments': len(unprocessed)
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to sync calendar'
            }), 500
            
    except Exception as e:
        error_msg = str(e)
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': error_msg,
            'hint': 'Check that token.json is in the backend/ folder and MongoDB connection works'
        }), 500

@app.route('/api/calendar/events', methods=['GET'])
def get_events():
    """Get all calendar events from MongoDB."""
    try:
        events = get_all_events()
        
        # Convert ObjectId to string for JSON serialization
        for event in events:
            event['_id'] = str(event['_id'])
        
        return jsonify({
            'success': True,
            'events': events
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/assignments/unprocessed', methods=['GET'])
def get_unprocessed():
    """Get unprocessed assignments from calendar."""
    try:
        assignments = get_unprocessed_assignments()
        
        # Convert ObjectId to string
        for assignment in assignments:
            assignment['_id'] = str(assignment['_id'])
        
        return jsonify({
            'success': True,
            'assignments': assignments,
            'count': len(assignments)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/assignments/sync-to-supabase', methods=['POST'])
def sync_to_supabase():
    """
    Sync unprocessed calendar assignments to Supabase.
    Body: { "user_email": "user@example.com" }
    """
    try:
        data = request.json
        user_email = data.get('user_email')
        
        if not user_email:
            return jsonify({
                'success': False,
                'error': 'user_email is required'
            }), 400
        
        result = check_and_sync_for_user(user_email)

        # Handle both old (list) and new (dict) return format
        if isinstance(result, dict):
            return jsonify({
                'success': True,
                'message': f"Created {result['assignments_count']} assignments successfully",
                'created_assignments': result['created_assignments'],
                'reminders': result['reminders'],
                'assignments_count': result['assignments_count'],
                'reminders_count': result['reminders_count']
            })
        else:
            # Old format compatibility (if result is just a list of reminders)
            return jsonify({
                'success': True,
                'message': 'Assignments synced successfully',
                'reminders': result or []
            })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reminders/check', methods=['POST'])
def check_reminders():
    """
    Check for upcoming assignments and generate reminders.
    Body: { "user_email": "user@example.com", "days_ahead": 7 }
    """
    try:
        data = request.json
        user_email = data.get('user_email')
        days_ahead = data.get('days_ahead', 7)
        
        if not user_email:
            return jsonify({
                'success': False,
                'error': 'user_email is required'
            }), 400
        
        # Get user ID from Supabase
        from assignment_sync import get_supabase_client
        supabase = get_supabase_client()
        result = supabase.table('profiles').select('id').eq('email', user_email).execute()
        
        if not result.data:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        user_id = result.data[0]['id']
        
        # Get reminders
        reminders = send_proactive_reminders(user_id, days_ahead)
        
        return jsonify({
            'success': True,
            'reminders': reminders,
            'count': len(reminders)
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/assignments/upcoming', methods=['GET'])
def get_upcoming():
    """Get upcoming assignments from MongoDB."""
    try:
        days = request.args.get('days', 30, type=int)
        assignments = get_upcoming_assignments(days)
        
        # Convert ObjectId to string
        for assignment in assignments:
            assignment['_id'] = str(assignment['_id'])
        
        return jsonify({
            'success': True,
            'assignments': assignments,
            'count': len(assignments)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/assignments/<assignment_id>/create-sessions', methods=['POST'])
def create_sessions_for_assignment_endpoint(assignment_id):
    """
    Create study sessions for an assignment after materials are uploaded.
    Body: { "user_id": "uuid-here" }
    """
    try:
        data = request.json
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id is required'
            }), 400

        sessions_created = create_sessions_for_assignment(assignment_id, user_id)

        if sessions_created > 0:
            return jsonify({
                'success': True,
                'message': f'Created {sessions_created} study sessions',
                'sessions_created': sessions_created
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create study sessions'
            }), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/agent/status', methods=['GET'])
def agent_status():
    """Get the status of the agentic AI agent."""
    try:
        status = get_agent_status()
        return jsonify({
            'success': True,
            'agent': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agent/start', methods=['POST'])
def start_agent_endpoint():
    """Manually start the agent (if stopped)."""
    try:
        start_agent()
        return jsonify({
            'success': True,
            'message': 'Agent started successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/agent/stop', methods=['POST'])
def stop_agent_endpoint():
    """Manually stop the agent."""
    try:
        stop_agent()
        return jsonify({
            'success': True,
            'message': 'Agent stopped successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/email/test', methods=['POST'])
def test_email():
    """Test email configuration by sending a test email."""
    try:
        data = request.json
        user_email = data.get('user_email')

        if not user_email:
            return jsonify({
                'success': False,
                'error': 'user_email is required'
            }), 400

        success, message = send_test_email(user_email)

        if success:
            return jsonify({
                'success': True,
                'message': 'Test email sent successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/mongodb/reset', methods=['POST'])
def reset_mongodb():
    """
    Reset MongoDB processed flags so assignments can be synced again.
    Useful for testing after clearing Supabase database.
    """
    try:
        from database import get_database

        db = get_database()
        collection = db["calendar_events"]

        # Count before reset
        total_assignments = collection.count_documents({'is_assignment': True})
        processed_before = collection.count_documents({'is_assignment': True, 'processed': True})

        # Reset processed and reminder_sent flags
        result = collection.update_many(
            {'is_assignment': True},
            {'$set': {
                'processed': False,
                'reminder_sent': False
            }}
        )

        # Count after reset
        processed_after = collection.count_documents({'is_assignment': True, 'processed': True})

        return jsonify({
            'success': True,
            'message': f'Reset {result.modified_count} assignment(s)',
            'stats': {
                'total_assignments': total_assignments,
                'processed_before': processed_before,
                'processed_after': processed_after,
                'unprocessed_now': total_assignments - processed_after
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    pass
    
    # Get port from environment variable (Railway sets this)
    port = int(os.getenv('PORT', 5001))
    
    # Start the agentic AI agent
    start_agent()
    
    # Disable reloader to prevent scheduler conflicts
    # Set use_reloader=False when running with APScheduler
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
