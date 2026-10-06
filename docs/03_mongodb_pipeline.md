from pathlib import Path

content = r'''# MongoDB Pipeline

## 1. Overview

MongoDB was added as a NoSQL data source to the **Student Data Engineering Pipeline**.

The MongoDB database contains student documents with both simple fields and nested data structures.

### Current MongoDB Configuration

| Configuration | Value |
|---|---|
| Database | `university_ai` |
| Collection | `students` |
| Number of Students | `9` |

### MongoDB Pipeline Stage

The current MongoDB stage includes:

1. Data Preparation
2. MongoDB Extraction
3. Conversion to Pandas DataFrame
4. Preparation for Validation and Integration

---

## 2. MongoDB Document Structure

A student document contains fields such as:

- `student_id`
- `name`
- `age`
- `address`
- `academic`
- `skills`

### Example Document

```json
{
    "student_id": 1009,
    "name": "Ahmed Ali",
    "age": 22,
    "address": {
        "city": "Sanaa",
        "country": "Yemen"
    },
    "academic": {
        "gpa": 3.5,
        "attendance": 92
    },
    "skills": [
        "Python",
        "SQL"
    ]
}
```

MongoDB supports nested structures such as `address` and `academic`, as well as arrays such as `skills`.

---

## 3. Data Preparation

A dedicated preparation script was created:

```text
scripts/prepare_mongodb_students.py
```

### Purpose

The purpose of this script is to add or update the required MongoDB fields:

- `academic.gpa`
- `academic.attendance`
- `skills`

The script uses MongoDB's `update_one()` operation together with `$set`.

This approach updates only the required fields without replacing the complete student document.

### Preparation Validation

After preparation, the script validates:

- Total number of students
- Number of students containing `academic`
- Number of students containing `skills`

### Current Validation Result

```text
Total students      : 9
Prepared students   : 9
```

**Validation passed successfully.**

---

## 4. MongoDB Extraction

The MongoDB extraction module is:

```text
app/sources/mongodb_source.py
```

The main extraction function is:

```python
extract_mongodb()
```

The module connects to MongoDB using **PyMongo** and reads documents from:

```text
university_ai.students
```

The MongoDB `_id` field is excluded from the extracted data because it is MongoDB's internal document identifier and is not required by the pipeline.

---

## 5. MongoDB to Pipeline Mapping

MongoDB fields are mapped to the common pipeline structure.

| MongoDB Field | Pipeline Field |
|---|---|
| `student_id` | `student_id` |
| `name` | `student_name` |
| `age` | `age` |
| `address.city` | `city` |
| `academic.gpa` | `gpa` |
| `academic.attendance` | `attendance` |
| `skills` | `skills` |
| — | `source = mongodb` |

This mapping allows MongoDB data to enter the pipeline in a consistent and structured Pandas DataFrame format.

---

## 6. Extraction Result

The MongoDB extraction was tested successfully.

### Current Result

```text
Total documents extracted: 9
```

The resulting DataFrame contains the following fields:

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

### Example

| student_id | student_name | age | city | gpa | attendance | skills | source |
|---:|---|---:|---|---:|---:|---|---|
| 1009 | Ahmed Ali | 22 | Sanaa | 3.5 | 92 | `[Python, SQL]` | mongodb |

---

## 7. Data Quality Observation

During extraction, some MongoDB documents do not contain `address.city`.

As a result, the `city` field is returned as a missing value for those records.

This missing value is **intentionally not replaced during extraction**.

The missing-value problem will be handled later during the **validation and cleaning** stages of the pipeline.

This approach maintains a clear separation between the different pipeline responsibilities:

- **Extraction**
- **Validation**
- **Cleaning**
- **Transformation**

The extraction stage should retrieve the source data without modifying or concealing data-quality issues.

---

## 8. Current MongoDB Pipeline

The current MongoDB pipeline is:

```text
MongoDB
   |
   v
MongoDB Extraction
   |
   v
Pandas DataFrame
   |
   v
Validation
   |
   v
Cleaning
   |
   v
Integration
   |
   v
Transformation
   |
   v
Final Validation
```

---

## 9. Files Added

The MongoDB implementation currently includes the following files:

```text
scripts/
└── prepare_mongodb_students.py

app/
└── sources/
    └── mongodb_source.py

tests/
└── test_mong.py
```

### File Responsibilities

| File | Responsibility |
|---|---|
| `scripts/prepare_mongodb_students.py` | Prepares and validates MongoDB student documents |
| `app/sources/mongodb_source.py` | Extracts MongoDB data and maps it to the pipeline structure |
| `tests/test_mong.py` | Tests the MongoDB pipeline functionality |

---

## 10. Git Development

MongoDB development is implemented incrementally using a separate Git branch:

```text
mongodb-pipeline-v1
```

### First MongoDB Preparation Commit

The first MongoDB preparation commit is:

```text
Add MongoDB student data preparation
```

The MongoDB extraction stage is being developed incrementally before integrating it into the main pipeline.

This approach allows the MongoDB implementation to be developed, tested, and validated independently before being merged into the main pipeline.

---
