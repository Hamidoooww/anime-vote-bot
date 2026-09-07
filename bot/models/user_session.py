from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class UserSession:
    current_index: int = 0
    answers: List[str] = field(default_factory=list)
    state: str = "answering"  # answering | edit_number | edit_answer | awaiting_final
    edit_index: Optional[int] = None
