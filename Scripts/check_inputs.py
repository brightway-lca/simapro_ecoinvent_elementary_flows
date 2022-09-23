import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent.resolve()
CONTRIBUTE_DIR = BASE_DIR / "Contribute"
LOGS_DIR = BASE_DIR / "Logs"
REQUIRED_COLUMNS = {
    "SourceListName",
    "SourceFlowName",
    "SourceFlowUUID",
    "SourceFlowContext",
    "SourceUnit",
    "TargetListName",
    "TargetFlowName",
    "TargetFlowUUID",
    "TargetFlowContext",
    "TargetUnit",
}
OPTIONAL_COLUMNS = {
    "ConversionFactor"
    "MatchCondition",
    "Mapper",
    "Verifier",
    "LastUpdated",
    "MemoMapper",
    "MemoVerifier",
    "MemoSource",
    "MemoTarget",
}
ALLOWED_COLUMNS = REQUIRED_COLUMNS.union(OPTIONAL_COLUMNS)


def check_inputs():
    assert CONTRIBUTE_DIR.is_dir()

    if any(filename.suffix.lower() == ".json" for filename in LOGS_DIR.iterdir()):
        return

    errors = []

    for filename in CONTRIBUTE_DIR.iterdir():
        if filename.suffix.lower() == ".csv":
            df = pd.read_csv(CONTRIBUTE_DIR / filename)
            if set(df.columns).symmetric_difference(REQUIRED_COLUMNS).difference(OPTIONAL_COLUMNS):
                errors.append(
                    {
                        "message": "Incorrect columns",
                        "filename": filename.name,
                        "extra columns": sorted(
                            set(df.columns).difference(ALLOWED_COLUMNS)
                        ),
                        "missing columns": sorted(
                            REQUIRED_COLUMNS.difference(set(df.columns))
                        ),
                    }
                )
        elif not filename.name.startswith("."):
            errors.append({"message": "unknown filetype", "filename": filename.name})
    if errors:
        with open(LOGS_DIR / "check_inputs.json", "w", encoding="utf-8") as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    check_inputs()
