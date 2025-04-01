
from .common import *
from .conversation import ConversationBase
from .questions import Question

class Actor():
    def __init__(self, conv: ConversationBase, space: Optional[str] = None):
        self.conv: ConversationBase = conv
        if space is None:
            raise Exception("no space is given for actor")
        self.space = space

    def ask(self, q: Question):
        answer = self.conv.ask(q)
        if q.noc:
            return answer
        for line in answer.splitlines():
            words = line.split()
            if len(words) == 0:
                continue
            try:
                w = words[0]
                if w[0] == '@':
                    cmd = w[1:]
                    return self.exec(cmd, words[1:], reply=answer)
            except Exception as x:
                raise Exception(f"error while executing command: {cmd} {words[1:]}") from x
        return answer

    def exec(self, cmd: str, args: List[str], reply: Optional[str] = None):
        with contextlib.chdir(self.space):
            if cmd == 'fread':
                q = command_fread(args[0])
            elif cmd == 'fwrite':
                q = command_fwrite(args[0], reply=reply)
            else:
                return f"there is no command named @{cmd}. please revise."
        return self.conv.ask(q)

    def print_summary(self):
        self.conv.print_summary()

def command_fread(filepath: str, reply: Optional[str] = None):
    text = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        return f"""
@response
{text}
@endresponse
"""
    except:
        return f"file {filepath} does not exist"

def command_fwrite(filepath, text: str, reply: Optional[str] = None):
    pass

def command_patch(filepath, text: str, reply: Optional[str] = None):
    pass

def command_git_add(filepath, text: str, reply: Optional[str] = None):
    pass

commands = {
    'fread': command_fread,
    'fwrite': command_fread,
    'git-add': command_git_add,
}
