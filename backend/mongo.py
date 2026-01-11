from pymongo import MongoClient


MONGODB_URL="mongodb+srv://belticvictor22:stud@iotbd.f16qbsn.mongodb.net/"

client = MongoClient(MONGODB_URL)

db = client.project
task_collection = db.get_collection("tasks")
user_collection = db.get_collection("users")