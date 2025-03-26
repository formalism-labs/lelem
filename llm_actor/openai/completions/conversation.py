
import os
import openai
from ...conversation import ConversationBase

class Conversation(ConversationBase):
    def __init__(self, ai, model=None, prolog=None, temperature=0):
        super().__init__()
        self.ai = ai
        self.model = model
        if prolog is None:
            prolog = "You are a knowledgeable and articulate AI assistant."
        self._messages = [self._question(prolog, role="system")]
        self.system_message = prolog
        self.temperature = temperature

    def _question(self, text, role="user"):
        return {"role": role, "content": text}

    def _reply(self, text, role="assistant"):
        return {"role": role, "content": text}

    def ask(self, q):
        self._messages.append(self._question(q))
        try:
            resp = self.ai.chat.completions.create(
                model=self.model,
                messages=self._messages,
                max_tokens=4096,
                temperature=self.temperature)
        except Exception as x:
            print(f"When asking: {q}\nAn error occurred: {x}")
            raise x
        output = resp.choices[0].message.content
        input_tokens = 0 # resp.usage.input_tokens
        output_tokens =  0 # resp.usage.output_tokens
        total_tokens = 0 # input_tokens + output_tokens
        self._messages.append(self._reply(output))
        self.messages_cost.append({'input': input_tokens, 'total': input_tokens})
        self.messages_cost.append({'output': output_tokens, 'total': output_tokens})
        self.total_tokens += total_tokens
        return output
