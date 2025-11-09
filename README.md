# Smart Study Buddy

An intelligent AI-powered study companion that automatically detects assignments from your Google Calendar and generates personalized study sessions with adaptive exercises.

## Features

### Automatic Assignment Detection
- Syncs with Google Calendar every 60 seconds to detect exam and assignment events
- Automatically identifies assignments using keywords (exam, test, quiz, assignment, etc.)
- Filters out study sessions to avoid duplicate detection

### AI-Powered Question Generation
- Generates exercises from your uploaded study materials using OpenAI GPT-4
- Creates 12 diverse exercises per study session across three cognitive tiers
- Questions are based on actual material content, not generic keywords

### Three-Tier Question Framework

**Tier 1: Basic Recall (40% - 5 exercises)**
- Multiple choice questions
- True/False statements
- Flashcards
- Fill-in-the-blank
- Numerical problems

**Tier 2: Understanding (30% - 4 exercises)**
- Short answer (Define)
- Short answer (Explain)
- Short answer (Compare and contrast)

**Tier 3: Application (30% - 3 exercises)**
- Scenario-based application
- Scenario-based prediction
- Error identification
- Mini problem sets

### Smart Study Scheduling
- Automatically schedules 2-4 study sessions before assignment due dates
- Integrates with Google Calendar to avoid scheduling conflicts
- Respects user's preferred study times (morning, afternoon, or evening)
- Creates Google Calendar events for each study session

### Material-Aware Learning
- Questions generated from actual uploaded content (lecture slides, notes, textbooks)
- Analyzes and extracts key concepts from study materials
- Provides contextual explanations based on your materials

### Progress Tracking
- Tracks completion status for all exercises
- Records user answers and evaluates correctness
- Immediate feedback with detailed explanations

### Email Notifications
- Sends notification when new assignment is detected
- Prompts user to upload study materials
- Direct links to assignment pages

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **Supabase client** for authentication and database
- **React Router** for navigation
- **OpenAI** for AI question generation

### Backend
- **Python 3.8+** with Flask
- **Supabase (PostgreSQL)** for relational data storage
- **MongoDB Atlas** for calendar events storage
- **Google Calendar API** for event detection and creation
- **SendGrid** for email notifications
- **APScheduler** for background tasks

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js 18+** and npm ([install with nvm](https://github.com/nvm-sh/nvm))
- **Python 3.8+** ([download here](https://www.python.org/downloads/))
- **Git** ([download here](https://git-scm.com/downloads))

You'll also need accounts for:

- **Supabase** ([sign up](https://supabase.com))
- **Google Cloud Platform** with Calendar API enabled ([console](https://console.cloud.google.com/))
- **OpenAI** with API access ([sign up](https://platform.openai.com/))
- **MongoDB Atlas** ([sign up](https://www.mongodb.com/cloud/atlas))
- **SendGrid** (optional, for email notifications) ([sign up](https://sendgrid.com/))

## Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GIT_URL>
cd smart-study-buddy-22
```

### 2. Install Frontend Dependencies

```bash
npm install
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 4. Set Up Environment Variables

#### Frontend (.env in project root)

```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

#### Backend (backend/.env)

```env
# Supabase
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# MongoDB
MONGODB_URI=your_mongodb_connection_string

# Google Calendar
GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials.json

# SendGrid (optional)
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_verified_sender_email

# Application URLs
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:5001

# User Email (for agentic AI)
USER_EMAIL=your.email@example.com
```

`FRONTEND_URL` is used when generating email links and Google Calendar events. Set it to a URL that your users can actually open (e.g., `https://yourapp.com`) instead of `localhost` when sharing externally.

## Docker Setup

1. **Create environment files**
   - Copy `backend/env.example` to `backend/.env` and fill in secrets (Supabase, MongoDB, OpenAI, SMTP, etc.).
   - Create `.env` in the project root for `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`. These values are injected at build time.
2. **Ensure Google credentials exist**
   - Place `credentials.json` and (if already authorized) `token.json` inside `backend/`. They are mounted into the backend container read-only.
3. **Build containers**

   ```bash
   docker compose build
   ```

4. **Run the stack**

   ```bash
   docker compose up -d
   ```

   - Backend is available at http://localhost:5001.
   - Frontend is served at http://localhost:5173 (nginx serving the Vite build).

5. **View logs / debug**

   ```bash
   docker compose logs -f backend
   docker compose logs -f frontend
   ```

6. **Stop containers**

   ```bash
   docker compose down
   ```

For local iteration you can bind-mount `./backend:/app/backend` in `docker-compose.yml` to enable live-reload style edits, then restart the backend service when dependencies change.

### 5. Set Up Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the credentials and save as `backend/credentials.json`
6. Run the authentication flow:

```bash
cd backend
python google_calendar.py
```

This will open a browser window for you to authorize the application. After authorization, a `token.json` file will be created.

### 6. Set Up Supabase Database

Run the following migrations in order via Supabase SQL Editor:

#### Migration 1: Initial Schema
Run the SQL from `supabase/migrations/20251108134937_*.sql`

#### Migration 2: Add Material Content Column
```sql
ALTER TABLE assignments ADD COLUMN IF NOT EXISTS material_content TEXT;
COMMENT ON COLUMN assignments.material_content IS 'Stores the actual study material content uploaded by the user for AI question generation';
```

#### Migration 3: Fix Split Topics
Run the SQL from `supabase/migrations/20251109010000_fix_split_topics.sql`

### 7. Verify Database Schema

Your Supabase database should have these main tables:

**assignments**
- `id` (uuid, primary key)
- `user_id` (uuid, foreign key)
- `title` (text)
- `type` (text): 'exam', 'assignment', 'quiz'
- `due_at` (timestamptz)
- `topics` (text[]): Array of extracted topics
- `materials_uploaded` (boolean)
- `material_content` (text): Actual study material
- `created_at` (timestamptz)

**study_sessions**
- `id` (uuid, primary key)
- `user_id` (uuid)
- `assignment_id` (uuid, foreign key)
- `scheduled_at` (timestamptz)
- `duration_min` (integer)
- `status` (text)
- `created_at` (timestamptz)

**exercises**
- `id` (uuid, primary key)
- `session_id` (uuid, foreign key)
- `exercise_type` (text)
- `tier` (integer): 1, 2, or 3
- `topic` (text)
- `difficulty` (text)
- `question_payload` (jsonb)
- `user_answer` (jsonb)
- `completed` (boolean)
- `is_correct` (boolean)
- `created_at` (timestamptz)

## Running the Application

### Start the Backend Services

#### Terminal 1: Flask API Server
```bash
cd backend
python api.py
```
The API will run on `http://localhost:5001`

#### Terminal 2: Agentic AI Service
```bash
cd backend
python agentic_service.py
```
This service syncs with Google Calendar every 60 seconds.

### Start the Frontend

#### Terminal 3: React Development Server
```bash
npm run dev
```
The frontend will run on `http://localhost:5173`

## How It Works

### 1. Assignment Detection Flow

1. **Agentic AI** checks Google Calendar every 60 seconds
2. Detects events containing keywords: exam, test, quiz, assignment, midterm, final, etc.
3. Excludes study sessions (events with "study:" prefix or "study session")
4. Extracts topics from event title (e.g., "Exam on Machine Learning" → "Machine Learning")
5. Creates assignment record in Supabase database

### 2. Material Upload Flow

1. User receives email notification about new assignment
2. User logs into the app and navigates to the assignment
3. User uploads study materials (PDF, text, slides, notes, etc.)
4. Material content is stored in `material_content` column
5. User clicks "Create Study Plan" button

### 3. Study Session Generation

1. System analyzes assignment due date and user's calendar
2. Determines number of sessions (1-5 based on days available)
3. For each session:
   - Checks Google Calendar for conflicts
   - Finds optimal time slot (respects 7 AM - 11 PM constraint)
   - Uses user's preferred study time (morning/afternoon/evening)
4. Creates study session records in database
5. Creates corresponding Google Calendar events

### 4. Exercise Generation

When user starts a study session:

1. System generates 12 exercises across three tiers
2. Each exercise uses uploaded material content as context
3. OpenAI GPT-4 generates questions based on:
   - Exercise type (MCQ, short answer, scenario, etc.)
   - Topic extracted from assignment title
   - Difficulty level
   - Actual material content
4. Questions are stored with correct answers and explanations

### 5. User Experience

1. User completes exercises one by one
2. Submits answers
3. System evaluates correctness
4. Provides immediate feedback with explanations
5. Tracks progress for each session

## API Endpoints

### Calendar

- `POST /api/calendar/sync` - Manually sync Google Calendar events
- `GET /api/calendar/events` - Get all stored calendar events
- `GET /api/calendar/stats` - Get calendar statistics

### Assignments

- `GET /api/assignments/unprocessed` - Get unprocessed calendar assignments
- `GET /api/assignments/upcoming?days=30` - Get upcoming assignments
- `POST /api/assignments/sync-to-supabase` - Sync assignments to Supabase
- `POST /api/assignments/:id/create-sessions` - Create study sessions for assignment

### Agent

- `GET /api/agent/status` - Get agentic AI status
- `POST /api/agent/start` - Start agentic AI service
- `POST /api/agent/stop` - Stop agentic AI service

### Email

- `POST /api/email/test` - Send test email

### MongoDB

- `POST /api/mongodb/reset` - Reset processed flags (for testing)

## Project Structure

```
smart-study-buddy-22/
├── backend/
│   ├── api.py                    # Flask API server
│   ├── agentic_service.py       # Background calendar sync (runs every 60s)
│   ├── assignment_sync.py       # Assignment detection and sync logic
│   ├── database.py              # MongoDB operations
│   ├── email_service.py         # SendGrid email notifications
│   ├── google_calendar.py       # Google Calendar API integration
│   ├── calendar_reader.py       # Read and store calendar events
│   ├── apply_migration.py       # Database migration helper
│   ├── reset_mongodb.py         # MongoDB reset utility
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Backend environment variables
├── src/
│   ├── components/
│   │   ├── exercises/          # Exercise component renderers
│   │   │   ├── ExerciseRenderer.tsx
│   │   │   ├── MultipleChoiceExercise.tsx
│   │   │   ├── ShortAnswerExercise.tsx
│   │   │   └── MiniProblemSetExercise.tsx
│   │   └── ui/                 # shadcn/ui components
│   ├── lib/
│   │   ├── services/
│   │   │   ├── exerciseService.ts    # Exercise generation logic
│   │   │   └── sessionService.ts     # Session management
│   │   └── templates/
│   │       ├── index.js              # Main template generator
│   │       ├── tier1_templates.js    # Tier 1 exercise templates
│   │       ├── tier2_templates.js    # Tier 2 exercise templates
│   │       └── tier3_templates.js    # Tier 3 exercise templates
│   ├── pages/
│   │   ├── Index.tsx                 # Dashboard
│   │   ├── AssignmentDetail.tsx      # Assignment & material upload
│   │   ├── SessionPage.tsx           # Study session interface
│   │   └── CalendarSync.tsx          # Manual calendar sync
│   └── main.tsx                      # Application entry point
├── supabase/
│   └── migrations/              # Database migration scripts
├── scripts/
│   ├── cleanup.py               # Code cleanup utility
│   ├── fix_empty_blocks.py      # Python syntax fixer
│   └── remove_emojis.py         # Emoji removal utility
├── .env                         # Frontend environment variables
├── package.json                 # Node.js dependencies
└── README.md                    # This file
```

## Troubleshooting

### "OpenAI API Error: 503 Service Unavailable"
This is an intermittent API rate limit or service availability issue. The system has retry logic and will continue with other exercises. This is expected with free or rate-limited API tiers.

### "Calendar events not being detected"
1. Verify `agentic_service.py` is running
2. Check Google Calendar credentials are valid (`token.json` exists)
3. Ensure event titles contain assignment keywords
4. Check backend logs for sync status
5. Verify `USER_EMAIL` in backend/.env matches your Supabase account email

### "Questions are too generic / not using materials"
1. Ensure study materials were uploaded before creating study plan
2. Check that `material_content` column exists in assignments table
3. Verify material content is stored (check Supabase table directly)
4. Re-upload materials if necessary

### "Database migration errors"
- Run migrations in chronological order
- Use Supabase SQL Editor for manual execution
- Check for column existence before running migrations

### "Email notifications not being sent"
1. Verify SendGrid API key is valid and active
2. Check that sender email is verified in SendGrid dashboard
3. Review backend logs for email service errors
4. Ensure SMTP credentials in backend/.env are correct

### "Study sessions showing as assignments"
Ensure your study session event titles:
- Start with "study:" or "Study:"
- Contain "study session" in the title
- Don't trigger assignment keywords before "study" prefix

### "Assignment not appearing in 'Your Assignments'"
1. Check that you're logged into the same account as USER_EMAIL
2. Verify assignment was created in Supabase (check database directly)
3. Refresh the page
4. Check browser console for errors

## Development

### Building for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Running Tests

```bash
npm run test
```

### Code Style

The project uses:
- **TypeScript** for type safety
- **ESLint** for code linting
- **Prettier** for code formatting

## Contributing

This project was built for educational purposes. Feel free to fork and adapt for your own use.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with [React](https://react.dev/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- AI powered by [OpenAI](https://openai.com/)
- Database by [Supabase](https://supabase.com/)
- Calendar integration via [Google Calendar API](https://developers.google.com/calendar)
