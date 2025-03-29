
from .common import * # noqa: F403, F401

class Questions:
    def __init__(self, qfile):
        self._questions = []
        in_q = False
        with open(qfile, "r") as  file:
            q = ""
            for line in file:
                if line[0] == '#':
                    continue
                line = line.strip()
                if not in_q:
                    if line[0:2] == 'Q:':
                        in_q = True
                        q = line[2:].strip()
                    else:
                        continue
                else:
                    if line[0:2] == 'Q:':
                        self._questions.append(q)
                        q = line[2:].strip()
                    else:
                        q += "\n" + line

    def __iter__(self):
        return iter(self._questions)
