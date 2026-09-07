import logging
from pyrogram import idle
from bot.client import create_client
from bot.config import Config
from bot.services.question_service import TelegramQuestionRepository
from bot.services.answer_service import TelegramAnswerRepository
from bot.services.session_manager import SessionManager
from bot.handlers.admin import register_admin_handlers
from bot.handlers.user import register_user_handlers
from bot.handlers.callbacks import register_callback_handlers

logging.basicConfig(level=logging.INFO)

def main():
    app = create_client()
    app.start()

    question_repo = TelegramQuestionRepository(app, Config.QUESTIONS_CHANNEL_ID)
    answer_repo = TelegramAnswerRepository(app, Config.ANSWERS_CHANNEL_ID)
    session_manager = SessionManager()

    register_admin_handlers(app, question_repo)
    register_user_handlers(app, question_repo, session_manager)
    register_callback_handlers(app, answer_repo, session_manager)

    logging.info("Bot is running...")
    idle()
    app.stop()

if __name__ == "__main__":
    main()