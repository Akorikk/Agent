# Agent

A real-time, agentic voice scheduling assistant that converses naturally with users, collects meeting details, confirms intent, and creates real Google Calendar events.

 
 .
 
Features

🗣 Conversational AI agent (stateful)

🧠 Multi-turn information extraction

✅ Explicit confirmation before action

📅 Real Google Calendar integration (OAuth 2.0)

🔊 Voice output (Text-to-Speech)

💬 Text-based UI (Streamlit)

🧩 Modular, production-style architecture

# High-Level Architecture
User (Text / Voice)
        ↓
Agentic LLM (OpenAI)
        ↓
Tool Invocation (create_calendar_event)
        ↓
FastAPI Backend
        ↓
Google Calendar API


# Project Structure
Voice_AI_Agent/
│
├── agent/                  # Agentic reasoning & tool orchestration
│   ├── agent.py             # Core LLM agent logic (stateful)
│   ├── tools.py             # Tool schema exposed to the LLM
│   └── __init__.py
│
├── backend/                 # Backend API (FastAPI)
│   ├── main.py              # API entrypoint + OAuth endpoints
│   ├── schemas.py           # Pydantic request/response models
│   ├── token.json           # Google OAuth token (ignored in Git)
│   ├── services/
│   │   ├── calendar_service.py  # Google Calendar integration
│   │   ├── oauth_service.py     # OAuth helpers (optional)
│   │   └── __init__.py
│   └── __init__.py
│
├── ui/                      # Frontend UI
│   └── app.py               # Streamlit text UI with voice output
│
├── voice/                   # Voice utilities
│   ├── tts.py               # Text-to-Speech (pyttsx3)
│   ├── stt.py               # Speech-to-Text (Vosk – optional)
│   ├── mic.py               # Microphone recording helper
│   ├── voice_agent.py       # Mic → Agent loop (optional)
│   └── __init__.py
│
├── vapi/
│   └── agent_prompt.txt     # System prompt design reference
│
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore
└── README.md


# Requirements
Python 3.10+ (tested on 3.10)
Dependencies (requirements.txt)

fastapi==0.110.0
uvicorn==0.29.0
pydantic==2.6.4
python-dotenv==1.0.1
google-api-python-client==2.122.0
google-auth==2.28.1
google-auth-oauthlib==1.2.0
openai==1.12.0
httpx==0.27.0
requests==2.31.0
loguru==0.7.2
sounddevice==0.4.6
scipy==1.10.1
pyttsx3
streamlit
requests
python-dotenv


# Environment Variables
OPENAI_API_KEY=your_openai_key

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:8001/auth/callback

CALENDAR_TIMEZONE=Asia/Kolkata


# Agent Design (Why this is Agentic)
Stateful memory (conversation history preserved)
Explicit intent confirmation
Tool calling via structured schema
Failure-aware responses
No hallucinated actions
This is not a chatbot — it is a decision-making AI agent.

# Calendar Integration
Uses Google Calendar API
OAuth 2.0 authentication
Events created in the user’s primary calendar
Timezone-aware scheduling

# Deployment
UI: Streamlit Cloud / Render
Backend: Render / Railway
Secrets: Environment variables

# Security Notes
.env → ignored
token.json → ignored
OAuth tokens never committed


# Folder-by-Folder Explanation
* This project is structured to separate agent reasoning, backend services, UI, and voice I/O, following production-style agentic system design.

# agent/ — Agentic Intelligence Layer (Brain)
This folder contains the LLM-powered decision-making agent.
Purpose
Handles conversation flow
Maintains state across turns
Decides when to ask questions
Decides when to call tools
Never performs side effects directly
* Files
agent.py
Core of the system
Responsibilities:
Maintains conversation memory (messages)
Sends conversation to LLM
Enforces agent rules:
Ask for missing info
Ask for year once
Ask for confirmation exactly once
Executes tool calls only after confirmation
Speaks responses using TTS
This is where agentic behavior lives.

* tools.py
Tool contract exposed to the LLM
Responsibilities:
Defines the schema for create_calendar_event
Tells the LLM:
What tool exists
When to use it
What parameters are required
This keeps tool logic decoupled from reasoning.
__init__.py
Marks agent/ as a Python package.

# backend/ — Action Execution Layer (Hands)
* This folder performs real-world actions (calendar creation).

Purpose
Exposes secure APIs
Handles OAuth
Interacts with Google Calendar
Never contains LLM logic
* Files
main.py
FastAPI entry point
Responsibilities:
/create-calendar-event → called by the agent tool
/auth/login → Google OAuth flow
/auth/callback → token exchange
Error handling and logging
This is the bridge between AI decisions and real systems.

* schemas.py
Request & response validation
Responsibilities:
Defines strict Pydantic models:
CalendarEventRequest
CalendarEventResponse
Ensures backend receives clean, typed data
This prevents malformed tool calls.

* services/
Business logic layer (pure services)
calendar_service.py
Google Calendar integration
Responsibilities:
Loads OAuth credentials (token.json)
Creates real calendar events
Handles timezone correctness
Talks directly to Google API
This is the only place where Google Calendar is touched.

* token.json
Stores OAuth access + refresh tokens
Never committed to GitHub
__init__.py
Marks services/ as a package.

# ui/ — User Interaction Layer (Face)
This is what the user sees
Purpose
Provide a simple text interface
Display chat history
Trigger agent turns
Enable voice output

* Files
app.py

Streamlit UI
Responsibilities:
Displays assistant & user messages
Always keeps text input available
Prevents duplicate messages
Calls run_agent_turn() for every user input
Speaks assistant responses
The UI is thin by design — all intelligence lives in agent/.

# voice/ — Voice I/O Layer (Ears & Mouth)
This folder handles speech input/output.

Files
tts.py
Text-to-Speech
Responsibilities:
Converts assistant responses to voice
Uses pyttsx3 (offline, free)
Re-initializes engine safely on Windows
stt.py
Speech-to-Text (Optional)
Responsibilities:
Uses Vosk for offline STT
Lazy-loads model
Safe fallback if model is missing
Voice input is optional but supported.
mic.py
Low-level microphone recording helper.
voice_agent.py
CLI loop:
Mic → STT → Agent → TTS

Used for voice-only testing (not required for deployment).

# vapi/ — Prompt Design & Reference
Purpose
Stores agent prompt design
Documents conversation rules
Useful for:
Prompt iteration
Switching to VAPI / Retell later
File
agent_prompt.txt
Defines:

Conversation flow

Confirmation rules

Tool usage rules

Failure handling


python -m uvicorn backend.main:app
python -m uvicorn backend.main:app --port 8001
python -m agent.agent
streamlit run ui/app.py