-- =========================================================
-- Basic SELECT Queries
-- =========================================================

-- 1. Display all students
SELECT *
FROM students;


-- 2. Display all instructors
SELECT *
FROM instructors;


-- 3. Display all courses
SELECT *
FROM courses;


-- 4. Display all enrollments
SELECT *
FROM enrollments;


-- 5. Display all assessments
SELECT *
FROM assessments;

-- =========================================================
-- Filtering with WHERE
-- =========================================================

-- 6. Display students from Sanaa
SELECT *
FROM students
WHERE city = 'Sanaa';


-- 7. Display female students
SELECT *
FROM students
WHERE gender = 'Female';


-- 8. Display courses with 3 credit hours
SELECT *
FROM courses
WHERE credit_hours = 3;


-- =========================================================
-- Sorting with ORDER BY
-- =========================================================

-- 9. Display students ordered by name
SELECT *
FROM students
ORDER BY full_name ASC;


-- 10. Display courses ordered by credit hours
-- from highest to lowest
SELECT *
FROM courses
ORDER BY credit_hours DESC;

-- =========================================================
-- JOIN Queries
-- =========================================================

-- 11. Display students with their enrolled courses
SELECT
    s.student_id,
    s.full_name AS student_name,
    c.course_name,
    e.semester
FROM enrollments AS e
JOIN students AS s
    ON e.student_id = s.student_id
JOIN courses AS c
    ON e.course_id = c.course_id
ORDER BY
    s.student_id,
    c.course_id;