import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
    QUESTIONS_CHANNEL_ID = int(os.getenv("QUESTIONS_CHANNEL_ID", "0"))
    ANSWERS_CHANNEL_ID = int(os.getenv("ANSWERS_CHANNEL_ID", "0"))
