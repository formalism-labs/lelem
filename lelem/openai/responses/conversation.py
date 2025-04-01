
from ...common import *
from ...conversation import ConversationBase, DEFAULT_PROLOG
from ...questions import Question
from ...prolog import Prolog

from openai import OpenAI

default_model = "gpt-4o-mini"

class Conversation(ConversationBase):
    def __init__(self, ai, model: str = default_model, prolog: Optional[Prolog] = None, temperature: float = 0):
        super().__init__()
        self.ai = ai
        self.model = model
        self.resp = None
        self.prolog = DEFAULT_PROLOG if prolog is None else str(prolog)
        self.temperature = temperature

    def _question(self, text: str, role: str = "user"):
        return {"role": role, "content": text}

    def _answer(self, text: str, role: str = "assistant"):
        return {"role": role, "content": text}

    def ask(self, q: Question):
        t0 = time.time()
        input = [self._question(q.text)]
        if self.resp is None:
            instructions = self.prolog
            self.resp = self.ai.responses.create(model=self.model, temperature=self.temperature, instructions=instructions, input=input)
        else:
            self.resp = self.ai.responses.create(model=self.model, temperature=self.temperature, previous_response_id=self.resp.id, input=input)
        if self.resp is None:
            raise Exception("Empty response")
        answer = self.resp.output_text
        cost = self._add_qa(q.text, answer, self.resp)
        self.add_qa(q, answer, time.time() - t0, cost)
        return answer

    def _add_qa(self, q: str, a: str, resp):
        self._messages.append(self._question(q))
        input_tokens = resp.usage.input_tokens
        cached_input_tokens = resp.usage.input_tokens_details.cached_tokens
        self.messages_cost.append({'input': input_tokens, 'input_cached': cached_input_tokens})
        self._messages.append(self._answer(a))
        
        output_tokens = resp.usage.output_tokens
        reasoning_tokens = resp.usage.output_tokens_details.reasoning_tokens
        self.messages_cost.append({'output': output_tokens, 'output_reasoning': reasoning_tokens})
        self.total_tokens += resp.usage.total_tokens
        
        return {'input': input_tokens, 'output': output_tokens, 'total': resp.usage.total_tokens}
    
    def message_cost(self, role: str, i: int):
        if role == "assistant":
            cost = self.messages_cost[i]['output']
            cost_1 = self.messages_cost[i]['output_reasoning']
        elif role == "user":
            cost = self.messages_cost[i]['input']
            cost_1 = self.messages_cost[i]['input_cached']
        else:
            return "?"
        return f"{cost}|{cost_1}"
