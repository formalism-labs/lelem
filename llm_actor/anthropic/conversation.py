
import os
import time
import anthropic
from ..conversation import ConversationBase, DEFAULT_PROLOG

default_model = "claude-3-5-haiku-20241022"

class Conversation(ConversationBase):
    def __init__(self, ai, model=default_model, prolog=None, temperature=0):
        super().__init__()
        self.ai = ai
        self.model = model
        if prolog is None:
            prolog = DEFAULT_PROLOG
        self.system_message = str(prolog)
        self.temperature = temperature

    def _question(self, text, role="user"):
        return {"role": role, "content": text}

    def _answer(self, text, role="assistant"):
        return {"role": role, "content": text}

    def ask(self, q):
        t0 = time.time()
        self._messages.append(self._question(q))
        try:
            resp = self.ai.messages.create(
                model=self.model,
                system=self.system_message,
                messages=self._messages,
                max_tokens=4096,
                temperature=self.temperature)
        except Exception as x:
            raise Exception(f"When asking: '{q}', an error occurred: {x}") from x
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
