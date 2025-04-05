
from .common import * # noqa: F403, F401
import paella # type: ignore

DEFAULT_PROLOG = """
You are a knowledgeable and articulate AI assistant.
Keep your answer very concise. Do not provide extra information unless asked.
"""

class Prolog:
    def __init__(self, fpath: str = f"{PROLOGS}/apprentice-system.1", comments: bool = True):
        fpath0 = fpath
        self.text = ""
        if not os.path.exists(fpath):
            fpath = f"{PROLOGS}/{fpath}"
            if not os.path.exists(fpath):
                raise Exception("Prolog: {fpath0} not found")
        fdir = os.path.dirname(fpath)
        with open(fpath, "r") as file:
            for line in file:
                if line[0] == '\\':
                    self.text += line[1:]
                    continue
                if line[0] == '#':
                    continue
                if line[0] == '@':
                    fpath1 = os.path.join(fdir, line.strip()[1:])
                    with open(fpath1, "r") as file1:
                        for line1 in file1:
                            if comments and line1[0] == '#':
                                continue
                            self.text += line1
                        self.text += "\n"
                else:
                    self.text += line

    def __str__ (self):
        return self.text

def main():
    import argparse
    import tiktoken
    from rich.console import Console
    from rich.markdown import Markdown

    parser = argparse.ArgumentParser(description='Display lelem prolog')
    parser.add_argument('-m', '--model', type=str, default="gpt-4o-mini", help=f"Use given model for token estimation")
    parser.add_argument('-x', '--markdown', action="store_true", help='Display as Markdown')
    parser.add_argument('--no-comments', action="store_true", help='Disallow comments in included files')
    parser.add_argument('name', nargs="?", default="apprentice-system.1", help='Prolog name')
    args = parser.parse_args()

    prolog = Prolog(args.name, comments=not args.no_comments)
    text = str(prolog)
    if args.markdown:
        print()
        console = Console()
        console.print(Markdown(text.replace("\n", "  \n")))
        print()
    else:
        print("\n" + text)

    try:
        enc = tiktoken.encoding_for_model(args.model)
    except:
        enc = tiktoken.get_encoding(args.model)

    ntok = len(enc.encode(prolog))
    print(f"={len(prolog)} [{ntok}]")
