import os
from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


class Config:
    API_ID = int(_required("API_ID"))
    API_HASH = _required("API_HASH")
    BOT_TOKEN = _required("BOT_TOKEN")
    ADMIN_ID = int(_required("ADMIN_ID"))
    QUESTIONS_CHANNEL_ID = int(_required("QUESTIONS_CHANNEL_ID"))
    ANSWERS_CHANNEL_ID = int(_required("ANSWERS_CHANNEL_ID"))
