
---

# 6. `docs/validation_rules.md`

```markdown
# Validation Rules

## Student ID

- Must be present.
- Must be numeric after transformation.

## Student Name

- Must be present.
- Missing student names are rejected.

## Age

When an age is available:

- Must be numeric.
- Must be between 16 and 80.

Invalid age records are rejected.

## GPA

When GPA is available:

- Must be numeric.
- Must be between 0 and 4.

## Attendance

When attendance is available:

- Must be numeric.
- Must be between 0 and 100.

## Source

The source must be one of:

- `csv`
- `api`
- `database`
- `mongodb`

## Duplicate Records

Duplicate records are detected using the standardized record fields:

```text
student_id
student_name
age
city
gpa
attendance
source
```
The skills array is preserved as a list and is not used directly by
Pandas duplicate detection.
## Rejected Data
Rejected records are stored in:
```
data/rejected/rejected_records.csv
```
Each rejected record contains a rejection reason.
----