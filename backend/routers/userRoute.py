from fastapi import APIRouter
from mongo import user_collection
from models import User
import datetime


def convertUser(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"],
        "joinedAt": user["joinedAt"],
    }

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/")
def create_user(name: str, rol: str):
    user = User(username= name,role = rol)
    user.joinedAt = datetime.datetime.now(datetime.UTC)
    user_dict = user.model_dump()
    print(user_dict)
    result = user_collection.insert_one(user_dict)
    new_user = user_collection.find_one({"_id": result.inserted_id})
    return {
        "message": "User creat",
        "user": convertUser(new_user)
    }

@router.get("/")
def get_users():
    users = []
    for user in user_collection.find():
        users.append(convertUser(user))
    return users