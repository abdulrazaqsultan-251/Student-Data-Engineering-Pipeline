from pymongo import MongoClient


# ==========================================================
# MongoDB Configuration
# ==========================================================

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "university_ai"
COLLECTION_NAME = "students"


# ==========================================================
# Student Academic and Skills Data
# ==========================================================

STUDENT_DATA = {
    1001: {
        "academic": {
            "gpa": 3.5,
            "attendance": 92,
        },
        "skills": [
            "Python",
            "SQL",
            "MongoDB",
        ],
    },

    1002: {
        "academic": {
            "gpa": 3.8,
            "attendance": 96,
        },
        "skills": [
            "Python",
            "Pandas",
            "SQL",
        ],
    },

    1003: {
        "academic": {
            "gpa": 3.1,
            "attendance": 88,
        },
        "skills": [
            "Java",
            "SQL",
            "Data Analysis",
        ],
    },

    1004: {
        "academic": {
            "gpa": 3.6,
            "attendance": 94,
        },
        "skills": [
            "Python",
            "MongoDB",
            "Data Analysis",
        ],
    },

    1005: {
        "academic": {
            "gpa": 2.9,
            "attendance": 85,
        },
        "skills": [
            "Java",
            "SQL",
            "Git",
        ],
    },

    1006: {
        "academic": {
            "gpa": 3.4,
            "attendance": 90,
        },
        "skills": [
            "Python",
            "Git",
            "SQL",
        ],
    },

    1007: {
        "academic": {
            "gpa": 3.7,
            "attendance": 97,
        },
        "skills": [
            "Python",
            "Machine Learning",
            "MongoDB",
        ],
    },

    1008: {
        "academic": {
            "gpa": 2.9,
            "attendance": 82,
        },
        "skills": [
            "Python",
            "SQL",
            "Git",
        ],
    },

    1009: {
        "academic": {
            "gpa": 3.5,
            "attendance": 92,
        },
        "skills": [
            "Python",
            "SQL",
        ],
    },
}


# ==========================================================
# MongoDB Connection
# ==========================================================

def get_collection():
    """
    Create a MongoDB connection and return the students collection.
    """

    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
    )

    # Verify MongoDB connection
    client.admin.command("ping")

    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]

    return client, collection


# ==========================================================
# Prepare Student Data
# ==========================================================

def prepare_student_data():
    """
    Add academic and skills information to existing students.

    Existing student information is preserved.
    Only the academic and skills fields are updated.
    """

    client, students = get_collection()

    try:
        print("MongoDB connection successful.")
        print()

        updated_count = 0
        skipped_count = 0

        for student_id, student_data in STUDENT_DATA.items():

            result = students.update_one(
                {"student_id": student_id},
                {
                    "$set": {
                        "academic": student_data["academic"],
                        "skills": student_data["skills"],
                    }
                },
            )

            if result.matched_count == 1:
                updated_count += 1

                print(
                    f"Student {student_id}: "
                    "academic and skills updated."
                )

            else:
                skipped_count += 1

                print(
                    f"Student {student_id}: "
                    "student not found."
                )

        print()
        print("=" * 50)
        print("MongoDB Data Preparation Completed")
        print("=" * 50)
        print(f"Students updated : {updated_count}")
        print(f"Students skipped : {skipped_count}")

    finally:
        client.close()


# ==========================================================
# Validate Prepared Data
# ==========================================================

def validate_prepared_data():
    """
    Verify that all prepared students contain
    academic and skills fields.
    """

    client, students = get_collection()

    try:
        print()
        print("Validating prepared MongoDB data...")
        print()

        total_students = students.count_documents({})

        valid_students = students.count_documents(
            {
                "academic": {"$exists": True},
                "skills": {"$exists": True},
            }
        )

        print(f"Total students      : {total_students}")
        print(f"Prepared students   : {valid_students}")

        if total_students != valid_students:
            raise ValueError(
                "Some students are missing academic or skills data."
            )

        print()
        print("Validation passed successfully.")

    finally:
        client.close()


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    prepare_student_data()
    validate_prepared_data()