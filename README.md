# Student Data Engineering Pipeline

## 1. Project Overview

This project implements a multi-source data engineering pipeline for student data.

The pipeline extracts data from three different sources:

- CSV file
- REST API
- SQLite database

The extracted data is validated, standardized, integrated, cleaned, transformed, validated again, and finally saved as a processed dataset.

The project also keeps rejected records separately and records pipeline execution details in a log file.

---

## 2. Project Architecture

```text
CSV Source ───────────┐
                      │
REST API Source ──────┼──> Extract
                      │
SQLite Database ──────┘
                             │
                             ▼
                         Validate
                             │
                             ▼
                           Clean
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
              Clean Records    Rejected Records
                    │                 │
                    ▼                 ▼
                 Integrate       rejected_records.csv
                    │
                    ▼
                 Transform
                    │
                    ▼
              Final Validation
                    │
                    ▼
             final_dataset.csv
```

The project is organized into separate modules for sources, transformation,
validation, output, and logging.

---

## 3. Project Structure

```text
student_data_pipeline/
│
├── app/
│   ├── sources/
│   │   ├── csv_source.py
│   │   ├── api_source.py
│   │   └── database_source.py
│   │
│   ├── transformation/
│   │   ├── cleaner.py
│   │   ├── transformer.py
│   │   └── integration.py
│   │
│   ├── validation/
│   │   └── quality.py
│   │
│   ├── output/
│   │   └── csv_writer.py
│   │
│   └── utils/
│       └── logger.py
│
├── data/
│   ├── raw/
│   │   └── students.csv
│   │
│   ├── processed/
│   │   └── final_dataset.csv
│   │
│   └── rejected/
│       └── rejected_records.csv
│
├── database/
│   ├── students.db
│   ├── schema.sql
│   ├── seed.sql
│   └── queries.sql
│
├── logs/
│   └── pipeline.log
│
├── tests/
│   └── test_pipeline.py
│
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 4. Data Sources

### 4.1 CSV

The CSV source contains student information including:

- student ID
- student name
- age
- major
- city

File:

```text
data/raw/students.csv
```

### 4.2 REST API

The project uses a REST API as an external data source.

The API records are standardized into the common student schema before integration.

Only the required fields are extracted from the API response.

### 4.3 SQLite Database

The project uses SQLite as the relational database source.

The database contains five tables:

1. students
2. instructors
3. courses
4. enrollments
5. assessments

The database source uses SQL JOIN operations to extract integrated student,
course, instructor, enrollment, and assessment information.

---

## 5. ETL Pipeline

The pipeline follows these stages:

### Extract

Data is extracted from:

- CSV
- REST API
- SQLite

### Validate

Source data is checked against the expected structure.

### Clean

The cleaning stage handles:

- duplicate records
- missing student names
- invalid ages

Invalid records are removed from the clean dataset and stored separately.

### Integrate

The three standardized sources are combined into a common structure.

Each record keeps its source through the `source` field.

### Transform

The transformation stage standardizes:

- text values
- student IDs
- age values
- column ordering

### Final Validation

The final dataset is checked for:

- required columns
- missing student IDs
- missing student names
- invalid ages
- invalid source values
- duplicate records

### Load

The valid final dataset is saved to:

```text
data/processed/final_dataset.csv
```

Rejected records are saved to:

```text
data/rejected/rejected_records.csv
```

---

## 6. Data Quality

The current input data contains intentionally invalid records for demonstrating
data quality processing.

The current pipeline processes:

```text
CSV records        : 13
API records        : 20
SQLite records     : 26
Integrated records : 41
Clean records      : 37
Rejected records   : 4
```

The rejected records include:

- one duplicate record
- one record with a missing student name
- two records with invalid ages

Rejected records are stored with a `rejection_reason` column.

---

## 7. Installation

Create and activate a Python virtual environment if desired.

Install the required packages:

```powershell
pip install -r requirements.txt
```

The project uses Python 3.11.

---

## 8. Running the Pipeline

Run the complete pipeline from the project root:

```powershell
python main.py
```

The pipeline performs all stages automatically.

Expected result:

```text
Pipeline completed successfully.
==============================
Final records    : 37
Rejected records : 4
```

---

## 9. Running Tests

Run the test suite using:

```powershell
pytest -v
```

The project currently contains tests for:

- CSV extraction
- API extraction
- SQLite extraction
- duplicate removal
- missing value rejection
- invalid record rejection
- data integration
- transformation
- final validation
- final dataset creation

Current test result:

```text
10 passed
```

---

## 10. Output Files

### Final Dataset

```text
data/processed/final_dataset.csv
```

Contains the cleaned and transformed records.

### Rejected Records

```text
data/rejected/rejected_records.csv
```

Contains records rejected during the cleaning stage together with the reason
for rejection.

### Pipeline Log

```text
logs/pipeline.log
```

Contains execution information for the different pipeline stages.

---

## 11. Technologies

- Python
- Pandas
- Requests
- SQLite
- SQL
- Pytest
- Python Logging
