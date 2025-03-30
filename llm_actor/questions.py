
from .common import * # noqa: F403, F401

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SESSIONS = os.path.abspath(os.path.join(ROOT, "sessions"))

class Questions:
    def __init__(self, qfile):
        self._questions = []
        in_q = False
        qfile0 = qfile
        if not os.path.exists(qfile):
            qfile = f"{SESSIONS}/{qfile}"
            if not os.path.exists(qfile):
                raise Exception(f"{qfile0} cannot be found")
        with open(qfile, "r") as  file:
            q = ""
            for line in file:
                if line[0] == '#':
                    continue
                line = line.strip()
                if line == "":
                    continue
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
            if in_q and q != "":
                self._questions.append(q)

    def __iter__(self):
        return iter(self._questions)
