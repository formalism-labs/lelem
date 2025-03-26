
import time

DEFAULT_PROLOG = """
You are a knowledgeable and articulate AI assistant.
Keep your answer very concise. Do not provide extra information unless asked.
"""

class ConversationBase:
    def __init__(self):
        self.t0 = time.time()
        self._messages = []
        self.messages_cost = []
        self._conv = []
        self.total_tokens = 0

    def add_qa(self, question, answer, time, cost):
        self._conv.append({'question': question, 'answer': answer, 'time': time, 'cost': cost})

    def message_cost(self, role, i):
        if role == "assistant":
            cost = self.messages_cost[i]['output']
        elif role == "user":
            cost = self.messages_cost[i]['input']
        else:
            return "?"
        return f"{cost}"
    
    @property
    def messages(self):
        t = f"model={self.model}\n"
        i = 0
        for m in self._messages:
            role = m["role"]
            text = m["content"]
            if "\n" in text:
                text = "\n" + text
            if role == "assistant":
                title = "A"
                # cost = self.messages_cost[i]['output']
            elif role == "user":
                title = "Q"
                # cost = self.messages_cost[i]['input']
            elif role == "system":
                continue
            else:
                title = role
            cost = self.message_cost(role, i)
            t += f"{title}({cost}): {text}\n"
            i += 1
        t += f"={self.total_tokens}\n"
        t += f"t={time.time() - self.t0:.2f}"
        return t

    def conversation(self):
        return self._conv
        
    def questions(self):
        return list(map(lambda m: m['question'], self._conv))
