from datetime import datetime, timezone
from pathlib import Path
import itertools

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


def add_unitary_conversion_when_missing(df: pd.DataFrame):
    missing = df.ConversionFactor.isnull()
    wrong_units = df.SourceUnit[missing] != df.TargetUnit[missing]
    if wrong_units.sum():
        name = "inconsistent-units-without-conversion.csv"
        (df[missing][wrong_units]).to_csv(LOGS_DIR / name, index=False)
        raise ValueError("Inconsistent units without conversion factor.\nSaved log to {}".format(LOGS_DIR / name))
    else:
        df.ConversionFactor[missing] = 1.0
        return df


def export_dataframe(df: pd.DataFrame, name: str, output_dir: Path = CONTRIBUTE_DIR) -> None:
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


def exclude_duplicates(df: pd.DataFrame, mapping_file: str = "SimaProv94-ecoinventEFv3.7.csv") -> pd.DataFrame:
    existing = pd.read_csv(MAPPED_FILES_DIR / mapping_file)[FIELDS]
    existing["FILTER_ME"] = True

    df = df.merge(existing, how="left", on=FIELDS)
    df = df[df["FILTER_ME"] != True]
    df = df.drop(columns=["FILTER_ME"])

    return df


def finish_notebook(
    df: pd.DataFrame,
    author: str,
    notebook_name: str,
    filename: str,
    output_dir: Path = CONTRIBUTE_DIR,
    default_match_condition: str = "=",
    mapping_file: str = "SimaProv94-ecoinventEFv3.7.csv",
    exclude_existing: bool = True,
) -> None:
    df = fix_names_after_merge(df=df)
    df = add_common_columns(
        df=df,
        author=author,
        notebook_name=notebook_name,
        default_match_condition=default_match_condition,
    )
    check_required_columns(df=df)
    if exclude_existing:
        df = exclude_duplicates(df=df, mapping_file=mapping_file)
    export_dataframe(df=df, name=filename, output_dir=output_dir)


def expand_simapro_context(df: pd.DataFrame, kind: str = "air"):
    if kind == "air":
        df = df[df.Context == "Airborne emissions"]
        CONTEXTS = [
            "Emissions to air/(unspecified)",
            "Emissions to air/indoor",
            "Emissions to air/high. pop.",
            "Emissions to air/low. pop.",
            "Emissions to air/low. pop., long-term",
            "Emissions to air/stratosphere + troposphere",
            "Emissions to air/stratosphere",
        ]
        df = df.rename(columns={"Context": "ParentContext"})
        expander = pd.DataFrame(zip(CONTEXTS, itertools.repeat("Airborne emissions")), columns=["Context", "ParentContext"])
        df = df.merge(expander, how="outer", on="ParentContext")
        return df
    elif kind == "water":
        df = df[df.Context == "Waterborne emissions"]
        CONTEXTS = [
            "Emissions to water/fossilwater",
            "Emissions to water/groundwater",
            "Emissions to water/groundwater, long-term",
            "Emissions to water/ocean",
            "Emissions to water/lake",
            "Emissions to water/river",
            "Emissions to water/river, long-term",
            "Emissions to water/(unspecified)"
        ]
        df = df.rename(columns={"Context": "ParentContext"})
        expander = pd.DataFrame(zip(CONTEXTS, itertools.repeat("Waterborne emissions")), columns=["Context", "ParentContext"])
        df = df.merge(expander, how="outer", on="ParentContext")
        return df
    elif kind == "soil":
        df = df[df.Context == "Emissions to soil"]
        CONTEXTS = [
            "Emissions to soil/agricultural",
            "Emissions to soil/forestry",
            "Emissions to soil/industrial",
            "Emissions to soil/urban, non industrial",
            "Emissions to soil/(unspecified)",
        ]
        df = df.rename(columns={"Context": "ParentContext"})
        expander = pd.DataFrame(zip(CONTEXTS, itertools.repeat("Emissions to soil")), columns=["Context", "ParentContext"])
        df = df.merge(expander, how="outer", on="ParentContext")
        return df
    elif kind == "resources":
        df = df[df.Context == "Raw materials"]
        CONTEXTS = [
            'Resources/land',
            'Resources/(unspecified)',
            'Resources/biotic',
            'Resources/in ground',
            'Resources/in air',
            'Resources/in water',
            'Resources/fossil well',
        ]
        df = df.rename(columns={"Context": "ParentContext"})
        expander = pd.DataFrame(zip(CONTEXTS, itertools.repeat("Raw materials")), columns=["Context", "ParentContext"])
        df = df.merge(expander, how="outer", on="ParentContext")
        return df
    else:
        raise ValueError


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
    elif kind == "water":
        expander = pd.DataFrame([
            ("Emissions to water/fossilwater", "water/fossil well"),
            ("Emissions to water/groundwater", "water/ground-"),
            ("Emissions to water/groundwater, long-term", "water/ground-, long-term"),
            ("Emissions to water/ocean", "water/ocean"),
            ("Emissions to water/lake", "water/surface water"),
            ("Emissions to water/river", "water/surface water"),
            ("Emissions to water/river, long-term", "water/surface water"),
            ("Emissions to water/(unspecified)", "water/unspecified"),
        ], columns=["Context", label])
        return df.merge(expander, how="left", on="Context")
    elif kind == "soil":
        expander = pd.DataFrame([
            ('Emissions to soil/(unspecified)', 'soil/unspecified'),
            ('Emissions to soil/agricultural', 'soil/agricultural'),
            ('Emissions to soil/forestry', 'soil/forestry'),
            ('Emissions to soil/industrial', 'soil/industrial'),
            ('Emissions to soil/urban, non industrial', 'soil/industrial'),
        ], columns=["Context", label])
        return df.merge(expander, how="left", on="Context")
    elif kind == "resources":
        expander = pd.DataFrame([
            ('Resources/(unspecified)', 'natural resource/unspecified'),
            ('Resources/biotic', 'natural resource/biotic'),
            ('Resources/fossil well', 'natural resource/in water'),
            ('Resources/in air', 'natural resource/in air'),
            ('Resources/in ground', 'natural resource/in ground'),
            ('Resources/in water', 'natural resource/in water'),
            ('Resources/land', 'natural resource/land'),
        ], columns=["Context", label])
        return df.merge(expander, how="left", on="Context")
    else:
        raise ValueError
