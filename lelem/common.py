
from abc import ABC, abstractmethod
import contextlib
import os
import re
import sys
import time
from typing import Any, cast, Dict, List, Optional, TypedDict
import yaml

# from rich import print_json
# from rich.syntax import Syntax
# from rich.console import Console
from colorama import Fore, Style

BRI = BOLD = Style.BRIGHT
BW = NOC = Style.RESET_ALL
RED = Fore.RED
BRED = BRI + RED
GREEN = Fore.GREEN
BGREEN = BRI + GREEN
BLUE = Fore.BLUE
BBLUE = BRI + BLUE

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SESSIONS = os.path.abspath(os.path.join(ROOT, "sessions"))
PROLOGS = os.path.abspath(os.path.join(ROOT, "prologs"))
SPACES = os.path.abspath(os.path.join(ROOT, "../lelem-spaces/spaces"))
