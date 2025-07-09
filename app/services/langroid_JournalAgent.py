# app/services/langroid_JournalAgent.py

import os
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write
from pydantic import BaseModel
from langroid.agent.tool_message import ToolMessage 

LOG_DIR = "logs/recordings"
os.makedirs(LOG_DIR, exist_ok=True)

def record_audio_fn(duration: float | None = None, samplerate: int = 44100, channels: int = 1) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = os.path.join(LOG_DIR, f"{timestamp}.wav")
    print(f"[JournalAgent] Recording → {fname}")
    rec = sd.rec(int((duration or 5) * samplerate), samplerate=samplerate, channels=channels)
    sd.wait()
    write(fname, samplerate, rec)
    print(f"[JournalAgent] Saved → {fname}")
    return fname

class RecordAudioTool(ToolMessage):
    request: str = "record_audio"
    purpose: str = "Record audio from mic; returns path to saved wav file."
    duration: float | None = None
    samplerate: int = 44100
    channels: int = 1

    @classmethod
    def examples(cls):
        return [cls(duration=5)]

    # Stateless handler: auto-registered into agent using `request` as method name
    def handle(self) -> str:
        return record_audio_fn(self.duration, self.samplerate, self.channels)
