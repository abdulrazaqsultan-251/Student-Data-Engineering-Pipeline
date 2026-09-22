import pandas as pd


def clean_student_data(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Clean integrated student data.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        Clean records and rejected records.
    """

    data = dataframe.copy()

    rejected_records = []

    # ======================================================
    # Detect duplicate records
    # ======================================================

    duplicate_mask = data.duplicated(
        keep="first"
    )

    if duplicate_mask.any():
        rejected_records.append(
            data.loc[
                duplicate_mask
            ].assign(
                rejection_reason="Duplicate record"
            )
        )

        data = data.loc[
            ~duplicate_mask
        ].copy()

    # ======================================================
    # Validate student name
    # ======================================================

    invalid_name = (
        data["student_name"].isna()
        | data["student_name"]
        .astype(str)
        .str.strip()
        .eq("")
    )

    if invalid_name.any():
        rejected_records.append(
            data.loc[
                invalid_name
            ].assign(
                rejection_reason="Missing student_name"
            )
        )

        data = data.loc[
            ~invalid_name
        ].copy()

    # ======================================================
    # Validate age
    # ======================================================

    invalid_age = (
        data["age"].notna()
        & ~data["age"].between(
            16,
            80
        )
    )

    if invalid_age.any():
        rejected_records.append(
            data.loc[
                invalid_age
            ].assign(
                rejection_reason="Invalid age"
            )
        )

        data = data.loc[
            ~invalid_age
        ].copy()

    # ======================================================
    # Build rejected DataFrame
    # ======================================================

    if rejected_records:
        rejected = pd.concat(
            rejected_records,
            ignore_index=True,
        )
    else:
        rejected = pd.DataFrame(
            columns=[
                *data.columns,
                "rejection_reason",
            ]
        )

    return data, rejected