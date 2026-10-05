import os

import pandas as pd
from pymongo import MongoClient


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "university_ai"
COLLECTION_NAME = "students"


def extract_mongodb() -> pd.DataFrame:
    """
    Extract student data from MongoDB.

    Returns:
        pd.DataFrame: Student records extracted from MongoDB.
    """
    client = MongoClient(MONGO_URI)

    try:
        client.admin.command("ping")

        collection = client[DATABASE_NAME][COLLECTION_NAME]

        documents = list(
            collection.find(
                {},
                {
                    "_id": 0,
                    "student_id": 1,
                    "name": 1,
                    "age": 1,
                    "address": 1,
                    "academic": 1,
                    "skills": 1,
                },
            )
        )

        if not documents:
            raise ValueError("MongoDB students collection is empty.")

        records = []

        for document in documents:
            address = document.get("address", {})
            academic = document.get("academic", {})

            records.append(
                {
                    "student_id": document.get("student_id"),
                    "student_name": document.get("name"),
                    "age": document.get("age"),
                    "city": address.get("city"),
                    "gpa": academic.get("gpa"),
                    "attendance": academic.get("attendance"),
                    "skills": document.get("skills", []),
                    "source": "mongodb",
                }
            )

        return pd.DataFrame(records)

    finally:
        client.close()