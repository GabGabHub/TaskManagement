from pymongo import MongoClient


MONGODB_URL="secret"

client = MongoClient(MONGODB_URL)

db = client.project
task_collection = db.get_collection("tasks")

user_collection = db.get_collection("users")
