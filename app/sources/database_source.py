from pathlib import Path
import logging
import sqlite3


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_FILE = (
    PROJECT_ROOT / "database" / "students.db"
)

SCHEMA_FILE = (
    PROJECT_ROOT / "database" / "schema.sql"
)

SEED_FILE = (
    PROJECT_ROOT / "database" / "seed.sql"
)


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# Database Connection
# ==========================================================

def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.
    """

    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    # Enable foreign key constraints
    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    return connection


# ==========================================================
# Initialize Database
# ==========================================================

def initialize_database() -> None:
    """
    Create the SQLite database and execute the database schema.
    """

    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(
            f"Schema file not found: {SCHEMA_FILE}"
        )

    schema_sql = SCHEMA_FILE.read_text(
        encoding="utf-8"
    )

    if not schema_sql.strip():
        raise ValueError(
            "Schema file is empty."
        )

    connection = get_connection()

    try:
        connection.executescript(
            schema_sql
        )

        connection.commit()

        logger.info(
            "Database initialized successfully: %s",
            DATABASE_FILE
        )

    except sqlite3.Error as exc:
        connection.rollback()

        logger.exception(
            "Database initialization failed."
        )

        raise RuntimeError(
            "Failed to initialize database."
        ) from exc

    finally:
        connection.close()


# ==========================================================
# Verify Tables
# ==========================================================

def get_table_names() -> list[str]:
    """
    Return the list of tables available in the database.
    """

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name;
            """
        )

        tables = [
            row[0]
            for row in cursor.fetchall()
        ]

        return tables

    finally:
        connection.close()


def validate_database_schema() -> None:
    """
    Verify that all required tables exist.
    """

    required_tables = {
        "students",
        "instructors",
        "courses",
        "enrollments",
        "assessments",
    }

    existing_tables = set(
        get_table_names()
    )

    missing_tables = (
        required_tables - existing_tables
    )

    if missing_tables:
        raise ValueError(
            "Missing database tables: "
            f"{sorted(missing_tables)}"
        )

    logger.info(
        "Database schema validation passed."
    )

# =========================================================
# Seed Database
# =========================================================
def seed_database() -> None:
    """
    Insert initial data into the SQLite database
    only when the database is empty.
    """

    if not SEED_FILE.exists():
        raise FileNotFoundError(
            f"Seed file not found: {SEED_FILE}"
        )

    seed_sql = SEED_FILE.read_text(
        encoding="utf-8"
    )

    if not seed_sql.strip():
        raise ValueError(
            "Seed file is empty."
        )

    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM students"
        )

        student_count = cursor.fetchone()[0]

        if student_count > 0:
            logger.info(
                "Database already contains data. "
                "Skipping seed operation."
            )
            return

        connection.executescript(
            seed_sql
        )

        connection.commit()

        logger.info(
            "Database seed data inserted successfully."
        )

    except sqlite3.Error as exc:

        connection.rollback()

        logger.exception(
            "Database seeding failed."
        )

        raise RuntimeError(
            "Failed to insert seed data."
        ) from exc

    finally:
        connection.close()

# =========================================================
# Get Table Counts
# =========================================================
def get_table_counts() -> dict[str, int]:
    """
    Return the number of records in each database table.
    """

    tables = [
        "students",
        "instructors",
        "courses",
        "enrollments",
        "assessments",
    ]

    connection = get_connection()

    try:
        counts = {}

        for table in tables:
            cursor = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            )

            counts[table] = cursor.fetchone()[0]

        return counts

    finally:
        connection.close()



# ==========================================================
# Validate Seed Data
# ==========================================================
def validate_seed_data() -> None:
    """
    Validate the expected number of records
    in the database tables.
    """

    expected_counts = {
        "students": 8,
        "instructors": 4,
        "courses": 5,
        "enrollments": 13,
        "assessments": 26,
    }

    actual_counts = get_table_counts()

    for table, expected_count in expected_counts.items():

        actual_count = actual_counts[table]

        if actual_count != expected_count:
            raise ValueError(
                f"Unexpected record count in {table}: "
                f"expected {expected_count}, "
                f"got {actual_count}"
            )

    logger.info(
        "Seed data validation passed."
    )

# ==========================================================
# Database Setup
# ==========================================================

def setup_database() -> None:
    """
    Initialize, seed, and validate the SQLite database.
    """

    initialize_database()

    validate_database_schema()

    seed_database()

    validate_seed_data()

    logger.info(
        "Database setup completed successfully."
    )
# =========================================================
# Database Extraction
# =========================================================

def extract_database():
    """
    Extract integrated student course data from SQLite.

    Returns
    -------
    pandas.DataFrame
        Student, course, instructor, enrollment,
        and assessment data.
    """

    import pandas as pd

    query = """
        SELECT
            s.student_id,
            s.full_name AS student_name,
            c.course_id,
            c.course_name,
            i.instructor_id,
            i.full_name AS instructor_name,
            e.enrollment_date,
            e.semester,
            a.assessment_type,
            a.score
        FROM enrollments AS e
        JOIN students AS s
            ON e.student_id = s.student_id
        JOIN courses AS c
            ON e.course_id = c.course_id
        LEFT JOIN instructors AS i
            ON c.instructor_id = i.instructor_id
        LEFT JOIN assessments AS a
            ON a.student_id = e.student_id
            AND a.course_id = e.course_id
        ORDER BY
            s.student_id,
            c.course_id,
            a.assessment_type;
    """

    connection = get_connection()

    try:
        dataframe = pd.read_sql_query(
            query,
            connection
        )

    except Exception as exc:
        logger.exception(
            "Database extraction failed."
        )

        raise RuntimeError(
            "Failed to extract data from database."
        ) from exc

    finally:
        connection.close()

    if dataframe.empty:
        raise ValueError(
            "Database extraction returned no records."
        )

    logger.info(
        "Database extraction completed: %d records.",
        len(dataframe)
    )

    return dataframe