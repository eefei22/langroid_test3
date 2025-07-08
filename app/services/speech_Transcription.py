# app/services/speech_Transcription.py

from faster_whisper import WhisperModel

model = WhisperModel("small", compute_type="int8", device="cpu")

def transcribe_audio(audio_path: str) -> str:
    segments, _ = model.transcribe(audio_path, beam_size=1, language="auto")
    return " ".join([seg.text for seg in segments])

