from html import escape
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.config import Config
from bot.services.question_service import QuestionRepository


def register_admin_handlers(app: Client, question_repo: QuestionRepository):
    @app.on_message(filters.command("add_question") & filters.private)
    async def add_question(client: Client, message: Message):
        if not message.from_user or message.from_user.id != Config.ADMIN_ID:
            return

        text = " ".join(message.command[1:]).strip()
        if not text:
            await message.reply_text("لطفاً متن سوال را بنویسید.")
            return

        await question_repo.add(text)
        await message.reply_text("✅ سوال اضافه شد.")

    @app.on_message(filters.command("remove_question") & filters.private)
    async def remove_question(client: Client, message: Message):
        if not message.from_user or message.from_user.id != Config.ADMIN_ID:
            return

        try:
            num = int(message.command[1])
        except (IndexError, ValueError):
            await message.reply_text("استفاده: /remove_question <شماره>")
            return

        success = await question_repo.remove_by_number(num)
        if success:
            await message.reply_text(f"✅ سوال {num} حذف شد.")
        else:
            await message.reply_text("شماره نامعتبر است.")

    @app.on_message(filters.command("list_questions") & filters.private)
    async def list_questions(client: Client, message: Message):
        if not message.from_user or message.from_user.id != Config.ADMIN_ID:
            return

        questions = await question_repo.get_all()
        if not questions:
            await message.reply_text("هیچ سوالی ثبت نشده است.")
            return

        lines = [
            f"{i}. {escape(q.text or '')}"
            for i, q in enumerate(questions, start=1)
        ]
        await message.reply_text(
            "<b>📝 سوالات فعلی:</b>\n\n" + "\n".join(lines),
            parse_mode="html",
        )
