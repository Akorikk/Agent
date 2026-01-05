# agent/agent.py

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

from agent.tools import create_calendar_event_tool
from voice.tts import speak

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BACKEND_URL = "http://127.0.0.1:8001/create-calendar-event"

SYSTEM_PROMPT = """
You are a scheduling assistant.

Rules:
1. Extract the user's name, meeting date, time, and title.
2. If ANY detail is missing, ask only for the missing detail.
3. If the date does not include a year, ask ONCE for the year.
4. Remember all previously provided information.
5. Ask exactly ONE confirmation question when all details are known.
6. Only after user confirms (yes / confirm / ok), call create_calendar_event.
7. Do NOT restart the conversation.
8. Do NOT ask further questions after confirmation.
"""

# -------------------------------------------------------------------
# Persistent conversation memory (AGENT-ONLY)
# -------------------------------------------------------------------

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def normalize_date(date_str: str) -> str:
    """
    Ensure YYYY-MM-DD format.
    """
    if "-" in date_str and len(date_str.split("-")) == 2:
        return f"{datetime.now().year}-{date_str}"
    return date_str


def normalize_time(time_str: str) -> str:
    """
    Ensure HH:MM 24-hour format.
    The model already converts AM/PM correctly.
    """
    return time_str.strip()


def call_create_calendar_event(arguments: dict):
    response = requests.post(BACKEND_URL, json=arguments)
    response.raise_for_status()
    return response.json()

# -------------------------------------------------------------------
# Core Agent Turn (USED BY UI & VOICE)
# -------------------------------------------------------------------

def run_agent_turn(user_input: str) -> str | None:
    """
    Runs one agent step.
    Returns assistant text (or None).
    DOES NOT touch Streamlit state.
    """

    global messages
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=[create_calendar_event_tool],
        tool_choice="auto",
    )

    message = response.choices[0].message

    # ---------------- TOOL CALL ----------------
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)

        if "date" in arguments:
            arguments["date"] = normalize_date(arguments["date"])

        if "time" in arguments:
            arguments["time"] = normalize_time(arguments["time"])

        print("\n🛠 Tool call detected:")
        print(arguments)

        try:
            call_create_calendar_event(arguments)

            confirmation_text = (
                f"✅ Your meeting has been successfully scheduled.\n\n"
                f"📅 Date: {arguments['date']}\n"
                f"⏰ Time: {arguments['time']}\n"
                f"📝 Title: {arguments.get('title', 'Meeting')}\n\n"
                "I’ve added it to your Google Calendar. "
                "Is there anything else I can help you with?"
            )

            speak(confirmation_text)
            return confirmation_text

        except requests.HTTPError:
            error_text = (
                "❌ Sorry, I couldn't create the calendar event. "
                "Please make sure Google Calendar is connected."
            )

            speak(error_text)
            return error_text

    # ---------------- NORMAL RESPONSE ----------------
    if message.content:
        speak(message.content)
        return message.content

    return None

# -------------------------------------------------------------------
# Text Mode Runner (CLI testing only)
# -------------------------------------------------------------------

def run_agent():
    welcome_text = (
        "Hi! I’m here to help you schedule a meeting. "
        "Just tell me the meeting details whenever you’re ready."
    )

    print("\n🤖 Assistant:")
    print(welcome_text)
    speak(welcome_text)

    print("\n🎙 Voice Scheduling Agent (stateful)")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        reply = run_agent_turn(user_input)
        if reply:
            print("\n🤖 Assistant:")
            print(reply)

# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    run_agent()