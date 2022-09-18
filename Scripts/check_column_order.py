import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
CONTRIBUTE_DIR = BASE_DIR / "Contribute"
COLUMN_ORDER = [
    "SourceListName", "SourceFlowName", "SourceFlowUUID", "SourceFlowContext", "SourceUnit",
    "MatchCondition", "TargetListName", "TargetFlowName", "TargetFlowUUID",
    "TargetFlowContext", "TargetUnit", "Mapper", "Verifier", "LastUpdated", "MemoMapper",
    "MemoVerifier", "MemoSource", "MemoTarget"
]


def check_column_order():
    assert CONTRIBUTE_DIR.is_dir()

    for filename in CONTRIBUTE_DIR.iterdir():
        if filename.suffix.lower() == ".csv":
            df = pd.read_csv(CONTRIBUTE_DIR / filename)
            if list(df.columns) != COLUMN_ORDER:
                df = df[COLUMN_ORDER]
                df.to_csv(filename, index=False)


if __name__ == "__main__":
    check_column_order()