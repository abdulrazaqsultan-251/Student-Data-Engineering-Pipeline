import os

import pandas as pd
from pymongo import MongoClient, UpdateOne


MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/",
)

DATABASE_NAME = "university_ai"
COLLECTION_NAME = "processed_students"


def save_processed_data(dataframe: pd.DataFrame) -> None:
    """
    Save the final processed student data to MongoDB.

    Records are identified by the combination of
    student_id and source to avoid overwriting records
    from different data sources.
    """

    if dataframe.empty:
        raise ValueError(
            "Cannot save an empty dataframe to MongoDB."
        )

    client = MongoClient(MONGO_URI)

    try:
        client.admin.command("ping")

        collection = client[DATABASE_NAME][COLLECTION_NAME]

        operations = []

        for record in dataframe.to_dict(
            orient="records"
        ):
            document = {}

            for key, value in record.items():
                if isinstance(value, (list, dict)):
                    document[key] = value
                elif pd.isna(value):
                    document[key] = None
                elif hasattr(value, "item"):
                    document[key] = value.item()
                else:
                    document[key] = value

            operations.append(
                UpdateOne(
                    {
                        "student_id": document["student_id"],
                        "source": document["source"],
                    },
                    {"$set": document},
                    upsert=True,
                )
            )

        if operations:
            collection.bulk_write(operations)

    finally:
        client.close()