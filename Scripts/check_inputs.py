import json
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent.resolve()
CONTRIBUTE_DIR = BASE_DIR / "Contribute"
LOGS_DIR = BASE_DIR / "logs"
EXPECTED_COLUMNS = {
    "SourceListName",
    "SourceFlowName",
    "SourceFlowUUID",
    "SourceFlowContext",
    "SourceUnit",
    "MatchCondition",
    "TargetListName",
    "TargetFlowName",
    "TargetFlowUUID",
    "TargetFlowContext",
    "TargetUnit",
    "Mapper",
    "Verifier",
    "LastUpdated",
    "MemoMapper",
    "MemoVerifier",
    "MemoSource",
    "MemoTarget",
}


def check_inputs():
    assert CONTRIBUTE_DIR.is_dir()

    errors = []

    for filename in CONTRIBUTE_DIR.iterdir():
        if filename.suffix.lower() == ".csv":
            df = pd.read_csv(CONTRIBUTE_DIR / filename)
            if set(df.columns).symmetric_difference(EXPECTED_COLUMNS):
                errors.append(
                    {
                        "message": "Incorrect columns",
                        "filename": filename.name,
                        "extra columns": sorted(
                            set(df.columns).difference(EXPECTED_COLUMNS)
                        ),
                        "missing columns": sorted(
                            EXPECTED_COLUMNS.difference(set(df.columns))
                        ),
                    }
                )
        elif not filename.name.startswith("."):
            errors.append({"message": "unknown filetype", "filename": filename.name})
    if errors:
        with open(LOGS_DIR / "check_inputs.json", "w", encoding="utf-8") as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)
        sys.exit(1)


if __name__ == "__main__":
    check_inputs()
