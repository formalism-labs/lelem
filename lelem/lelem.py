
from .common import *
import os
import argparse
import readline
from lelem import Model, Models, Question, Questions, Prolog, Actor, create_conv

DEFAULT_MODEL = "gemini-2.0-flash-lite"

def find_questions(dir, prefix):
    if dir == "":
        dir = "."
    elif not os.path.isdir(dir):
        return None
    files = [f for f in os.listdir(dir) if f.startswith(prefix)]
    if len(files) == 1:
        return files[0]
    return None

def main():
    parser = argparse.ArgumentParser(description='Conversation with lelem that asks')
    parser.add_argument('-m', '--model', type=str, default=DEFAULT_MODEL, help=f"Use given model (default: {DEFAULT_MODEL})")
    parser.add_argument('--lc', action="store_true", help='Use LangChain')
    parser.add_argument('-a', '--actor', action="store_true", help='Actor mode')
    parser.add_argument('-p', '--prolog', type=str, default='prologs/apprentice-system.1', help="Use given prolog")
    parser.add_argument('-q', '--questions', type=str, default='004-bolt', help="Questions file")
    parser.add_argument('--space', type=str, help='Operate inside given space')
    parser.add_argument('-i', '--interactive', action="store_true", help='Interactive mode')
    parser.add_argument('-s', '--summary', action="store_true", help='Print summary')
    parser.add_argument('--models', action="store_true", help='Print models')
    args = parser.parse_args()

    if args.models:
        Models().print_table()
        exit(0)

    try:
        if args.interactive:
            prolog = Prolog()
            
            conv = create_conv(model_name=args.model, use_langchain=args.lc, prolog=prolog)
            if args.actor:
                space = qq.space or f"{SPACES}/001"
                act = Actor(conv, space=space)
                x_conv = act
            else:
                x_conv = conv

            qt = input(">>> ")
            while qt != "/bye":
                q = Question(qt)
                a = x_conv.ask(q).strip()
                if "\n" in a:
                    print(f"{RED}A:\n{BW}{BLUE}{a}{NOC}")
                else:
                    print(f"{RED}A: {BW}{BLUE}{a}{NOC}")
                qt = input(">>> ")
            print("So long.")
            if args.summary:
                conv.print_summary()
            exit(0)

        questions_file = find_questions(os.path.dirname(args.questions), os.path.basename(args.questions))
        if questions_file is None:
            questions_file = find_questions("sessions", args.questions)
            if questions_file is None:
                print(f"Error: cannot find {questions_file}")
                exit(1)
        qq = Questions(questions_file)

        is_actor = args.actor or qq.actor

        prolog = None
        if is_actor:
            fprolog = args.prolog
            if fprolog != "":
                prolog = Prolog(fprolog)

        conv = create_conv(model_name=args.model, use_langchain=args.lc, prolog=prolog)

        x_conv = None

        def ask(q: Question):
            q.pprint()
            a = x_conv.ask(q).strip()
            if "\n" in a:
                print(f"{RED}A:\n{BW}{BLUE}{a}{NOC}")
            else:
                print(f"{RED}A: {BW}{BLUE}{a}{NOC}")

        if is_actor or qq.actor:
            space = qq.space or f"{SPACES}/001"
            act = Actor(conv, space=space)
            x_conv = act
        else:
            x_conv = conv

        for q in qq:
            ask(q)
        if args.summary:
            conv.print_summary()
    except Exception as x:
        print(f"{BRED}Error: {x}{BW}")
        sys.excepthook(type(x), x, x.__traceback__)
        conv.print_summary()
