# Agent

A real-time, agentic voice scheduling assistant that converses naturally with users, collects meeting details, confirms intent, and creates real Google Calendar events.


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



































































python -m uvicorn backend.main:app
python -m uvicorn backend.main:app --port 8001
python -m agent.agent
My name is Smit. Schedule a meeting on Jan 14 at 11 AM about AI final test
streamlit run ui/app.py