from datetime import datetime, timezone
from pathlib import Path
import itertools

import pandas as pd


output_dir = (Path.cwd().parent / "Contribute").resolve()


def fix_names_after_merge(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "Flow UUID": "SourceFlowUUID",
        "FlowUUID": "TargetFlowUUID",  # Incorrect column header in provided ecoinvent data
        "Flowable_x": "SourceFlowName",
        "Flowable_y": "TargetFlowName",
        "Unit_x": "SourceUnit",
        "Unit_y": "TargetUnit",
        "Context_x": "SourceFlowContext",
        "Context_y": "TargetFlowContext",
    }
    return df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})


def add_common_columns(
    df: pd.DataFrame,
    author: str,
    notebook_name: str,
    default_match_condition: str = "=",
) -> pd.DataFrame:
    df["SourceListName"] = "SimaPro9.4"
    df["TargetListName"] = "ecoinventEFv3.7"
    df["MatchCondition"] = default_match_condition
    df["Mapper"] = author
    df["MemoMapper"] = f"Automated match. Notebook: {notebook_name}"
    df["MemoSource"] = ""
    df["MemoTarget"] = ""
    df["MemoVerifier"] = ""
    df["LastUpdated"] = datetime.now(timezone.utc).astimezone().isoformat()
    df["Verifier"] = ""
    return df


def check_required_columns(df: pd.DataFrame) -> None:
    expected = set(
        [
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
        ]
    )
    given = set(df.columns)
    difference = expected.difference(given)
    if difference:
        print("Missing the following required columns:", difference)


def export_dataframe(df: pd.DataFrame, name: str, output_dir: Path) -> None:
    SPEC_COLUMNS = [
        "SourceListName",
        "SourceFlowName",
        "SourceFlowUUID",
        "SourceFlowContext",
        "SourceUnit",
        "MatchCondition",
        "ConversionFactor",
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
    ]

    df = df[[col for col in SPEC_COLUMNS if col in df.columns]]

    if not name.lower().endswith(".csv"):
        name += ".csv"

    df.to_csv(output_dir / name, index=False)


def finish_notebook(
    df: pd.DataFrame,
    author: str,
    notebook_name: str,
    filename: str,
    output_dir: Path = output_dir,
    default_match_condition: str = "=",
) -> None:
    df = fix_names_after_merge(df=df)
    df = add_common_columns(
        df=df,
        author=author,
        notebook_name=notebook_name,
        default_match_condition=default_match_condition,
    )
    check_required_columns(df=df)
    export_dataframe(df=df, name=filename, output_dir=output_dir)


def expand_simapro_context(df: pd.DataFrame, kind: str = "air"):
    if kind == "air":
        df = df[df.Context == "Airborne emissions"]
        AIR_CONTEXTS = [
            "Emissions to air/(unspecified)",
            "Emissions to air/indoor",
            "Emissions to air/high. pop.",
            "Emissions to air/low. pop.",
            "Emissions to air/low. pop., long-term",
            "Emissions to air/stratosphere + troposphere",
            "Emissions to air/stratosphere",
        ]
        df = df.rename(columns={"Context": "ParentContext"})
        expander = pd.DataFrame(zip(AIR_CONTEXTS, itertools.repeat("Airborne emissions")), columns=["Context", "ParentContext"])
        df = df.merge(expander, how="outer", on="ParentContext")
        return df


def add_ecoinvent_context_column(df: pd.DataFrame, label: str, kind: str = "air"):
    if kind == "air":
        expander = pd.DataFrame([
            ("Emissions to air/(unspecified)", "air/unspecified"),
            ("Emissions to air/high. pop.", "air/urban air close to ground"),
            ("Emissions to air/indoor", "air/indoor"),
            ("Emissions to air/low. pop.", "air/non-urban air or from high stacks"),
            ("Emissions to air/low. pop., long-term", "air/low population density, long-term"),
            ("Emissions to air/stratosphere + troposphere", "air/lower stratosphere + upper troposphere"),
            ("Emissions to air/stratosphere", "air/lower stratosphere + upper troposphere"),
        ], columns=["Context", label])
        return df.merge(expander, how="left", on="Context")
