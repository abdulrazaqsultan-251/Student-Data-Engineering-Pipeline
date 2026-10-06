import pandas as pd


def transform_student_data(dataframe):
    data = dataframe.copy()

    # Clean text columns
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

    # Convert numeric columns
    data["student_id"] = pd.to_numeric(
        data["student_id"],
        errors="coerce",
    ).astype("Int64")

    data["age"] = pd.to_numeric(
        data["age"],
        errors="coerce",
    ).astype("Int64")

    data["gpa"] = pd.to_numeric(
        data["gpa"],
        errors="coerce",
    )

    data["attendance"] = pd.to_numeric(
        data["attendance"],
        errors="coerce",
    )

    # Keep the complete standardized structure
    final_columns = [
        "student_id",
        "student_name",
        "age",
        "city",
        "gpa",
        "attendance",
        "skills",
        "source",
    ]

    return data[final_columns].reset_index(drop=True)