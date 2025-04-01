
from .common import *
from .models import Model, Models
from .questions import Question
from .prolog import Prolog

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

    @abstractmethod
    def ask(self, q: Question):
        pass

    def add_qa(self, question: Question, answer: str, time: float, cost: Any):
        self._conv.append({'question': str(question), 'answer': answer, 'time': float, 'cost': cost})

    def message_cost(self, role: str, i: int):
        if role == "assistant":
            cost = self.messages_cost[i]['output']
        elif role == "user":
            cost = self.messages_cost[i]['input']
        else:
            return "?"
        return f"{cost}"
    
    @property
    def messages(self):
        t = f"model={RED}{self.model}{BW}\n"
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
            if title == 'Q':
                t += f"{BRED}{title}({cost}):{NOC} {BRI + BLUE}{text}{NOC}\n"
            else:
                t += f"{BRED}{title}({cost}):{NOC} {BLUE}{text}{NOC}\n"
            i += 1
        t += f"={self.total_tokens}\n"
        t += f"t={time.time() - self.t0:.2f}"
        return t

    def conversation(self):
        return self._conv
        
    def questions(self):
        return list(map(lambda m: m['question'], self._conv))

    def print_summary(self):
        print('---')
        print(self.messages)
        print('---')
        # print_json(data=self.conversation())
        # print('---')
                
        class MultiLineDumper(yaml.Dumper):
            def represent_scalar(self, tag, value, style=None):
                if "\n" in value:
                    style = "|"
                return super().represent_scalar(tag, value, style)

        # print(yaml.dump(self.conversation(), sort_keys=False, default_flow_style=False, Dumper=MultiLineDumper))

def find_model(model_name):
    models = Models()
    model = models.match(model_name)
    if model == []:
        print(f"Error: no model matches {model_name}")
        exit(1)
    elif isinstance(model, list):
        matched_models = model
        for m in matched_models:
            if m.name == model_name:
                return m
        print(f"Error: more than one model match: {[model.name for model in model]}")
        exit(1)
    return model

def create_conv(model_name: Optional[str] = None, prolog: Optional[Prolog] = None, use_langchain: bool = False, temperature: float = 0) -> ConversationBase:
    model = find_model(model_name)

    if use_langchain:
        from langchain_core.language_models.chat_models import BaseChatModel
        from lelem.langchain import Conversation # type: ignore
        lc_chat: Any = None # Optional[BaseChatModel]
        ai: Any = None

    if model.by == "openai":
        if not use_langchain:
            from openai import OpenAI
            from lelem.openai.responses import Conversation # type: ignore
            ai = OpenAI()
        else:
            from langchain_openai import ChatOpenAI
            lc_chat = ChatOpenAI(model=model.full_name, temperature=temperature)
    elif model.by == "anthropic":
        if not use_langchain:
            import anthropic
            from lelem.anthropic import Conversation # type: ignore
            api_key = os.getenv("ANTHROPIC_API_KEY")
            ai = anthropic.Anthropic(api_key=api_key)
        else:
            raise Exception("ollama/anthropic is not supported yet")
    elif model.by == "google":
        if not use_langchain:
            from google import genai
            from lelem.gemini import Conversation # type: ignore
            api_key = os.getenv("GOOGLE_API_KEY")
            ai = genai.Client(api_key=api_key)
        else:
            from langchain_google_genai import GoogleGenerativeAI
            lc_chat = GoogleGenerativeAI(model=model.full_name, temperature=temperature)
    elif model.by == "deepseek":
        if not use_langchain:
            import openai
            from lelem.deepseek import Conversation # type: ignore
            api_key = os.getenv("DEEPSEEK_API_KEY")
            ai = openai.OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        else:
            from langchain_deepseek import ChatDeepSeek
            lc_chat = ChatDeepSeek(model=model.full_name, temperature=temperature)
    elif model.ollama:
        if use_langchain:
            from langchain_ollama import ChatOllama
            lc_chat = ChatOllama(model=model.full_name, temperature=temperature, n_gpu_layers=-1)
        else:
            raise Exception("native ollama is not supported yet")

    if not use_langchain:
        conv = Conversation(ai, model=model.full_name, prolog=prolog, temperature=temperature) # type: ignore
    else:
        conv = Conversation(lc_chat, model=model.full_name, prolog=prolog) # type: ignore
    return conv
