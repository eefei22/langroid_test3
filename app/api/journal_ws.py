#/api/journal_ws.py

import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.speech_StreamingTranscription import WhisperStreamingASR

router = APIRouter()

# Store active ASR object globally if needed by tool handlers later
active_asr = {}

@router.websocket("/ws/journal")
async def journal_ws(websocket: WebSocket):
    print("WebSocket route hit")
    await websocket.accept()
    print("WebSocket connected")

    transcriber = WhisperStreamingASR(websocket)
    active_asr[websocket] = transcriber

    asr_task = asyncio.create_task(transcriber.run())

    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            print(f"Received audio chunk: {len(audio_chunk)} bytes")
            await transcriber.enqueue_audio(audio_chunk)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        transcriber.stop()
        await asr_task
        active_asr.pop(websocket, None)
