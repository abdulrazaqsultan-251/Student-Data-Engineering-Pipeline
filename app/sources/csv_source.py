from pathlib import Path

import pandas as pd


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "students.csv"
)


# ==========================================================
# CSV Extraction
# ==========================================================

def extract_csv(
    file_path: Path = CSV_FILE,
) -> pd.DataFrame:
    """
    Extract student data from a CSV file.

    Parameters
    ----------
    file_path:
        Path to the source CSV file.

    Returns
    -------
    pd.DataFrame
        Raw student data.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    dataframe = pd.read_csv(
        file_path
    )

    if dataframe.empty:
        raise ValueError(
            "CSV file contains no records."
        )

    return dataframe