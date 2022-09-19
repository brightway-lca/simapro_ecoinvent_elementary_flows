import sys
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent.resolve()
LOGS_DIR = BASE_DIR / "Logs"


def check_duplicates():
    if any(filename.suffix.lower() == ".json" for filename in LOGS_DIR.iterdir()):
        sys.exit(1)


if __name__ == "__main__":
    check_duplicates()
