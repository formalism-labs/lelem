
import os
import anthropic
from ..conversation import ConversationBase, DEFAULT_PROLOG

class Conversation(ConversationBase):
    def __init__(self, ai, model=None, prolog=DEFAULT_PROLOG, temperature=0):
        super().__init__()
        self.ai = ai
        self.model = model
        self.system_message = str(prolog)
        self.temperature = temperature

    def _question(self, text, role="user"):
        return {"role": role, "content": text}

    def _reply(self, text, role="assistant"):
        return {"role": role, "content": text}

    def ask(self, q):
        self._messages.append(self._question(q))
        try:
            resp = self.ai.messages.create(
                model=self.model,
                system=self.system_message,
                messages=self._messages,
                max_tokens=4096,
                temperature=self.temperature)
        except Exception as x:
            print(f"When asking: {q}\nAn error occurred: {x}")
            raise x
        output = resp.content[0].text
        input_tokens = resp.usage.input_tokens
        output_tokens =  resp.usage.output_tokens
        total_tokens = input_tokens + output_tokens
        self._messages.append(self._reply(output))
        self.messages_cost.append({'input': input_tokens, 'total': input_tokens})
        self.messages_cost.append({'output': output_tokens, 'total': output_tokens})
        self.total_tokens += total_tokens
        return output
