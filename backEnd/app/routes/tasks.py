from fastapi import APIRouter,Depends,HTTPException
from uuid import uuid4
from models.task import TaskCreate
from database.mongo import task_collection
from typing import List
from routes.authentication import get_current_user

router = APIRouter()

@router.post("/createTask", response_model=TaskCreate)
async def create_task(task: TaskCreate, user: dict = Depends(get_current_user)):
    task_dict = task.dict()
    task_dict["task_id"] = str(uuid4())
    task_dict["user_id"] = user["sub"]

    result = await task_collection.insert_one(task_dict)

    if result.inserted_id:
        return task_dict
    raise HTTPException(status_code=500, detail="Task creation failed")

@router.get("/allTasks", response_model=List[TaskCreate])
async def get_tasks(user : dict = Depends(get_current_user)):
    tasks_cursor = task_collection.find({"user_id": user["id"]})
    tasks = []
    async for task in tasks_cursor:
        tasks.append(TaskCreate(**task))
    return tasks

@router.get("/{task_id}",response_model = TaskCreate)
async def get_task(task_id: str, user: dict = Depends(get_current_user)):
    task = await task_collection.find_one({"task_id": task_id, "user_id": user["id"]})
    if not task:
        raise HTTPException(status_code = 404, detail = "task not found")
    return TaskCreate(**task)
  

@router.put("/{task_id}", response_model= TaskCreate)
async def update_task(task_id: str, updated_task: TaskCreate, user: dict = Depends(get_current_user)):
    task = await task_collection.replace_one({"id": task_id, "user_id": user["id"]}, {**updated_task.dict(), "task_id": task_id, "user_id": user["id"]})
    if task.modified_count == 0:
        raise HTTPException(status_code = 404, detail = "Task not found or no changes made")
    return updated_task

@router.delete("/{task_id}")
async def delete_task(task_id: str, user: dict = Depends(get_current_user)):
    task = await task_collection.delete_one({"task_id": task_id, "user_id": user["id"]})
    if task.deleted_count == 0:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return {"message":"Task deleted successfully"}