from typing import List
from pyrogram.types import Message

def build_preview(answers: List[str]) -> str:
    lines = [f"{i}. {ans}" for i, ans in enumerate(answers, start=1)]
    preview = "📋 **پیش‌نمایش پاسخ‌های شما:**\n\n" + "\n".join(lines)
    preview += "\n\nبرای تغییر پاسخ یک سوال، شماره آن را بفرستید یا دکمه تأیید نهایی را بزنید."
    return preview

