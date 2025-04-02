
from .common import * # noqa: F403, F401
import paella # type: ignore

DEFAULT_PROLOG = """
You are a knowledgeable and articulate AI assistant.
Keep your answer very concise. Do not provide extra information unless asked.
"""

class Prolog:
    def __init__(self, fpath = "prologs/apprentice-system.1"):
        self.text = ""
        fdir = os.path.dirname(fpath)
        with open(fpath, "r") as file:
            for line in file:
                if line[0] == '#':
                    continue
                if line[0] == '@':
                    fpath1 = os.path.join(fdir, line.strip()[1:])
                    with open(fpath1, "r") as file1:
                        for line1 in file1:
                            if line1[0] == '#':
                                continue
                            self.text += line1
                        self.text += "\n"
                else:
                    self.text += line

    def __str__ (self):
        return self.text

def main():
    import tiktoken

    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        fname = "prologs/apprentice-system.1"
    prolog = str(Prolog(fname))
    print("\n" + prolog)

    model = os.getenv("MODEL", "gpt-4o-mini")
    try:
        enc = tiktoken.encoding_for_model(model)
    except:
        enc = tiktoken.get_encoding(model)

    ntok = len(enc.encode(prolog))
    print(f"={len(prolog)} [{ntok}]")
