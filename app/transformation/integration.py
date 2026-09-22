import pandas as pd


STANDARD_COLUMNS = [
    "student_id",
    "student_name",
    "age",
    "city",
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
                "source": "api",
            }
        )

    return pd.DataFrame(
        standardized_records,
        columns=STANDARD_COLUMNS,
    )

def standardize_database(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize SQLite records
    into the common student schema.
    """

    required_columns = [
        "student_id",
        "student_name",
    ]

    missing_columns = (
        set(required_columns)
        - set(dataframe.columns)
    )

    if missing_columns:
        raise ValueError(
            "Database data is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    result = dataframe[
        [
            "student_id",
            "student_name",
        ]
    ].copy()

    # SQLite does not currently contain an age column.
    result["age"] = pd.NA
    result["city"] = pd.NA
    result["source"] = "database"

    return result[
        STANDARD_COLUMNS
    ].drop_duplicates()

def integrate_data(
    csv_data: pd.DataFrame,
    api_data: pd.DataFrame,
    database_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine standardized records from all data sources.
    """

    dataframes = [
        csv_data,
        api_data,
        database_data,
    ]

    integrated_data = pd.concat(
        dataframes,
        ignore_index=True,
    )

    return integrated_data[
        STANDARD_COLUMNS
    ]