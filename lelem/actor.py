
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
        self.conv.space = space

    def ask(self, q: Question) -> str:
        answer = self.conv.ask(q)
        if q.noc:
            return answer
        cmd = ""
        in_cmd = False
        for line in answer.splitlines():
            if line == '---BEGIN @-COMMAND---':
                in_cmd = True
            elif line == '---END @-COMMAND---':
                if in_cmd:
                    in_cmd = False
                    try:
                        cmd_dict = json.loads(cmd)
                    except Exception as x:
                        raise Exception(f"invalid command: {cmd}") from x
                    try:
                        return self.exec(cmd_dict, reply=answer)
                    except Exception as x:
                        raise Exception(f"error executing command: {cmd}") from x
            elif in_cmd:
                cmd += line + "\n"
        return answer

    def exec(self, cmd: dict, reply: Optional[str] = None):
        cmd_name = cmd["name"]
        with contextlib.chdir(self.space):
            if cmd_name == 'fread':
                answer = command_fread(cmd['path'])
                q = Question(answer, response=True)
                return self.conv.ask(q)
            elif cmd_name == 'fwrite':
                return command_fwrite(cmd['path'], cmd['content'], reply=reply)
            elif cmd_name == 'ls':
                try:
                    path = cmd['path']
                except:
                    path = '/'
                answer = command_ls(path, space=self.space, reply=reply)
                q = Question(answer, response=True)
                return self.ask(q)
            elif cmd_name == 'patch':
                return command_patch(cmd['path'], cmd['content'], reply=reply)
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
            text = json.dumps({'content': f.read()})
        return f"""
---BEGIN @-COMMAND RESPONSE---
{text}
---END @-COMMAND RESPONSE---
"""
    except:
        return f"file {filepath} does not exist"

def command_fwrite(filepath: str, content: str, reply: Optional[str] = None):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"Written file {filepath}"

def command_patch(filepath: str, content: str, reply: Optional[str] = None):
    fpatch = paella.tempfilepath("", ".patch")
    with open(fpatch, 'w', encoding='utf-8') as f:
        f.write(content)
    try:
        paella.sh(f"patch -p1 -i {fpatch}")
        return f"Patched file {filepath}"
    except:
        return f"Problem patching file {filepath}"

def command_ls(path, space: str, reply: Optional[str] = None):
    if path == "":
        path = "/"
    try:
        output = paella.sh(f"ls {space}/{path}")
        text = json.dumps({'content': output})
        return f"""
---BEGIN @-COMMAND RESPONSE---
{text}
---END @-COMMAND RESPONSE---
"""
    except:
        return f"path {path} does not exist"

def command_git_add(filepath, reply: Optional[str] = None):
    pass

commands = {
    'fread': { 'fn': command_fread, 'reask': True },
    'fwrite': { 'fn': command_fread, 'reask': False },
    'ls': { 'fn': command_ls, 'reask': True },
    'git-add': { 'fn': command_git_add, 'reask': False },
}
