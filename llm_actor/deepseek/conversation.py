
from ..openai.completions import Conversation as OpenAIConversation

default_model = "deepseek-chat"

class Conversation(OpenAIConversation):
    def __init__(self, ai, model=default_model, prolog=None, temperature=0):
        super().__init__(ai, model=model, prolog=prolog, temperature=temperature)

