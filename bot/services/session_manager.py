from typing import Dict, Optional
from bot.models.user_session import UserSession

class SessionManager:
    def __init__(self):
        self._sessions: Dict[int, UserSession] = {}

    def get(self, user_id: int) -> Optional[UserSession]:
        return self._sessions.get(user_id)

    def create(self, user_id: int) -> UserSession:
        session = UserSession()
        self._sessions[user_id] = session
        return session

    def update(self, user_id: int, session: UserSession) -> None:
        self._sessions[user_id] = session

    def delete(self, user_id: int) -> None:
        self._sessions.pop(user_id, None)