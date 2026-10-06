# Pipeline Documentation

## 1. Overview

The Student Data Engineering Pipeline collects student data from multiple
sources, validates and cleans the data, integrates the sources, transforms
the records, performs final validation, and loads the final results into
CSV and MongoDB.

## 2. Data Sources

The pipeline currently uses four sources:

1. CSV
2. REST API
3. SQLite database
4. MongoDB

## 3. Extraction

Each source has a dedicated extraction module.

```text
CSV ────────────┐
REST API ───────┤
SQLite ─────────┤
MongoDB ────────┘
       ↓
    Extract
```
The MongoDB source extracts records from:
```
university_ai.students
```
## 4. Source Validation
Source-level validation is applied before integration.
The pipeline checks the expected structure of the source data.
## 5. Standardization
Records from all sources are converted to a common structure:
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
## 6. Integration
The standardized records from all four sources are combined into one
integrated DataFrame.
```
CSV
API
SQLite
MongoDB
  ↓
Integrated DataFrame
```
## 7. Cleaning
The cleaning stage handles data-quality problems including:
- Duplicate records
- Missing student names
- Invalid ages
Rejected records are saved to:
```
data/rejected/rejected_records.csv
```

## 8. Transformation
The transformation stage:
- Standardizes text fields
- Converts numeric fields to appropriate numeric types
- Preserves gpa
- Preserves attendance
- Preserves skills
## 9. Final Validation
Final validation checks:
- Required columns
- Student identifiers
- Student names
- Age values
- Allowed source values
- GPA range when available
- Attendance range when available
- Duplicate records
## 10. Loading
Validated records are saved to:
```
data/processed/final_dataset.csv
```
and MongoDB:
```
university_ai.processed_students
```
The MongoDB loader uses:
```
student_id + source
```
to support repeatable pipeline execution.
## 11. Final Pipeline
```text
CSV ────────────┐
REST API ───────┤
SQLite ─────────┤
MongoDB ────────┘
       ↓
     Extract
       ↓
Source Validation
       ↓
Standardization
       ↓
Integration
       ↓
Cleaning
       ↓
Transformation
       ↓
Final Validation
       ↓
   ┌───┴────┐
   ↓        ↓
  CSV     MongoDB
````
## 12. Final Execution Result
The final successful pipeline execution produced:
```
Final records    : 45
Rejected records : 5

Rejected records:
Duplicate record      : 2
Invalid age           : 2
Missing student_name  : 1
```
---