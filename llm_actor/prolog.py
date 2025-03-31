
from .common import * # noqa: F403, F401

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
