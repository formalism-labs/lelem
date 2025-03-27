
import contextlib
from rich import print_json
import yaml
from rich.syntax import Syntax
from rich.console import Console

class Actor():
    def __init__(self, conv, space=None):
        self.conv = conv
        if space is None:
            raise Exception("no space is given for actor")
        self.space = space

    def ask(self, q):
        answer = self.conv.ask(q)
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

    def exec(self, cmd, args, reply=None):
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

def command_fread(filepath, reply=None):
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

def command_fwrite(filepath, text, reply=None):
    pass

def command_patch(filepath, text, reply=None):
    pass

def command_git_add(filepath, text, reply=None):
    pass

commands = {
    'fread': command_fread,
    'fwrite': command_fread,
    'git-add': command_git_add,
}
