# voice/voice_agent.py

from voice.stt import speech_to_text
from agent.agent import run_agent_turn  # we’ll add this small helper


print("🎙 Voice Scheduling Agent (mic mode)")
print("Speak to schedule a meeting. Say 'exit' to stop.")

while True:
    user_text = speech_to_text()

    if not user_text:
        continue

    if user_text.lower() in {"exit", "quit"}:
        break

    run_agent_turn(user_text)