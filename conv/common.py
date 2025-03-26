
import os
import sys
import json
import traceback
from rich import print_json

import inspect
parent_globals = inspect.stack()[1].frame.f_globals
parent_globals.update(globals())
