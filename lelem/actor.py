
from .common import *
import paella
from .conversation import ConversationBase
from .questions import Question

class Actor():
    def __init__(self, conv: ConversationBase, space: Optional[str] = None):
        self.conv: ConversationBase = conv
        if space is None:
            raise Exception("no space is given for actor")
        space0 = space
        if not os.path.isdir(space):
            space = f"{SPACES}/{space}"
            if not os.path.isdir(space):
                raise Exception(f"space not found: {space0}")
        self.space = space

    def ask(self, q: Question) -> str:
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
                raise Exception(f"error executing command: {cmd} {words[1:]}") from x
        return answer

    def exec(self, cmd: str, args: List[str], reply: Optional[str] = None):
        with contextlib.chdir(self.space):
            if cmd == 'fread':
                answer = command_fread(args[0])
            elif cmd == 'fwrite':
                return command_fwrite(args[0], reply=reply)
            elif cmd == 'ls':
                answer = command_ls(args, space=self.space, reply=reply)
            else:
                return f"there is no command named @{cmd}. please revise."
        q = Question(answer, response=True)
        return self.conv.ask(q)

    def print_summary(self) -> None:
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

def command_fwrite(filepath, reply: Optional[str] = None):
    text = ""
    collecting = False
    for line in re.split(r'(\n)', reply): # reply.splitlines():
        if line.startswith("@fwrite"):
            collecting = True
        elif collecting:
            if line == "@end":
                collecting = False
                break
            else:
                text += line
    if collecting:
        print("Warning: in @fwrite: @end is missing from reply")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return f"Written file {filepath}"

def command_ls(paths, space: str, reply: Optional[str] = None):
    path = paths[0] if len(paths) > 0 else ""
    if path == "":
        path = "/"
    try:
        text= paella.sh(f"ls {space}/{path}")
        return f"""
@response
{text}
@endresponse
"""
    except:
        return f"path {path} does not exist"

def command_patch(filepath, reply: Optional[str] = None):
    pass

def command_git_add(filepath, reply: Optional[str] = None):
    pass

commands = {
    'fread': { 'fn': command_fread, 'reask': True },
    'fwrite': { 'fn': command_fread, 'reask': False },
    'ls': { 'fn': command_ls, 'reask': True },
    'git-add': { 'fn': command_git_add, 'reask': False },
}
