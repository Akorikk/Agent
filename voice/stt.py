# voice/stt.py

import os

try:
    from vosk import Model, KaldiRecognizer
    import sounddevice as sd
    import queue
    import json

    MODEL_PATH = "models/vosk-model-small-en-us-0.15"

    model = None  # ⬅️ lazy-loaded

except Exception:
    model = None


def speech_to_text():
    global model

    if model is None:
        if not os.path.exists(MODEL_PATH):
            print("⚠️ Vosk model not found. Voice input disabled.")
            return None

        model = Model(MODEL_PATH)

    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        rec = KaldiRecognizer(model, 16000)
        print("🎤 Listening... Speak now")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text")