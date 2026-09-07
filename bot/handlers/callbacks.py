from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from bot.services.answer_service import AnswerRepository
from bot.services.session_manager import SessionManager

def register_callback_handlers(
    app: Client,
    answer_repo: AnswerRepository,
    session_manager: SessionManager
):
    @app.on_callback_query()
    async def handle_buttons(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        session = session_manager.get(user_id)
        if not session:
            await callback_query.answer("جلسه نامعتبر است.")
            return

        if callback_query.data == "confirm_final":
            await answer_repo.send(user_id, session.answers)
            await callback_query.edit_message_text("✅ پاسخ‌های شما با موفقیت ثبت شد. متشکریم!")
            session_manager.delete(user_id)

        elif callback_query.data == "edit_answer":
            session.state = "edit_number"
            session_manager.update(user_id, session)
            await callback_query.edit_message_text(
                "شماره سوالی که می‌خواهید تغییر دهید را بفرستید (مثلاً 1):"
            )
