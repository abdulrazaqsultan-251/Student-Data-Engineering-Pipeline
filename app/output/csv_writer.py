from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REJECTED_DIR = PROJECT_ROOT / "data" / "rejected"

FINAL_DATASET_FILE = (
    PROCESSED_DIR / "final_dataset.csv"
)

REJECTED_RECORDS_FILE = (
    REJECTED_DIR / "rejected_records.csv"
)


def save_final_dataset(
    dataframe: pd.DataFrame,
    file_path: Path = FINAL_DATASET_FILE,
) -> None:
    """
    Save the final processed dataset as CSV.
    """

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig",
    )


def save_rejected_records(
    dataframe: pd.DataFrame,
    file_path: Path = REJECTED_RECORDS_FILE,
) -> None:
    """
    Save rejected records as CSV.
    """

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig",
    )