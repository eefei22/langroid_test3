from fastapi import FastAPI
from app.api import journal_ws
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(journal_ws.router)
