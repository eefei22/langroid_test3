import sounddevice as sd
import numpy as np
import soundfile as sf
import os
from dotenv import load_dotenv
from faster_whisper import WhisperModel

from langroid.language_models import OpenAIGPTConfig
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig

from app.services import journal_Manager

# Load .env
load_dotenv()

# === Setup Langroid ===
llm_cfg = OpenAIGPTConfig(
    chat_model="deepseek/deepseek-chat",
    api_base="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

agent_cfg = ChatAgentConfig(
    name="WellBot",
    llm=llm_cfg,
    system_message=(
        "You are Well-Bot, a journaling assistant. "
        "When the user says something like 'start a journal' or 'stop it', "
        "respond supportively and invoke the correct tool."
    ),
)

class JournalAgent(ChatAgent):
    def __init__(self, config):
        super().__init__(config)

    def chat_response(self, message: str) -> str:
        msg_lower = message.lower()

        if "journal" in msg_lower:
            result = journal_Manager.start_journal(websocket=None)
            return result.get("status", "Started.")

        elif "stop journal" in msg_lower:
            result = journal_Manager.stop_journal(websocket=None)
            return result.get("text", "Stopped.")

        return self.llm_response(message)

agent = JournalAgent(agent_cfg)

# === Record from mic ===
DURATION = 6
SAMPLE_RATE = 16000
CHANNELS = 1
print("🎙️ Recording... Speak now!")
audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32')
sd.wait()
print("✅ Recording complete.")

sf.write("temp_output.wav", audio, SAMPLE_RATE)

# === Transcribe ===
model = WhisperModel("small", compute_type="int8", device="cpu")
audio_np = audio[:, 0]
segments, _ = model.transcribe(audio_np, language="en")

transcript = " ".join([seg.text for seg in segments])
print("📝 Transcript:", transcript)

# === Run through Langroid ===
response = agent.chat_response(transcript)
print("🤖 Well-Bot:", response)
