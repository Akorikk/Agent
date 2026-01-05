# ui/app.py

# -------------------------------------------------
# Add project root to Python path (MUST BE FIRST)
# -------------------------------------------------
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# Imports
# -------------------------------------------------
import streamlit as st
from agent.agent import run_agent_turn

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Voice Scheduling Agent",
    page_icon="🎙",
    layout="centered"
)

st.title("🎙 Voice Scheduling Agent")
st.caption("Schedule meetings using text (voice output enabled)")

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""

# -------------------------------------------------
# Welcome message (shown ONCE)
# -------------------------------------------------
if not st.session_state.chat:
    welcome_text = (
        "Hi! I’m here to help you schedule a meeting. "
        "Just tell me the meeting details whenever you’re ready."
    )
    st.session_state.chat.append(("assistant", welcome_text))

# -------------------------------------------------
# Chat display
# -------------------------------------------------
for role, msg in st.session_state.chat:
    if role == "assistant":
        st.markdown(f"**🤖 Assistant:** {msg}")
    else:
        st.markdown(f"**🧑 You:** {msg}")

st.divider()

# -------------------------------------------------
# Send message handler
# -------------------------------------------------
def send_message():
    user_text = st.session_state.pending_input.strip()
    if not user_text:
        return

    # Add user message
    st.session_state.chat.append(("user", user_text))

    # Run agent (agent handles memory + voice)
    assistant_reply = run_agent_turn(user_text)

    # Add assistant reply if present
    if assistant_reply:
        st.session_state.chat.append(("assistant", assistant_reply))

    # Clear input safely
    st.session_state.pending_input = ""

# -------------------------------------------------
# Text input (ALWAYS AVAILABLE)
# -------------------------------------------------
st.text_input(
    "Type your message",
    key="pending_input",
    placeholder="e.g. Schedule a meeting on Jan 7 at 11:30 AM",
)

st.button("Send", on_click=send_message)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("Built with FastAPI • Agentic LLMs • Google Calendar • Streamlit")