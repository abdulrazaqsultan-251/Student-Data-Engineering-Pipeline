import pandas as pd

from app.output.csv_writer import (
    FINAL_DATASET_FILE,
)
from app.sources.api_source import extract_api
from app.sources.csv_source import extract_csv
from app.sources.database_source import (
    extract_database,
    setup_database,
)
from app.transformation.cleaner import (
    clean_student_data,
)
from app.transformation.integration import (
    integrate_data,
    standardize_api,
    standardize_csv,
    standardize_database,
)
from app.transformation.transformer import (
    transform_student_data,
)
from app.validation.quality import (
    validate_final_data,
    validate_student_source,
)


def build_integrated_data():
    """
    Build the integrated dataset used by tests.
    """

    csv_data = standardize_csv(
        extract_csv()
    )

    api_data = standardize_api(
        extract_api()
    )

    database_data = standardize_database(
        extract_database()
    )

    return integrate_data(
        csv_data,
        api_data,
        database_data,
    )


def test_csv_load():
    """Test CSV extraction."""

    dataframe = extract_csv()

    assert isinstance(
        dataframe,
        pd.DataFrame,
    )

    assert len(dataframe) > 0

    validate_student_source(
        dataframe
    )


def test_api_connection():
    """Test REST API extraction."""

    records = extract_api()

    assert isinstance(
        records,
        list,
    )

    assert len(records) > 0


def test_sqlite_extraction():
    """Test SQLite extraction."""

    setup_database()

    dataframe = extract_database()

    assert isinstance(
        dataframe,
        pd.DataFrame,
    )

    assert len(dataframe) > 0


def test_duplicate_removal():
    """Test duplicate record removal."""

    dataframe = pd.DataFrame(
        {
            "student_id": [1001, 1001],
            "student_name": [
                "Ahmed Ali",
                "Ahmed Ali",
            ],
            "age": [21, 21],
            "city": ["Sanaa", "Sanaa"],
            "source": ["csv", "csv"],
        }
    )

    clean, rejected = (
        clean_student_data(dataframe)
    )

    assert len(clean) == 1
    assert len(rejected) == 1
    assert (
        rejected.iloc[0]["rejection_reason"]
        == "Duplicate record"
    )


def test_missing_value_rejection():
    """Test missing student name rejection."""

    dataframe = pd.DataFrame(
        {
            "student_id": [1001],
            "student_name": [None],
            "age": [21],
            "city": ["Sanaa"],
            "source": ["csv"],
        }
    )

    clean, rejected = (
        clean_student_data(dataframe)
    )

    assert len(clean) == 0
    assert len(rejected) == 1
    assert (
        rejected.iloc[0]["rejection_reason"]
        == "Missing student_name"
    )


def test_invalid_record_rejection():
    """Test invalid age rejection."""

    dataframe = pd.DataFrame(
        {
            "student_id": [1001],
            "student_name": ["Ahmed Ali"],
            "age": [-21],
            "city": ["Sanaa"],
            "source": ["csv"],
        }
    )

    clean, rejected = (
        clean_student_data(dataframe)
    )

    assert len(clean) == 0
    assert len(rejected) == 1
    assert (
        rejected.iloc[0]["rejection_reason"]
        == "Invalid age"
    )


def test_integration():
    """Test multi-source integration."""

    dataframe = build_integrated_data()

    assert len(dataframe) == 41

    assert set(dataframe["source"]) == {
        "csv",
        "api",
        "database",
    }


def test_transformation():
    """Test final data transformation."""

    integrated = build_integrated_data()

    clean, _ = clean_student_data(
        integrated
    )

    transformed = transform_student_data(
        clean
    )

    assert len(transformed) == 37

    assert list(
        transformed.columns
    ) == [
        "student_id",
        "student_name",
        "age",
        "city",
        "source",
    ]


def test_final_validation():
    """Test final dataset validation."""

    integrated = build_integrated_data()

    clean, _ = clean_student_data(
        integrated
    )

    transformed = transform_student_data(
        clean
    )

    validate_final_data(
        transformed
    )


def test_final_dataset_exists():
    """Test final dataset creation."""

    assert FINAL_DATASET_FILE.exists()

    dataframe = pd.read_csv(
        FINAL_DATASET_FILE
    )

    assert len(dataframe) == 37

    assert set(
        dataframe.columns
    ) == {
        "student_id",
        "student_name",
        "age",
        "city",
        "source",
    }