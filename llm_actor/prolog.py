
from .common import * # noqa: F403, F401

class Prolog:
    def __init__(self, fpath = "prologs/apprentice-system.1"):
        self.text = ""
        fdir = os.path.dirname(fpath)
        with open(fpath, "r") as file:
            for line in file:
                if line[0] == '@':
                    fpath1 = os.path.join(fdir, line.strip()[1:])
                    with open(fpath1, "r") as file:
                        text1 = file.read()
                        self.text += text1 + "\n"
                elif line[0] == '#':
                    continue
                else:
                    self.text += line

    def __str__ (self):
        return self.text
