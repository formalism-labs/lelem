
from ..common import *
from ..conversation import ConversationBase, DEFAULT_PROLOG
from ..questions import Question
from ..prolog import Prolog

from langchain.schema import SystemMessage, HumanMessage, AIMessage

class Conversation(ConversationBase):
    def __init__(self, chat, model: Optional[str] = None, prolog: Optional[Prolog] = None):
        super().__init__()
        self.chat = chat
        if model is None:
            try:
                self.model = chat.model_name
            except:
                raise Exception("cannot determine model name")
        else:
            self.model = model
        self.prolog = DEFAULT_PROLOG if prolog is None else str(prolog)
        self._messages = [SystemMessage(content=self.prolog)]
    
    def ask(self, q: Question):
        t0 = time.time()
        self._messages.append(HumanMessage(content=q.text))
        try:
            resp = self.chat.invoke(self._messages)
        except Exception as x:
            print(f"When asking: {q.text}\nAn error occurred: {x}")
            raise x
        input_tokens = output_tokens = total_tokens = 0
        if isinstance(resp, str):
            answer = resp
            input_tokens = self.chat.get_num_tokens(q.text)
            output_tokens = self.chat.get_num_tokens(resp)
            total_tokens = input_tokens + output_tokens
        elif hasattr(resp, 'content'):
            answer = resp.content
            try:
                token_usage = resp.usage_metadata
                if token_usage:
                    input_tokens = token_usage.get('input_tokens', 0)
                    output_tokens = token_usage.get('output_tokens', 0)
                    total_tokens = token_usage.get('total_tokens', 0)
            except:
                pass
        else:
            raise Exception('cannot determine LLM output')
        self._messages.append(AIMessage(content=answer))
        
        self.messages_cost.append({'input': input_tokens, 'total': input_tokens})
        self.messages_cost.append({'output': output_tokens, 'total': output_tokens})
        self.total_tokens += total_tokens

        self.add_qa(q, answer, time.time() - t0, {'input': input_tokens, 'output': output_tokens, 'total': total_tokens})
        return answer

    @property
    def messages(self):
        t = f"model={self.model}\n"
        i = 0
        for m in self._messages:
            # role = "A" if isinstance(m, AIMessage) else "Q" if isinstance(m, HumanMessage) else "System"
            if isinstance(m, SystemMessage):
                continue
            text = m.content
            if "\n" in text:
                text = "\n" + text
            if isinstance(m, AIMessage):
                title = "A"
                cost = self.messages_cost[i]['output']
            elif isinstance(m, HumanMessage):
                title = "Q"
                cost = self.messages_cost[i]['input']
            t += f"{title}({cost}): {text}\n"
            i += 1
        t += f"={self.total_tokens}\n"
        t += f"t={time.time() - self.t0:.2f}"
        return t
