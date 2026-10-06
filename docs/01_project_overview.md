# Student Data Engineering Pipeline

## 1. Project Overview

The Student Data Engineering Pipeline is a multi-source ETL pipeline
designed to collect, validate, clean, integrate, transform, and process
student data from different data sources.

The current project version uses three data sources:

- CSV
- REST API
- SQLite Database

The pipeline processes the extracted data through several stages and
produces a final processed dataset.

The project also maintains rejected records separately and records
pipeline execution information through logging.

This project will be developed incrementally by adding new data sources,
processing capabilities, validation rules, and storage mechanisms in
separate development stages.

---

## 2. Project Objectives

The main objectives of the project are:

1. Extract student data from multiple data sources.
2. Standardize data from different source formats.
3. Validate source data before processing.
4. Clean invalid and duplicate records.
5. Preserve rejected records with rejection reasons.
6. Integrate data from multiple sources.
7. Transform the integrated dataset into a standardized structure.
8. Perform final data quality validation.
9. Store the processed dataset.
10. Maintain execution logs.
11. Provide automated tests for the pipeline.
12. Document each development stage of the project.

---

## 3. Current Data Sources

The current version of the project contains three data sources:

### 3.1 CSV

The CSV source contains basic student information such as:

- student ID
- student name
- age
- major
- city

Source file:

```text
data/raw/students.csv
```
### 3.2 REST API
The REST API provides student records from an external data source.
Only the required fields are extracted from the API response and
standardized into the common student schema.
### 3.3 SQLite Database
The SQLite database provides relational student information.
The database contains:
- students
- instructors
- courses
- enrollments
- assessments
SQL JOIN operations are used to extract integrated information from
the relational database.
## 4. Current Pipeline
The current pipeline follows these stages:
```text 
CSV ────────────┐
                │
REST API ───────┼──> Extract
                │
SQLite ─────────┘
                    │
                    ▼
                 Validate
                    │
                    ▼
                   Clean
                    │
              ┌─────┴─────┐
              ▼           ▼
        Clean Records  Rejected Records
              │           │
              ▼           ▼
          Integrate    rejected_records.csv
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

## 5. Data Quality Processing
The pipeline currently handles the following data quality problems:
- Duplicate records
- Missing student names
- Invalid ages
- Missing required values
- Invalid source values
- Duplicate student records
Rejected records are not silently discarded.
Instead, they are stored separately with a rejection reason.
Output file:
```text
data/rejected/rejected_records.csv
```
## 6. Current Pipeline Results
The current baseline version processes the following records:

| Stage | Records |
|---|---:|
| CSV | 13 |
| REST API | 20 |
| SQLite | 26 |
| Integrated | 41 |
| Clean | 37 |
| Rejected | 4 |

The rejected records currently include:
- One duplicate record
- One record with a missing student name
- Two records with invalid ages
These values represent the current baseline version and will be updated when future pipeline stages change the input sources or
processing rules.

### 7. Output
The current pipeline produces the following outputs.
### 7.1 Final Dataset
```text
data/processed/final_dataset.csv
```
Contains valid, cleaned, integrated, and transformed records.
### 7.2 Rejected Records
```text
data/rejected/rejected_records.csv
```
Contains records rejected during data quality processing together
with the reason for rejection.
### 7.3 Pipeline Log
```text
logs/pipeline.log
```
Contains information about pipeline execution and processing stages.

### 8. Technologies
The current project uses:
- Python
- Pandas
- Requests
- SQLite
- SQL
- Pytest
- Python Logging

### 9. Development Strategy
The project will be developed incrementally.
Each development stage will be implemented and documented separately.
The development process will include:
1. Create a new Git branch.
2. Implement one development stage.
3. Test the changes.
4. Document the changes.
5. Run the complete pipeline.
6. Record the results.
7. Commit the changes.
8. Push the branch to GitHub.
9. Merge the changes when the stage is approved.
Future development stages will extend the current pipeline with
additional data sources and data engineering capabilities.
## 10. Current Version
```text
Version: 1.0
Status: Baseline
Sources: CSV + REST API + SQLite
```
This version represents the starting point for the next development
stages of the Student Data Engineering Pipeline.