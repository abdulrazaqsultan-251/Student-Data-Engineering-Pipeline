import pandas as pd


def transform_student_data(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Transform cleaned student data
    into the final standardized format.
    """

    data = dataframe.copy()

    # Normalize text fields
    text_columns = [
        "student_name",
        "city",
        "source",
    ]

    for column in text_columns:
        data[column] = (
            data[column]
            .astype("string")
            .str.strip()
        )

    # Normalize student ID
    data["student_id"] = pd.to_numeric(
        data["student_id"],
        errors="coerce",
    ).astype("Int64")

    # Normalize age
    data["age"] = pd.to_numeric(
        data["age"],
        errors="coerce",
    ).astype("Int64")

    # Keep a clear and consistent column order
    final_columns = [
        "student_id",
        "student_name",
        "age",
        "city",
        "source",
    ]

    return data[final_columns].reset_index(
        drop=True
    )