PRAGMA foreign_keys = ON;

-- =========================================
-- Instructors
-- =========================================

CREATE TABLE IF NOT EXISTS instructors (
    instructor_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    department TEXT NOT NULL,
    email TEXT UNIQUE
);


-- =========================================
-- Students
-- =========================================

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    gender TEXT,
    date_of_birth TEXT,
    city TEXT
);


-- =========================================
-- Courses
-- =========================================

CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    credit_hours INTEGER NOT NULL,
    instructor_id INTEGER,

    CONSTRAINT fk_course_instructor
        FOREIGN KEY (instructor_id)
        REFERENCES instructors(instructor_id),

    CONSTRAINT chk_credit_hours
        CHECK (credit_hours > 0)
);


-- =========================================
-- Enrollments
-- =========================================

CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date TEXT NOT NULL,
    semester TEXT NOT NULL,

    CONSTRAINT fk_enrollment_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id),

    CONSTRAINT fk_enrollment_course
        FOREIGN KEY (course_id)
        REFERENCES courses(course_id),

    CONSTRAINT uq_student_course_semester
        UNIQUE (
            student_id,
            course_id,
            semester
        )
);


-- =========================================
-- Assessments
-- =========================================

CREATE TABLE IF NOT EXISTS assessments (
    assessment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    assessment_type TEXT NOT NULL,
    score REAL NOT NULL,

    CONSTRAINT fk_assessment_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id),

    CONSTRAINT fk_assessment_course
        FOREIGN KEY (course_id)
        REFERENCES courses(course_id),

    CONSTRAINT chk_score
        CHECK (score BETWEEN 0 AND 100)
);