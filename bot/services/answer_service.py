from html import escape
from typing import Protocol, List
from pyrogram import Client
from pyrogram.types import Message


class AnswerRepository(Protocol):
    async def send(self, user_id: int, answers: List[str]) -> Message:
        ...


class TelegramAnswerRepository:
    def __init__(self, client: Client, channel_id: int):
        self._client = client
        self._channel_id = channel_id

    async def send(self, user_id: int, answers: List[str]) -> Message:
        lines = [f"👤 <b>User ID:</b> <code>{user_id}</code>", ""]
        for i, ans in enumerate(answers, start=1):
            lines.append(f"<b>سوال {i}:</b> {escape(ans)}")

        text = "\n".join(lines)

        # Telegram message size is limited, so split oversized submissions.
        chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)] or [""]
        first = await self._client.send_message(
            self._channel_id, chunks[0], parse_mode="html"
        )

        for chunk in chunks[1:]:
            await self._client.send_message(
                self._channel_id, chunk, parse_mode="html"
            )

        return first
