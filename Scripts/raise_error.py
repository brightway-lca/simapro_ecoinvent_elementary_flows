import json
import sys
from pathlib import Path
from pprint import pprint


BASE_DIR = Path(__file__).parent.parent.resolve()
LOGS_DIR = BASE_DIR / "Logs"


def check_duplicates():
    if any(filename.suffix.lower() == ".json" for filename in LOGS_DIR.iterdir()):
        print("Errors found:")
        for filename in LOGS_DIR.iterdir():
            pprint(json.load(open(filename)))

        sys.exit(1)


if __name__ == "__main__":
    check_duplicates()
