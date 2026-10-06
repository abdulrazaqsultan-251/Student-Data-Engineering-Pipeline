# Data Dictionary

## Student Data Fields

| Field | Type | Required | Description |
|---|---|---|---|
| student_id | INTEGER | Yes | Student business identifier |
| student_name | TEXT | Yes | Student full name |
| age | INTEGER | No | Student age |
| city | TEXT | No | Student city |
| gpa | FLOAT | No | Grade Point Average, when available |
| attendance | FLOAT | No | Student attendance percentage, when available |
| skills | ARRAY | No | List of student skills |
| source | TEXT | Yes | Original data source |

## Source Values

The `source` field identifies where each record originated.

Allowed values:

- `csv`
- `api`
- `database`
- `mongodb`

## MongoDB Academic Structure

The original MongoDB student documents contain:

```text
academic
├── gpa
└── attendance
```
and:
skills

as an array of student skills.
During extraction, the nested MongoDB fields are converted into the standardized pipeline columns:
- academic.gpa → gpa
- academic.attendance → attendance
- skills → skills

---
