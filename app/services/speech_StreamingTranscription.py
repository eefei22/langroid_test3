#services/speech_StreamingTranscription.py

import asyncio
import numpy as np

from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
SAMPLE_WIDTH = 2
CHANNELS = 1

model = WhisperModel("small", compute_type="int8", device="cpu")

class WhisperStreamingASR:
    def __init__(self, websocket):
        self.queue = asyncio.Queue()
        self.websocket = websocket
        self.running = True
        self.buffer = bytearray()  # for live transcript
        self.recording_buffer = bytearray()  # for journal entry
        self.recording_enabled = False

    async def enqueue_audio(self, chunk: bytes):
        await self.queue.put(chunk)

    async def run(self):
        while self.running:
            try:
                chunk = await asyncio.wait_for(self.queue.get(), timeout=2.0)

                # Optional: buffer for journal
                if self.recording_enabled:
                    self.recording_buffer.extend(chunk)

                # Live transcription every 1s
                self.buffer.extend(chunk)
                MIN_SECONDS = 1.5
                min_buffer_bytes = int(SAMPLE_RATE * SAMPLE_WIDTH * MIN_SECONDS)

                if len(self.buffer) >= min_buffer_bytes:
                    try:
                        float_audio = self._bytes_to_float32(self.buffer[:SAMPLE_RATE * SAMPLE_WIDTH])
                        print("Buffer converted to float")
                        text = self.transcribe_array(float_audio)
                        print("💬 Transcribed:", text)
                        if text.strip():
                            await self.websocket.send_text(text)
                    except Exception as e:
                        print("Error during transcription:", e)
                    finally:
                        self.buffer = self.buffer[SAMPLE_RATE * SAMPLE_WIDTH:]

            except asyncio.TimeoutError:
                continue

    def start_recording(self):
        self.recording_buffer = bytearray()
        self.recording_enabled = True
        print("🟢 Journal recording started")

    def stop_recording_and_transcribe(self) -> str:
        self.recording_enabled = False
        float_audio = self._bytes_to_float32(self.recording_buffer)
        text = self.transcribe_array(float_audio)
        print("🛑 Journal recording stopped")
        return text

    def _bytes_to_float32(self, audio_bytes: bytes) -> np.ndarray:
        int_samples = np.frombuffer(audio_bytes, dtype=np.int16)
        return int_samples.astype(np.float32) / 32768.0
        normalized = float_samples * 2.0  
        return np.clip(normalized, -1.0, 1.0)

    def transcribe_array(self, audio_array: np.ndarray) -> str:
        segments, _ = model.transcribe(audio_array, beam_size=1, language="en")

        result = ""
        for seg in segments:
            print(f"[{seg.start:.2f}s -> {seg.end:.2f}s] → '{seg.text}'")  # SHOW TEXT IN QUOTES
            result += seg.text + " "

        print("💬 Final transcript:", result.strip())
        return result.strip()


    def stop(self):
        self.running = False
