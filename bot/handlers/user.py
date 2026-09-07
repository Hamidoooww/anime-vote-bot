from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import Config
from bot.services.question_service import QuestionRepository
from bot.services.session_manager import SessionManager
from bot.utils.telegram import build_preview

def register_user_handlers(
    app: Client,
    question_repo: QuestionRepository,
    session_manager: SessionManager
):
    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id == Config.ADMIN_ID:
            await message.reply_text(
                "🔐 **پنل ادمین**\n\n"
                "دستورات:\n"
                "/add_question <متن سوال>\n"
                "/remove_question <شماره>\n"
                "/list_questions"
            )
            return

        questions = await question_repo.get_all()
        if not questions:
            await message.reply_text("فعلاً سوالی ثبت نشده است.")
            return

        session = session_manager.create(user_id)
        session.current_index = 0
        session.answers = []
        session.state = "answering"
        session_manager.update(user_id, session)

        await message.reply_text(
            f"سلام! لطفاً به {len(questions)} سوال پاسخ دهید.\n\n"
            f"سوال ۱:\n{questions[0].text}"
        )

    @app.on_message(filters.text & filters.private & ~filters.command)
    async def handle_text(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id == Config.ADMIN_ID:
            return

        session = session_manager.get(user_id)
        if not session:
            return

        text = message.text.strip()
        questions = await question_repo.get_all()
        total = len(questions)

        if session.state == "answering":
            session.answers.append(text)
            session.current_index += 1

            if session.current_index < total:
                next_q = questions[session.current_index].text
                await message.reply_text(
                    f"سوال {session.current_index + 1}:\n{next_q}"
                )
            else:
                preview = build_preview(session.answers)
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ تأیید نهایی", callback_data="confirm_final")],
                    [InlineKeyboardButton("✏️ ویرایش پاسخ", callback_data="edit_answer")]
                ])
                await message.reply_text(preview, reply_markup=keyboard)
                session.state = "awaiting_final"
                session_manager.update(user_id, session)

        elif session.state == "awaiting_final":
            # کاربر بعد از دیدن پیش‌نمایش مستقیماً شماره سوال را فرستاده
            try:
                q_num = int(text) - 1
                if 0 <= q_num < total:
                    session.edit_index = q_num
                    session.state = "edit_answer"
                    await message.reply_text(f"پاسخ جدید برای سوال {q_num + 1} را بفرستید:")
                    session_manager.update(user_id, session)
                else:
                    await message.reply_text("شماره نامعتبر است.")
            except ValueError:
                await message.reply_text("برای ویرایش، شماره سوال را بفرستید یا از دکمه استفاده کنید.")

        elif session.state == "edit_number":
            try:
                q_num = int(text) - 1
                if 0 <= q_num < total:
                    session.edit_index = q_num
                    session.state = "edit_answer"
                    await message.reply_text(f"پاسخ جدید برای سوال {q_num + 1} را بفرستید:")
                    session_manager.update(user_id, session)
                else:
                    await message.reply_text("شماره نامعتبر است.")
            except ValueError:
                await message.reply_text("لطفاً یک عدد بفرستید.")

        elif session.state == "edit_answer":
            edit_idx = session.edit_index
            session.answers[edit_idx] = text
            session.state = "answering"
            preview = build_preview(session.answers)
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ تأیید نهایی", callback_data="confirm_final")],
                [InlineKeyboardButton("✏️ ویرایش پاسخ", callback_data="edit_answer")]
            ])
            await message.reply_text(preview, reply_markup=keyboard)
            session.state = "awaiting_final"
            session_manager.update(user_id, session)