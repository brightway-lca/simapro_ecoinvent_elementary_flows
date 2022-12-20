from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent.resolve()
CONTRIBUTE_DIR = BASE_DIR / "Contribute"
MAPPED_FILES_DIR = BASE_DIR / "Mapping" / "Output" / "Mapped_files"


def add_mappings():
    assert CONTRIBUTE_DIR.is_dir()
    assert MAPPED_FILES_DIR.is_dir()

    pd.concat(
        objs=(
            [pd.read_csv(MAPPED_FILES_DIR / "SimaProv94-ecoinventEFv3.7.csv")]
            + [
                pd.read_csv(CONTRIBUTE_DIR / filename)
                for filename in CONTRIBUTE_DIR.iterdir()
                if filename.suffix.lower() == ".csv"
            ]
        )
    ).to_csv(MAPPED_FILES_DIR / "SimaProv94-ecoinventEFv3.7.csv", index=False)


def archive_contributions():
    for file in CONTRIBUTE_DIR.glob("*.csv"):
        file.rename(CONTRIBUTE_DIR / "Archive" / file.name)


if __name__ == "__main__":
    add_mappings()
    archive_contributions()
