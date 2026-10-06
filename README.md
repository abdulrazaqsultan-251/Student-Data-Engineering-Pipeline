# Student Data Engineering Pipeline

## 1. Project Overview

This project implements a multi-source data engineering pipeline for student data.

The pipeline extracts data from four different sources:

- CSV file
- REST API
- SQLite database
- MongoDB database

The extracted data is validated, standardized, integrated, cleaned, transformed, validated again, and finally saved as processed data.

The project also keeps rejected records separately and records pipeline execution details in a log file.

The final processed dataset is written to both CSV and MongoDB.

---

## 2. Project Architecture

```text
CSV Source ───────────┐
                      │
REST API Source ──────┤
                      │
SQLite Database ──────┤
                      │
MongoDB Database ─────┘
                      │
                      ▼
                   Extract
                      │
                      ▼
             Source Validation
                      │
                      ▼
                Standardize
                      │
                      ▼
                 Integrate
                      │
                      ▼
                   Clean
                  /     \\
                 /       \\
                ▼         ▼
       Clean Records   Rejected Records
                │         │
                │         ▼
                │    rejected_records.csv
                │
                ▼
             Transform
                │
                ▼
          Final Validation
                │
           ┌────┴────┐
           ▼         ▼
       CSV Output  MongoDB Output
           │         │
           ▼         ▼
   final_dataset.csv
   processed_students
```

The project is organized into separate modules for data sources, transformation, validation, output, and logging.

---

## 3. Project Structure

```text
student_data_pipeline/
│
├── app/
│   ├── sources/
│   │   ├── csv_source.py
│   │   ├── api_source.py
│   │   ├── database_source.py
│   │   └── mongodb_source.py
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
│   │   ├── csv_writer.py
│   │   └── mongodb_writer.py
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
├── docs/
│   ├── 01_project_overview.md
│   ├── 02_data_sources.md
│   ├── 03_mongodb_pipeline.md
│   ├── data_dictionary.md
│   ├── pipeline.md
│   ├── schema.md
│   └── validation_rules.md
│
├── logs/
│   └── pipeline.log
│
├── scripts/
│   └── prepare_mongodb_students.py
│
├── tests/
│   ├── test_mong.py
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

The database source uses SQL JOIN operations to extract integrated student, course, instructor, enrollment, and assessment information.

### 4.4 MongoDB

The project uses MongoDB as a NoSQL document database source.

Database:

```text
university_ai
```

Source collection:

```text
students
```

The MongoDB documents contain nested fields such as:

- `address`
- `academic`
- `skills`

The nested academic fields are standardized into the common pipeline schema:

```text
academic.gpa        → gpa
academic.attendance → attendance
skills              → skills
```

MongoDB extraction is implemented in:

```text
app/sources/mongodb_source.py
```

MongoDB data preparation is implemented in:

```text
scripts/prepare_mongodb_students.py
```

---

## 5. ETL Pipeline

The pipeline follows these stages:

### Extract

Data is extracted from:

- CSV
- REST API
- SQLite
- MongoDB

### Source Validation

Each source is checked against the expected structure before integration.

### Standardize

Data from the different sources is converted into a common schema:

```text
student_id
student_name
age
city
gpa
attendance
skills
source
```

Each record keeps its original source through the `source` field.

### Integrate

The four standardized sources are combined into a single dataset.

Current integrated record count:

```text
50
```

### Clean

The cleaning stage handles:

- duplicate records
- missing student names
- invalid ages

Invalid records are removed from the clean dataset and stored separately.

### Transform

The transformation stage standardizes:

- text values
- student IDs
- age values
- GPA values
- attendance values
- column ordering

### Final Validation

The final dataset is checked for:

- required columns
- missing student IDs
- missing student names
- invalid ages
- invalid GPA values
- invalid attendance values
- invalid source values
- duplicate records

### Load

The valid final dataset is saved to:

```text
data/processed/final_dataset.csv
```

The same processed records are also written to MongoDB:

```text
Database: university_ai
Collection: processed_students
```

Rejected records are saved to:

```text
data/rejected/rejected_records.csv
```

---

## 6. Data Quality

The current input data contains intentionally invalid records for demonstrating data quality processing.

The current pipeline processes:

```text
CSV records       : 13
API records       : 20
SQLite records    : 26
MongoDB records   : 9
Integrated records: 50
Rejected records  : 4
Final records     : 46
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

MongoDB is required for the MongoDB source and output stages.

The project currently uses MongoDB running locally on:

```text
mongodb://localhost:27017/
```

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
Final records    : 46
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
- MongoDB extraction
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

Contains the cleaned, transformed, and validated student records.

### Rejected Records

```text
data/rejected/rejected_records.csv
```

Contains records rejected during the cleaning stage together with the reason for rejection.

### MongoDB Processed Data

```text
Database: university_ai
Collection: processed_students
```

Contains the processed student records written by the pipeline.

### Pipeline Log

```text
logs/pipeline.log
```

Contains execution information for the different pipeline stages.

---

## 11. Documentation

Additional project documentation is available in the `docs/` directory:

- `01_project_overview.md` — project overview
- `02_data_sources.md` — source descriptions
- `03_mongodb_pipeline.md` — MongoDB preparation and extraction
- `data_dictionary.md` — standardized data fields
- `schema.md` — database and MongoDB schema
- `pipeline.md` — pipeline stages and flow
- `validation_rules.md` — data quality and validation rules

---

## 12. Technologies

- Python 3.11
- Pandas
- Requests
- PyMongo
- SQLite
- SQL
- MongoDB
- Pytest
- Python Logging
- Git
- GitHub
