# Data Sources Documentation

## 1. Overview

The Student Data Engineering Pipeline currently collects data from
three different data sources:

1. CSV File
2. REST API
3. SQLite Database

Each source has a different data format and extraction method.

The purpose of this stage is to document the structure, role, and
extraction method of each source before the data is integrated into
the main pipeline.

---

## 2. Source Summary

| Source | Type | Format | Extraction Method | Main Purpose |
|---|---|---|---|---|
| CSV | File | CSV | Pandas | Student basic information |
| REST API | External Source | JSON | Requests | External student records |
| SQLite | Relational Database | SQL Tables | SQLite + SQL | Relational student and academic information |

---

# 3. CSV Source

## 3.1 Source Type

The CSV source is a local file-based data source.

```text
Source Type: File
Format: CSV
Processing Library: Pandas
```
## 3.2 Source Location
The current CSV file is stored at:
```text
data/raw/students.csv
```
## 3.3 Data Content
The CSV source contains basic student information.
The current fields include:
- student ID
- student name
- age
- major
- city
## 3.4 Expected Structure
The expected logical structure is:

| Field|	Description |
|---|---:|
| student_id	| Unique identifier for the student |
| name |	Student name
| age |	 Student age
| major|	Student major
| city|	Student city



## 3.5 Extraction
The CSV data is extracted using Python and Pandas.
The extracted data is loaded into a Pandas DataFrame before
validation and transformation.
The extraction flow is:
```
students.csv
     |
     v
Pandas DataFrame
     |
     v
Validation
     |
     v
Cleaning
```
## 3.6 Data Quality Considerations
The CSV source may contain:
- Duplicate records
- Missing student names
- Invalid ages
- Missing required values
These issues are handled by the data cleaning and validation stages
of the pipeline.
# 4. REST API Source
## 4.1 Source Type
The REST API is an external data source.
```
Source Type: REST API
Response Format: JSON
Python Library: Requests
```
## 4.2 Purpose
The REST API provides student records from an external source.
The API allows the project to demonstrate extraction from an
external service instead of relying only on local files and databases.
## 4.3 Extraction Process
The API extraction process follows these steps:
```
REST API
    |
    v
HTTP Request
    |
    v
JSON Response
    |
    v
Extract Required Fields
    |
    v
Standardize Schema
    |
    v
Data Validation
```
Only the fields required by the project are extracted from the API
response.
## 4.4 Standardized Fields
The API records are converted into the common student schema used
by the integration stage.
The standardized fields include:

| Field	 | Description|
|---|---:|
student_id	| Unique identifier for the student
name	| Student name
age	| Student age
major	| Student major
city |	Student city
source	|Original source of the record


## 4.5 Data Quality Considerations
The API source may require validation for:
- Missing fields
- Invalid data types
- Invalid student IDs
- Invalid ages
- Unexpected API response structure
The API extraction process should also handle request failures and
invalid responses.
# 5. SQLite Database Source
## 5.1 Source Type
The SQLite source is a relational database.
```
Source Type: Relational Database
Database Engine: SQLite
Query Language: SQL
```
## 5.2 Database Content
The SQLite database contains the following tables:
1. students
2. instructors
3. courses
4. enrollments
5. assessments
These tables represent relational information about students,
courses, instructors, enrollments, and assessments.
## 5.3 Database Relationships
The relational database uses relationships between tables to connect
student and academic information.
The extraction process uses SQL JOIN operations to combine related
records.
Conceptually:
```
students
    |
    +---- enrollments
    |         |
    |         +---- courses
    |
    +---- assessments
    |
    +---- instructors
```
The exact relationships are defined by the database schema.
## 5.4 Extraction Process
The database extraction process follows:
```
SQLite Database
       |
       v
SQL Query
       |
       v
JOIN Related Tables
       |
       v
Extract Result
       |
       v
Pandas DataFrame
       |
       v
Validation
```
## 5.5 Main Extracted Information
The database source provides relational student and academic
information, including:
- Student information
- Course information
- Instructor information
- Enrollment information
- Assessment information
## 5.6 Data Quality Considerations
The database extraction stage should validate:
- Required columns
- Student IDs
- Missing values
- Data types
- Duplicate records
- Valid relationships between related records
# 6. Common Student Schema
Although the three sources use different formats, the pipeline
standardizes the data before integration.
The common student-level schema includes:

| Field	| Description |
|---|---:|
|student_id	| Student identifier|
|name	| Student name|
age	|Student age|
major|	Student major|
city|	Student city|
source|	Original data source|


The source field is used to preserve the origin of each record
after integration.
# 7. Source-to-Common-Schema Mapping
The sources are mapped into a common structure before integration.
| Common Field	| CSV	| REST API	| SQLite
|---|---|---|---:|
| student_id| student_id    | 	API student ID  | 	students.student_id| 
| name      | name          | 	API name field	| Student name| 
| age	    | age           | 	API age field   | 	Student age| 
| major	    | major         | 	API major field | 	Student/academic field| 
| city	    | city          | 	API city field  | 	Student city    | 
| source    | CSV	        | API	            | SQLite    | 


The exact source column names may differ between systems.
The extraction layer is responsible for mapping source-specific
fields into the common schema.
# 8. Source Validation
Each source is validated before integration.
The validation process checks:
1. Required fields exist.
2. Student IDs are present.
3. Data types are valid.
4. Student ages are valid.
5. Required student names are present.
6. Source information is correctly assigned.
Invalid records are separated from valid records and stored in the
rejected records output.
# 9. Data Lineage
The pipeline preserves the original source of each record through
the source field.
Example:
```
student_id    name          source
-----------   -----------   -------
1001          Ahmed Ali     CSV
1002          Mohammed      API
1003          Ali Hassan    SQLite
```
This allows the project to identify where an integrated record
originated.
## 10. Future Data Sources
The project will be extended with additional data sources in future
development stages.
Planned sources include:
```
- JSON
- MongoDB / NoSQL
```
These sources will be documented and integrated into the pipeline
through separate development stages.
The data source documentation will be updated whenever a new source
is added.
# 11. Development Status
|Source	|Status
|---|---:|
|CSV	|Implemented
|REST API	|Implemented
|SQLite Database|	Implemented
|JSON	|Planned
|MongoDB / NoSQL|	Planned


Current version:
```
Version: 1.0
```