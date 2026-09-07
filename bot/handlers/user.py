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
        if not message.from_user:
            return

        user_id = message.from_user.id

        if user_id == Config.ADMIN_ID:
            await message.reply_text(
                "🔐 <b>پنل ادمین</b>\n\n"
                "دستورات:\n"
                "/add_question &lt;متن سوال&gt;\n"
                "/remove_question &lt;شماره&gt;\n"
                "/list_questions",
                parse_mode="html",
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
        session.edit_index = None

        await message.reply_text(
            f"سلام! لطفاً به {len(questions)} سوال پاسخ دهید.\n\n"
            f"سوال ۱:\n{questions[0].text or ''}"
        )

    # IMPORTANT: filters.command() requires command names.
    # This is a general text handler, so commands are ignored explicitly below.
    @app.on_message(filters.text & filters.private)
    async def handle_text(client: Client, message: Message):
        if not message.from_user or not message.text:
            return

        user_id = message.from_user.id

        # Commands belong to command handlers.
        if message.text.startswith("/"):
            return

        if user_id == Config.ADMIN_ID:
            return

        session = session_manager.get(user_id)
        if not session:
            return

        text = message.text.strip()
        if not text:
            await message.reply_text("لطفاً یک پاسخ وارد کنید.")
            return

        questions = await question_repo.get_all()
        total = len(questions)

        # Questions may have been removed while a user was answering.
        if total == 0 or session.current_index >= total:
            session_manager.delete(user_id)
            await message.reply_text(
                "سوالات تغییر کرده‌اند و جلسه قبلی دیگر معتبر نیست. لطفاً /start را بزنید."
            )
            return

        if session.state == "answering":
            session.answers.append(text)
            session.current_index += 1

            if session.current_index < total:
                next_q = questions[session.current_index].text or ""
                await message.reply_text(
                    f"سوال {session.current_index + 1}:\n{next_q}"
                )
            else:
                preview = build_preview(session.answers)
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ تأیید نهایی", callback_data="confirm_final")],
                    [InlineKeyboardButton("✏️ ویرایش پاسخ", callback_data="edit_answer")]
                ])
                session.state = "awaiting_final"
                session_manager.update(user_id, session)
                await message.reply_text(
                    preview, reply_markup=keyboard, parse_mode="html"
                )

        elif session.state in ("awaiting_final", "edit_number"):
            try:
                q_num = int(text) - 1
            except ValueError:
                await message.reply_text("لطفاً شماره سوال را به صورت عدد بفرستید.")
                return

            if 0 <= q_num < len(session.answers):
                session.edit_index = q_num
                session.state = "edit_answer"
                session_manager.update(user_id, session)
                await message.reply_text(
                    f"پاسخ جدید برای سوال {q_num + 1} را بفرستید:"
                )
            else:
                await message.reply_text("شماره سوال نامعتبر است.")

        elif session.state == "edit_answer":
            edit_idx = session.edit_index

            if edit_idx is None or not (0 <= edit_idx < len(session.answers)):
                session_manager.delete(user_id)
                await message.reply_text(
                    "جلسه ویرایش نامعتبر شد. لطفاً /start را بزنید."
                )
                return

            session.answers[edit_idx] = text
            session.edit_index = None
            session.state = "awaiting_final"

            preview = build_preview(session.answers)
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ تأیید نهایی", callback_data="confirm_final")],
                [InlineKeyboardButton("✏️ ویرایش پاسخ", callback_data="edit_answer")]
            ])
            session_manager.update(user_id, session)

            await message.reply_text(
                preview, reply_markup=keyboard, parse_mode="html"
            )
