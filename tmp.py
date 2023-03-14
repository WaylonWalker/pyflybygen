from pathlib import Path

from .pyflybygen import pyflybygen

statements = """
from __future__ import (absolute_import,
                        division)
import os
import collections, itertools
from math import *
from gzip import open as gzip_open
from subprocess import check_output, Popen
"""


imports = more_itertools.flatten(
    [get_imports(p.read_text()) for p in Path(".").glob("**/*.py")]
)
print("\n".join(set(imports)))
