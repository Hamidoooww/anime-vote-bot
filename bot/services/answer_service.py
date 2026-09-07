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
        text = f"👤 **User ID:** `{user_id}`\n\n"
        for i, ans in enumerate(answers, start=1):
            text += f"سوال {i}: {ans}\n"
        return await self._client.send_message(self._channel_id, text)
