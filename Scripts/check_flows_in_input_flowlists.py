import json
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent.resolve()
CONTRIBUTE_DIR = BASE_DIR / "Contribute"
LOGS_DIR = BASE_DIR / "logs"
FLOWLISTS_DIR = BASE_DIR / "Mapping" / "Input" / "Flowlists"


def check_flows_in_input_flowslists():
    assert CONTRIBUTE_DIR.is_dir()
    assert FLOWLISTS_DIR.is_dir()

    ecoinvent_df = pd.read_csv(FLOWLISTS_DIR / "ecoinventEFv3.7.csv")
    simapro_df = pd.read_csv(FLOWLISTS_DIR / "SimaProv9.4.csv")
    ecoinvent_set = {
        (row["FlowUUID"], row["Flowable"], row["Context"], row["Unit"])
        for _, row in ecoinvent_df.iterrows()
    }
    simapro_set = {
        (row["Flow UUID"], row["Flowable"], row["Context"], row["Unit"])
        for _, row in simapro_df.iterrows()
    }

    errors = []

    for filename in CONTRIBUTE_DIR.iterdir():
        if filename.suffix.lower() == ".csv":
            df = pd.read_csv(CONTRIBUTE_DIR / filename)

            input_simapro = {
                (
                    row["SourceFlowUUID"],
                    row["SourceFlowName"],
                    row["SourceFlowContext"],
                    row["SourceUnit"],
                )
                for _, row in df.iterrows()
            }
            input_ecoinvent = {
                (
                    row["TargetFlowUUID"],
                    row["TargetFlowName"],
                    row["TargetFlowContext"],
                    row["TargetUnit"],
                )
                for _, row in df.iterrows()
            }

            if input_simapro.difference(simapro_set):
                errors.append(
                    {
                        "message": "input flows not in simapro master list",
                        "filename": filename.name,
                        "extra flows": sorted(input_simapro.difference(simapro_set)),
                    }
                )
            if input_ecoinvent.difference(ecoinvent_set):
                errors.append(
                    {
                        "message": "input flows not in ecoinvent master list",
                        "filename": filename.name,
                        "extra flows": sorted(
                            input_ecoinvent.difference(ecoinvent_set)
                        ),
                    }
                )
    if errors:
        with open(
            LOGS_DIR / "check_flows_in_input_flowslists.json", "w", encoding="utf-8"
        ) as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)
        sys.exit(1)


if __name__ == "__main__":
    check_flows_in_input_flowslists()
