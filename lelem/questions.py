
from .common import * # noqa: F403, F401

class Question:
    def __init__(self, text: str = "", response: bool = False):
        self.response = response
        self.text = ""
        self.noc = False # no commands flag
        if text != "":
            self.append_line(text)

    def append_line(self, line):
        if line == "@noc":
            self.noc = True
            return
        self.text += ("\n" if self.text != "" else "") + line

    def is_multiline(self):
        return "\n" in self.text

    def pprint(self):
        color = BLUE if self.response else BBLUE
        print(f"\n{RED}Q: {BW}{color}{self.text}{BW}")

    def __str__ (self):
        return self.text

class Questions:
    def __init__(self, qfile: str):
        self._questions : List[Question] = []
        self.actor = False
        self.space = None

        qfile0 = qfile
        if not os.path.exists(qfile):
            qfile = f"{SESSIONS}/{qfile}"
            if not os.path.exists(qfile):
                raise Exception(f"Questions file '{qfile0}' cannot be found")
        self._file = qfile
        with open(qfile, "r") as file:
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
                        q = Question(t)
                    elif line[0] == '@':
                        self.process_directive(line)
                        continue
                elif line[0:2] == 'Q:':
                    self._questions.append(q)
                    t = line[2:].strip()
                    q = Question(t)
                else:
                    q.append_line(line)
            if q is not None:
                self._questions.append(q)

    def process_directive(self, line):
        words = line[1:].split()
        if words[0] == 'actor':
            self.actor = True
            return
        if words[0] == 'space':
            if len(words) < 2:
                raise Exception(f"in {self._file}: invalid space specification: {line}")
            self.space = words[1]
            return
        raise Exception(f"in {self._file}: invalid directive: {line}")

    def __iter__(self):
        return iter(self._questions)
