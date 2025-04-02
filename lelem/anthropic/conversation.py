
# pip install anthropic

from ..common import *
from ..conversation import ConversationBase, DEFAULT_PROLOG
from ..questions import Question
from ..prolog import Prolog

import anthropic

DEFAULT_MODEL = "claude-3-5-haiku-20241022"

class Conversation(ConversationBase):
    def __init__(self, ai, model: str = DEFAULT_MODEL, prolog: Optional[Prolog] = None, temperature: float = 0):
        super().__init__()
        self.ai = ai
        self.model = model
        self.prolog = DEFAULT_PROLOG if prolog is None else str(prolog)
        self.temperature = temperature

    def _question(self, text: str, role: str = "user"):
        return {"role": role, "content": text}

    def _answer(self, text: str, role: str = "assistant"):
        return {"role": role, "content": text}

    def ask(self, q: Question):
        t0 = time.time()
        self._messages.append(self._question(q.text))
        try:
            resp = self.ai.messages.create(
                model=self.model,
                system=self.prolog,
                messages=self._messages,
                max_tokens=4096,
                temperature=self.temperature)
        except Exception as x:
            raise Exception(f"When asking: '{q.text}', an error occurred: {x}") from x
        answer = resp.content[0].text
        self._messages.append(self._answer(answer))

        input_tokens = resp.usage.input_tokens
        output_tokens =  resp.usage.output_tokens
        total_tokens = input_tokens + output_tokens
        self.messages_cost.append({'input': input_tokens, 'total': input_tokens})
        self.messages_cost.append({'output': output_tokens, 'total': output_tokens})
        self.total_tokens += total_tokens

        cost = {'input': input_tokens, 'output': output_tokens, 'total': total_tokens}
        self.add_qa(q, answer, time.time() - t0, cost)
        return answer
