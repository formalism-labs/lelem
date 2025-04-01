
from .common import * # noqa: F403, F401

class Question:
    def __init__(self, text: str = ""):
        self.text = text.strip()
        self.noc = False # no commands flag

    def append_line(self, line):
        self.text += ("\n" if self.text != "" else "") + line

    def is_multiline(self):
        return "\n" in self.text

    def pprint(self):
        print(f"\n{RED}Q: {BW}{BBLUE}{self.text}{BW}")

    def __str__ (self):
        return self.text

class Questions:
    def __init__(self, qfile: str):
        self._questions : List[Question] = []
        qfile0 = qfile
        if not os.path.exists(qfile):
            qfile = f"{SESSIONS}/{qfile}"
            if not os.path.exists(qfile):
                raise Exception(f"{qfile0} cannot be found")
        with open(qfile, "r") as  file:
            q = None
            for line in file:
                if line[0] == '#':
                    continue
                line = line.strip()
                if line == "":
                    continue
                if q is None:
                    if line[0:2] == 'Q:':
                        t = line[2:].strip()
                        q = Question()
                        if t == "@noc":
                            q.noc = True
                        else:
                            q.append_line(t)
                    else:
                        # comments or directives here
                        continue
                elif line[0:2] == 'Q:':
                    self._questions.append(q)
                    t = line[2:].strip()
                    q = Question()
                    if t == "@noc":
                        q.noc = True
                    else:
                        q.append_line(t)
                else:
                    q.append_line(line)
            if q is not None:
                self._questions.append(q)

    def __iter__(self):
        return iter(self._questions)
