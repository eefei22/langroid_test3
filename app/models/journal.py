#/models/journal.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Langroid tool schema: StartJournal
class StartJournal(BaseModel):
    request: str = "start_journal"
    topic: Optional[str] = Field(None, description="Optional journal topic")
    tags: Optional[list[str]] = Field(default_factory=list)

# Langroid tool schema: StopJournal
class StopJournal(BaseModel):
    request: str = "stop_journal"

# Langroid tool schema: AttachImage
class AttachImage(BaseModel):
    request: str = "attach_image"

# MongoDB journal document schema
class JournalEntry(BaseModel):
    user_id: str
    text: str
    topic: Optional[str]
    tags: list[str] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    image_path: Optional[str] = None
