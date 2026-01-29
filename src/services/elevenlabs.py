# src/services/elevenlabs.py
from core.exceptions import TransientError

def synthesize_voice():
    # Simulated failure
    raise TransientError("ElevenLabs", "503 Service Unavailable")
