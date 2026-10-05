from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["university_ai"]
students = db["students"]

print("Total documents:", students.count_documents({}))
print("Student IDs:")

for doc in students.find({}, {"_id": 0, "student_id": 1}):
    print(doc)