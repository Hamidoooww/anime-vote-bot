from html import escape
from typing import List


def build_preview(answers: List[str]) -> str:
    lines = [f"{i}. {escape(ans)}" for i, ans in enumerate(answers, start=1)]
    preview = "📋 <b>پیش‌نمایش پاسخ‌های شما:</b>\n\n" + "\n".join(lines)
    preview += (
        "\n\nبرای تغییر پاسخ یک سوال، شماره آن را بفرستید "
        "یا دکمه تأیید نهایی را بزنید."
    )
    return preview
