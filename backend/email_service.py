# email_service.py - Proactive Email Notifications
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
FRONTEND_URL = os.getenv('FRONTEND_URL') or os.getenv('PUBLIC_FRONTEND_URL') or 'http://localhost:5173'

def build_frontend_url(path: str) -> str:
    """Return an absolute frontend URL for the given path."""
    base = FRONTEND_URL.rstrip('/')
    cleaned_path = (path or '').strip()
    if cleaned_path and not cleaned_path.startswith('/'):
        cleaned_path = f'/{cleaned_path}'
    return f'{base}{cleaned_path}'

def send_new_assignment_notification(user_email, assignment_details):
    """
    Send email notification when a new assignment is detected from calendar.
    This prompts the user to login and upload materials BEFORE study sessions are created.

    Args:
        user_email: User's email address
        assignment_details: Dict with assignment info (title, date, course, type, id)
    """

    # Email configuration from environment variables
    from dotenv import load_dotenv
    import os as os_module
    env_path = os_module.path.join(os_module.path.dirname(__file__), '.env')
    load_dotenv(env_path)

    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD', '').strip().replace(' ', '')


    if not sender_email or not sender_password:
        return False

    # Create email message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f" New Assignment Detected: {assignment_details['title']}"
    msg['From'] = f"Study Companion AI <{sender_email}>"
    msg['To'] = user_email

    # Get assignment ID for direct link
    assignment_id = assignment_details.get('id', '')
    assignment_path = f"/assignments/{assignment_id}" if assignment_id else "/assignments"
    assignment_url = build_frontend_url(assignment_path)

    # Email body (plain text)
    text_body = f"""
Hi there! 

Great news! I've detected a new assignment from your calendar:
    pass

 Assignment: {assignment_details['title']}
 Due Date: {assignment_details['date']}
 Type: {assignment_details['type'].title()}

 NEXT STEP: Upload Your Study Materials

To create a personalized study plan with practice questions, I need you to:
    pass

1. Click the link below to go directly to this assignment
2. Upload your study materials:
    Lecture slides
    Course syllabus/instructions
    Practice problems or past exams
    Any other relevant study materials
3. Click "Create Study Plan" to generate your personalized schedule

 Upload materials here: {assignment_url}

Once you upload the materials, I'll automatically:
    pass
 Generate a personalized study schedule
 Create practice questions based on your materials
 Track your progress and adapt difficulty

Let's prepare for success! 

Best,
Your Study Companion AI

---
This is an automated notification. Your assignment was detected from your Google Calendar.
"""

    # Email body (HTML for better formatting)
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
        .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .assignment-card {{ background: #f0f4ff; border-left: 4px solid #667eea; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .action-button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
        .steps {{ background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .step {{ padding: 10px 0; border-left: 3px solid #667eea; padding-left: 15px; margin: 10px 0; }}
        .materials-list {{ background: #fff8e1; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; border-radius: 5px; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> New Assignment Detected!</h1>
            <p style="font-size: 18px; margin: 10px 0 0 0;">Your AI Study Companion is ready to help</p>
        </div>
        <div class="content">
            <p>Hi there! </p>

            <p><strong>Great news!</strong> I've detected a new assignment from your calendar:</p>

            <div class="assignment-card">
                <h2 style="margin: 0 0 10px 0; color: #667eea;"> {assignment_details['title']}</h2>
                <p style="margin: 5px 0;"><strong> Due Date:</strong> {assignment_details['date']}</p>
                <p style="margin: 5px 0;"><strong> Type:</strong> {assignment_details['type'].title()}</p>
            </div>

            <h3 style="color: #667eea;"> NEXT STEP: Upload Your Study Materials</h3>

            <p>To create a personalized study plan with practice questions, please follow these steps:</p>

            <div class="steps">
                <div class="step">
                    <strong>1.</strong> Log in to your Study Companion dashboard
                </div>
                <div class="step">
                    <strong>2.</strong> Navigate to: <em>"{assignment_details['title']}"</em>
                </div>
                <div class="step">
                    <strong>3.</strong> Upload your study materials
                </div>
            </div>

            <div class="materials-list">
                <strong> Materials I can work with:</strong>
                <ul style="margin: 10px 0;">
                    <li> Lecture slides (PDF, PowerPoint)</li>
                    <li> Course syllabus/instructions</li>
                    <li> Practice problems or past exams</li>
                    <li> Textbook chapters or notes</li>
                    <li> Any other relevant study materials</li>
                </ul>
            </div>

            <div style="text-align: center;">
                <a href="{assignment_url}" class="action-button"> Upload Materials for This Assignment</a>
            </div>

            <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <strong> Once you upload the materials, I'll automatically:</strong>
                <ul style="margin: 10px 0;">
                    <li>Generate a personalized study schedule</li>
                    <li>Create practice questions based on your materials</li>
                    <li>Track your progress and adapt difficulty</li>
                </ul>
            </div>

            <p style="margin-top: 30px; text-align: center; color: #667eea; font-weight: bold;">Let's prepare for success! </p>

            <p style="text-align: center; margin-top: 20px;">Best,<br><strong>Your Study Companion AI</strong></p>
        </div>
        <div class="footer">
            This is an automated notification. Your assignment was detected from your Google Calendar.<br>
            To manage notifications, adjust your settings in the dashboard.
        </div>
    </div>
</body>
</html>
"""

    # Attach both plain text and HTML versions
    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Send email
    try:
        pass

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True

    except Exception as e:
        return False


def send_test_email(user_email):
    """Send a test email to verify SMTP configuration."""

    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')

    if not sender_email or not sender_password:
        return False, "Email credentials not configured"

    msg = MIMEText("Your Study Companion AI is now active and monitoring your calendar! ")
    msg['Subject'] = " Study Companion AI - Email Notifications Enabled"
    msg['From'] = sender_email
    msg['To'] = user_email

    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True, "Test email sent successfully"
    except Exception as e:
        return False, str(e)
