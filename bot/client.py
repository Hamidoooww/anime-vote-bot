from pyrogram import Client
from bot.config import Config

def create_client() -> Client:
    return Client(
        "telegram_survey_bot",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
    )
