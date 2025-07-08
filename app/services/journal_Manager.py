from datetime import datetime
from app.models.journal import JournalEntry
from app.crud import journal as journal_crud
from app.api.journal_ws import active_asr  # maps websocket: WhisperStreamingASR
import uuid
import os
import asyncio

# You could wire this up with a real user/session ID later
DUMMY_USER_ID = "user-001"

def start_journal(websocket):
    transcriber = active_asr.get(websocket)
    if transcriber:
        transcriber.start_recording()
        return {"status": "recording_started"}
    return {"error": "No active transcriber found"}

def stop_journal(websocket, topic=None, tags=None):
    transcriber = active_asr.get(websocket)
    if not transcriber:
        return {"error": "No active transcriber found"}

    text = transcriber.stop_recording_and_transcribe()
    entry = JournalEntry(
        user_id=DUMMY_USER_ID,
        text=text,
        topic=topic,
        tags=tags or [],
        timestamp=datetime.utcnow(),
    )

    asyncio.create_task(journal_crud.save_entry(entry))
    return {"status": "recording_stopped", "text": text}

def attach_image(webcam_service) -> str:
    """
    Stub for image capture - implement this later with OpenCV or PiCam.
    """
    image_id = str(uuid.uuid4())[:8]
    image_path = f"data/images/journal_{image_id}.jpg"
    # Simulate camera capture
    os.makedirs("data/images", exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(b"FAKE_IMAGE_DATA")  # placeholder
    return image_path
