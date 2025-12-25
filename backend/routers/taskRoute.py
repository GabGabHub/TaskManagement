from fastapi import APIRouter, HTTPException, Body
from mongo import task_collection
from models import Task
import datetime


def convertTask(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "status": task["status"],
        "priority": task["priority"],
        "assignedTo": task.get("assignedTo"),
        "createdAt": task.get("createdAt"),
        "assignedAt": task.get("assignedAt"),
        "completedAt": task.get("completedAt")
    }

router = APIRouter(
 prefix="/tasks",
 tags=["tasks"]
)

@router.post("/")
def create_task(task: Task):
    task.createdAt = datetime.datetime.now(datetime.UTC)
    task_dict = task.model_dump()
    result = task_collection.insert_one(task_dict)
    new_task = task_collection.find_one({"_id": result.inserted_id})
    return {
        "message": "Task creat",
        "task": convertTask(new_task)
    }


@router.get("/")
def get_tasks():
    tasks = []
    for task in task_collection.find():
        tasks.append(convertTask(task))
    return tasks

@router.delete("/{id}")
def delete_task(id: str):

    delete_result = task_collection.delete_one({"title": id})

    if delete_result.deleted_count == 1:
        return {"message":"Task deleted succesfully"}

    raise HTTPException(status_code=404, detail=f"Task {id} not found")

@router.put("/{id}")
def assign_task(id: str, user: str = Body(...)):

    update_task = task_collection.update_one({"title": id},{"$set": {"assignedTo": user,"status": "assigned", "assignedAt": datetime.datetime.now(datetime.UTC)}})

    if update_task.modified_count != 0:
        return {"message":"Task assigned succesfully"}

    raise HTTPException(status_code=404, detail=f"Task {id} not found")

@router.put("/complete/{id}")
def assign_task(id: str):

    update_task = task_collection.update_one({"title": id},{ "$set": {"status": "closed", "completedAt": datetime.datetime.now(datetime.UTC)}})

    if update_task.modified_count != 0:
        return {"message":"Task completed succesfully"}

    raise HTTPException(status_code=404, detail=f"Task {id} not found")