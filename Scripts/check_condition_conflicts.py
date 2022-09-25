import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent.resolve()
CONTRIBUTE_DIR = BASE_DIR / "Contribute"
MAPPED_FILES_DIR = BASE_DIR / "Mapping" / "Output" / "Mapped_files"
LOGS_DIR = BASE_DIR / "Logs"


FIELDS = [
    "SourceFlowName",
    "SourceFlowUUID",
    "SourceFlowContext",
    "TargetFlowName",
    "TargetFlowUUID",
    "TargetFlowContext",
]


def check_condition_conflicts():
    assert CONTRIBUTE_DIR.is_dir()
    assert MAPPED_FILES_DIR.is_dir()

    if any(filename.suffix.lower() == ".json" for filename in LOGS_DIR.iterdir()):
        return

    existing = {
        tuple([row[field] for field in FIELDS]): row["MatchCondition"]
        for _, row in pd.read_csv(
            MAPPED_FILES_DIR / "SimaProv94-ecoinventEFv3.7.csv"
        ).iterrows()
    }

    errors = []

    for filename in CONTRIBUTE_DIR.iterdir():
        if filename.suffix.lower() == ".csv":
            new = {
                tuple([row[field] for field in FIELDS]): row["MatchCondition"]
                for _, row in pd.read_csv(CONTRIBUTE_DIR / filename).iterrows()
            }
            conflicts = []

            for key, condition in new.items():
                if key in existing and existing[key] != condition:
                    conflicts.append(
                        {
                            "source": key[:3],
                            "target": key[3:],
                            "current": existing[key],
                            "new": condition,
                        }
                    )
            if conflicts:
                errors.append(
                    {
                        "message": "conflicting conditions",
                        "filename": filename.name,
                        "conflicts": conflicts,
                    }
                )

    if errors:
        with open(
            LOGS_DIR / "check_condition_conflicts.json", "w", encoding="utf-8"
        ) as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    check_condition_conflicts()
