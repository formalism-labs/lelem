
from .common import *
from .models import Model, Models, find_model
from .questions import Question
from .prolog import Prolog

class ExchangeTokens(TypedDict):
    input: int
    output: int
    total: int

class Exchange(TypedDict):
    question: str
    answer: str
    time: float
    cost: ExchangeTokens

class ConversationBase:
    def __init__(self):
        self.t0: float = time.time()
        self._messages = []
        self.messages_cost = []
        self._conv: List[Exchange] = []
        self.total_tokens = 0
        self.space: str = ''
        self.questions_file: Optional[str] = None
        self.temperature = 1

    @abstractmethod
    def ask(self, q: Question):
        pass

    def add_qa(self, question: Question, answer: str, time: float, cost: Any):
        self._conv.append({'question': str(question), 'answer': answer, 'time': time, 'cost': cost})

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
        t = ""
        t += f"model: {RED}{self.model}{BW}\n"
        t += f"space: {RED}{self.space}{BW}\n"
        t += f"termerature: {RED}{self.temperature}{BW}\n"
        t += "\n"

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
                t += f"{BRED}{title}({cost}):{NOC} {BBLUE}{text}{NOC}\n"
            else:
                t += f"{BRED}{title}({cost}):{NOC} {BLUE}{text}{NOC}\n"
            i += 1
        t += f"={self.total_tokens}\n"
        t += f"t={time.time() - self.t0:.2f}"
        return t

    def conversation(self):
        return self._conv
        
    def questions(self) -> List[str]:
        return list(map(lambda m: m['question'], self._conv))

    @property
    def summary(self) -> str:
        #class MultiLineDumper(yaml.Dumper):
        #    def represent_scalar(self, tag, value, style=None):
        #        if "\n" in value:
        #            style = "|"
        #        return super().represent_scalar(tag, value, style)

        # yaml = yaml.dump(self.conversation(), sort_keys=False, default_flow_style=False, Dumper=MultiLineDumper)
        data = {
            'model': self.model,
            'space': self.space,
            'temperature': self.temperature
            }
        if self.questions_file is not None:
            data["questions"] = self.questions_file
            
        data['conversation'] = self.conversation()

        return yaml.dump(data, sort_keys=False)
    
    def log_summary(self):
        text = self.summary
        flog = datetime.now().strftime("%Y%m%d-%H%M%S")
        paella.mkdir_p(LOGS)
        with open(f"{LOGS}/{flog}.yml", 'w') as file:
            file.write(text)
    
    def print_messages(self):
        print('---\n')
        print(self.messages)

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
            lc_chat = ChatOllama(model=model.full_name, temperature=temperature) #, n_gpu_layers=-1)
        else:
            raise Exception("native ollama is not supported yet")

    if not use_langchain:
        conv = Conversation(ai, model=model.full_name, prolog=prolog, temperature=temperature) # type: ignore
    else:
        conv = Conversation(lc_chat, model=model.full_name, prolog=prolog) # type: ignore
        
    conv.temperature = temperature
    return conv
