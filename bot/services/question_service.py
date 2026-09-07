from typing import Protocol, List
from pyrogram import Client
from pyrogram.types import Message

class QuestionRepository(Protocol):
    async def get_all(self) -> List[Message]:
        ...

    async def add(self, text: str) -> Message:
        ...

    async def remove_by_number(self, number: int) -> bool:
        ...

class TelegramQuestionRepository:
    def __init__(self, client: Client, channel_id: int):
        self._client = client
        self._channel_id = channel_id

    async def get_all(self) -> List[Message]:
        messages = []
        async for msg in self._client.get_chat_history(self._channel_id, limit=100):
            if msg.text:
                messages.append(msg)
        messages.reverse()
        return messages

    async def add(self, text: str) -> Message:
        return await self._client.send_message(self._channel_id, text)

    async def remove_by_number(self, number: int) -> bool:
        questions = await self.get_all()
        if 1 <= number <= len(questions):
            msg = questions[number - 1]
            await self._client.delete_messages(self._channel_id, msg.id)
            return True
        return False