# audio_utils.py

import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
import whisper
import os

# Tell whisper where ffmpeg is
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"


# Load OpenAI Whisper model
model = whisper.load_model("base")

def record_audio(duration=30, fs=44100):
    try:
        print("🎤 Recording...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        print("✅ Recording complete.")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            wav.write(tmpfile.name, fs, audio)
            return tmpfile.name  # This is the full path
    except Exception as e:
        print(f"Recording failed: {e}")
        return None


def transcribe_audio(file_path):
    try:
        print(f"📂 Transcribing file: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError("Audio file not found")
        
        result = model.transcribe(file_path)
        print("🔍 Transcription Result:", result)
        return result["text"].strip()
    except Exception as e:
        print(f"Transcription failed: {e}")
        return ""
