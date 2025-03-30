
import os
import time
import openai
from ...conversation import ConversationBase, DEFAULT_PROLOG

default_model = "gpt-4o-mini"

class Conversation(ConversationBase):
    def __init__(self, ai, model=default_model, prolog=None, temperature=0):
        super().__init__()
        self.ai = ai
        self.model = model
        if prolog is None:
            prolog = DEFAULT_PROLOG
        self.prolog = str(prolog)
        self._messages = [self._question(self.prolog, role="system")]
        self.temperature = temperature

    def _question(self, text, role="user"):
        return {"role": role, "content": text}

    def _answer(self, text, role="assistant"):
        return {"role": role, "content": text}

    def ask(self, q):
        t0 = time.time()
        self._messages.append(self._question(q))
        try:
            resp = self.ai.chat.completions.create(
                model=self.model,
                messages=self._messages,
                max_tokens=4096,
                temperature=self.temperature)
        except Exception as x:
            raise Exception(f"When asking: '{q}' an error occurred: {x}") from x

        answer = resp.choices[0].message.content
        self._messages.append(self._answer(answer))

        input_tokens = resp.usage.prompt_tokens
        cached_input_tokens = resp.usage.model_extra['prompt_cache_hit_tokens']
        output_tokens = resp.usage.completion_tokens
        total_tokens = resp.usage.total_tokens

        self.messages_cost.append({'input': input_tokens, 'input_cached': cached_input_tokens, 'total': input_tokens})
        self.messages_cost.append({'output': output_tokens, 'total': output_tokens})
        self.total_tokens += total_tokens
        
        cost = {'input': input_tokens, 'output': output_tokens, 'total': total_tokens}
        self.add_qa(q, answer, time.time() - t0, cost)
        return answer
