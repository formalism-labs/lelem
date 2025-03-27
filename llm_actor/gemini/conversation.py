
# pip install google-generativeai

import time
# from google import genai
import google.generativeai as genai
from google.genai import types
from ..conversation import ConversationBase, DEFAULT_PROLOG

default_model = "gemini-2.0-flash-lite-preview-02-05"

class Conversation(ConversationBase):
    def __init__(self, ai, model=default_model, prolog=DEFAULT_PROLOG, temperature=0):
        super().__init__()
        self.ai = ai
        self.model = model
        self.prolog = str(prolog)
        self.temperature = temperature

        self.config = types.GenerateContentConfig(
            # system_instruction=self.system_message,
            max_output_tokens=4096,
            temperature=temperature)
        self.gen_model = genai.GenerativeModel(model, system_instruction=self.prolog)
        self.chat = self.gen_model.start_chat()

    def _question(self, text, role="user"):
        return {"role": role, "content": text}

    def _answer(self, text, role="assistant"):
        return {"role": role, "content": text}

    def _count_tokens(self, text):
        return self.ai.models.count_tokens(model=self.model, contents=text).total_tokens
    
    def ask(self, q):
        t0 = time.time()
        self._messages.append(self._question(q))
        input_tokens = self._count_tokens(q)
        self.messages_cost.append({'input': input_tokens, 'total': input_tokens})
        try:
            resp = self.chat.send_message(q)
        except Exception as x:
            print(f"When asking: {q}\nAn error occurred: {x}")
            raise x
        answer = resp.text
        self._messages.append(self._answer(answer))
        
        output_tokens = self._count_tokens(answer)
        self.messages_cost.append({'output': output_tokens, 'total': output_tokens})
        
        total_tokens = input_tokens + output_tokens
        self.total_tokens += total_tokens

        self.add_qa(q, answer, time.time() - t0, {'input': input_tokens, 'output': output_tokens, 'total': total_tokens})
        return answer
