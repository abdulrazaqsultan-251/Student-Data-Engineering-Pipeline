from typing import Iterable

import pandas as pd


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: Iterable[str],
) -> None:
    """
    Validate that a DataFrame contains all required columns.
    """

    if dataframe.empty:
        raise ValueError(
            "Dataset is empty."
        )

    actual_columns = set(
        dataframe.columns
    )

    missing_columns = (
        set(required_columns)
        - actual_columns
    )

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            f"{sorted(missing_columns)}"
        )


def validate_student_source(
    dataframe: pd.DataFrame,
) -> None:
    """
    Validate the basic schema of a student source.
    """

    required_columns = {
        "student_id",
        "student_name",
        "age",
        "major",
        "city",
    }

    validate_required_columns(
        dataframe,
        required_columns,
    )

def validate_final_data(
    dataframe: pd.DataFrame,
) -> None:
    """
    Validate the final transformed dataset
    before loading it to the processed output.
    """

    required_columns = {
        "student_id",
        "student_name",
        "age",
        "city",
        "source",
    }

    validate_required_columns(
        dataframe,
        required_columns,
    )

    # Student ID must exist
    if dataframe["student_id"].isna().any():
        raise ValueError(
            "Final dataset contains missing student_id values."
        )

    # Student name must exist
    if (
        dataframe["student_name"]
        .isna()
        .any()
    ):
        raise ValueError(
            "Final dataset contains missing student_name values."
        )

    # Age is optional because the SQLite source
    # does not provide age.
    invalid_age = (
        dataframe["age"].notna()
        & ~dataframe["age"].between(16, 80)
    )

    if invalid_age.any():
        raise ValueError(
            "Final dataset contains invalid age values."
        )

        # Validate GPA when available
    if "gpa" in dataframe.columns:
        invalid_gpa = dataframe[
            dataframe["gpa"].notna()
            & ~dataframe["gpa"].between(0, 4)
        ]

        if not invalid_gpa.empty:
            raise ValueError(
                "Invalid GPA values found. "
                "GPA must be between 0 and 4."
            )

    # Validate attendance when available
    if "attendance" in dataframe.columns:
        invalid_attendance = dataframe[
            dataframe["attendance"].notna()
            & ~dataframe["attendance"].between(0, 100)
        ]

        if not invalid_attendance.empty:
            raise ValueError(
                "Invalid attendance values found. "
                "Attendance must be between 0 and 100."
            )

    # Source must identify the origin of each record
    allowed_sources = {
    "csv",
    "api",
    "database",
    "mongodb",
    }

    invalid_sources = (
        ~dataframe["source"].isin(
            allowed_sources
        )
    )

    if invalid_sources.any():
        raise ValueError(
            "Final dataset contains invalid source values."
        )

    # The final dataset must not contain
    # exact duplicate records.
    duplicate_columns = [
        "student_id",
        "student_name",
        "age",
        "city",
        "gpa",
        "attendance",
        "source",
    ]

    if dataframe.duplicated(
        subset=duplicate_columns
    ).any():
        raise ValueError(
            "Duplicate records found in final data."
        )
