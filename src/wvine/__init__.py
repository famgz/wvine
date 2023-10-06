import sys
from pathlib import Path

if __package__ is None:
    sys.path.insert(0, Path(__file__).resolve().parent.parent)

from .l3 import getkey
