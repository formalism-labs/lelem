
import contextlib

class Actor():
    def __init__(self, conv, space=None):
        self.conv = conv
        self.space = space

    def ask(self, q):
        reply = self.conv.ask(q)
        for line in reply.splitlines():
            words = line.split()
            try:
                w = words[0]
                if w[0] == '@':
                    cmd = w[1:]
                    return self.exec(cmd, words[1:], reply=reply)
            except:
                pass
        return reply

    def exec(self, cmd, args, reply=None):
        with contextlib.chdir(self.space):
            if cmd == 'fread':
                q = command_fread(args[0])
            elif cmd == 'fwrite':
                q = command_fwrite(args[0], reply=reply)
        return self.ask(q)

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
