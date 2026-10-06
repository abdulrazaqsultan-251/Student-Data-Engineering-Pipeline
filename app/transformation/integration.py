from unittest import result

import pandas as pd


STANDARD_COLUMNS = [
    "student_id",
    "student_name",
    "age",
    "city",
    "gpa",
    "attendance",
    "skills",
    "source",
]


def standardize_csv(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize the CSV student data.
    """

    required_columns = [
        "student_id",
        "student_name",
        "age",
        "city",
    ]

    missing_columns = (
        set(required_columns)
        - set(dataframe.columns)
    )

    if missing_columns:
        raise ValueError(
            "CSV is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    result = dataframe[
        required_columns
    ].copy()

    result["source"] = "csv"
    result["gpa"] = pd.NA
    result["attendance"] = pd.NA
    result["skills"] = [[] for _ in range(len(result))]

    return result[
        STANDARD_COLUMNS
    ]


def standardize_api(
    records: list[dict],
) -> pd.DataFrame:
    """
    Standardize raw API records
    into the common student schema.
    """

    if not records:
        raise ValueError(
            "API records are empty."
        )

    standardized_records = []

    for record in records:
        address = record.get("address", {})

        standardized_records.append(
            {
                "student_id": record.get("id"),
                "student_name": (
                    f"{record.get('firstName', '')} "
                    f"{record.get('lastName', '')}"
                ).strip(),
                "age": record.get("age"),
                "city": address.get("city"),
                "gpa": pd.NA,
                "attendance": pd.NA,
                "skills": [],
                "source": "api",
                
            }
        )

    return pd.DataFrame(
        standardized_records,
        columns=STANDARD_COLUMNS,
    )

def standardize_database(dataframe: pd.DataFrame) -> pd.DataFrame:
    required_columns = [
        "student_id",
        "student_name",
    ]

    missing_columns = set(required_columns) - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Database data is missing required columns: "
            f"{missing_columns}"
        )

    result = dataframe[
        ["student_id", "student_name"]
    ].copy()

    # Remove duplicate database records
    # before adding list-type columns.
    result = result.drop_duplicates()

    result["age"] = pd.NA
    result["city"] = pd.NA
    result["gpa"] = pd.NA
    result["attendance"] = pd.NA
    result["skills"] = [[] for _ in range(len(result))]
    result["source"] = "database"

    return result[STANDARD_COLUMNS]


def standardize_mongodb(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize MongoDB records
    into the common student schema.
    """

    required_columns = [
        "student_id",
        "student_name",
        "age",
        "city",
        "gpa",
        "attendance",
        "skills",
    ]

    missing_columns = (
        set(required_columns)
        - set(dataframe.columns)
    )

    if missing_columns:
        raise ValueError(
            "MongoDB data is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    result = dataframe[
        required_columns
    ].copy()

    result["source"] = "mongodb"

    return result[
        STANDARD_COLUMNS
    ]


def integrate_data(
    csv_data: pd.DataFrame,
    api_data: pd.DataFrame,
    database_data: pd.DataFrame,
    mongodb_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine standardized records from all data sources.
    """

    dataframes = [
        csv_data,
        api_data,
        database_data,
        mongodb_data,
    ]
    integrated_data = pd.concat(
        dataframes,
        ignore_index=True,
    )

    return integrated_data[
        STANDARD_COLUMNS
    ]