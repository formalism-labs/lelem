
from typing import Optional

from ..openai.completions import Conversation as OpenAIConversation
from ..prolog import Prolog

DEFAULT_MODEL = "deepseek-chat"

class Conversation(OpenAIConversation):
    def __init__(self, ai, model: str=DEFAULT_MODEL, prolog: Optional[Prolog] = None, temperature: float = 0):
        super().__init__(ai, model=model, prolog=prolog, temperature=temperature)
