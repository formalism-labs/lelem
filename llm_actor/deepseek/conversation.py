
from ..openai.completions import Conversation as OpenAIConversation
from ..conversation import DEFAULT_PROLOG

default_model = "deepseek-chat"

class Conversation(OpenAIConversation):
    def __init__(self, ai, model=default_model, prolog=DEFAULT_PROLOG, temperature=0):
        super().__init__(ai, model=model, prolog=prolog, temperature=temperature)

