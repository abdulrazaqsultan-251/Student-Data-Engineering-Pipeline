# Database Schema

## SQLite

The SQLite database is used as one of the project data sources.

The database provides student records that are extracted and standardized
before integration with the other sources.

## MongoDB Source

Database:

```text
university_ai
```
Collection:
students

The source MongoDB documents contain:
students
├── student_id
├── name
├── age
├── address
│   ├── city
│   └── country
├── academic
│   ├── gpa
│   └── attendance
└── skills[]

## MongoDB Processed Data
Database:
```
university_ai
```
Collection:
```
processed_students
```
The processed collection contains the standardized and validated pipeline
records.
The logical record identifier is the combination of:
```
student_id + source
```
This prevents records from different sources with the same student ID
from overwriting each other.
## Business Key
```
student_id is the student business identifier.
```
```
MongoDB's _id remains the MongoDB document identifier.
```
---