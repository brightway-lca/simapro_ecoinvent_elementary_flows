import sys
import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent.resolve()
TEMPLATES_DIR = BASE_DIR / "Templates"


def add_contributor():
    assert TEMPLATES_DIR.is_dir()

    try:
        username = str(sys.argv[1])
        print(username)
    except:
        print("Can't get username; not adding new data contributor")


if __name__ == "__main__":
    add_contributor()
