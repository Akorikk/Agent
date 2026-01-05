# voice/tts.py

import pyttsx3


def speak(text: str):
    try:
        print("🔊 Speaking...")

        # 🔁 Re-initialize engine EVERY time (critical on Windows)
        engine = pyttsx3.init()
        engine.setProperty("rate", 155)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print(f"⚠️ TTS failed: {e}")