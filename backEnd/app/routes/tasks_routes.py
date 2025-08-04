from fastapi import APIRouter,Depends,HTTPException
from uuid import uuid4
from models.task import TaskCreate,TaskOut
from database.mongo import task_collection
from typing import List
from routes.authentication import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/createTask", response_model=TaskOut)
async def create_task(task: TaskCreate, user: dict = Depends(get_current_user)):
    task_dict = task.dict()
    task_dict["task_id"] = str(uuid4())
    task_dict["user_id"] = user["_id"]

    result = await task_collection.insert_one(task_dict)

    if result.inserted_id:
        return TaskOut(**task_dict)
    raise HTTPException(status_code=500, detail="Task creation failed")

@router.get("/allTasks", response_model=List[TaskOut])
async def get_tasks(user : dict = Depends(get_current_user)):
    tasks_cursor = task_collection.find({"user_id": user["_id"]})
    tasks = []
    async for task in tasks_cursor:
        tasks.append(TaskOut(**task))
    return tasks

@router.get("getTask/{task_id}",response_model = TaskOut)
async def get_task(task_id: str, user: dict = Depends(get_current_user)):
    task = await task_collection.find_one({"task_id": task_id, "user_id": user["_id"]})
    if not task:
        raise HTTPException(status_code = 404, detail = "task not found")
    return TaskOut(**task)
  

@router.put("update/{task_id}", response_model= TaskOut)
async def update_task(task_id: str, updated_task: TaskCreate, user: dict = Depends(get_current_user)):
    existing_task = await task_collection.find_one({"task_id": task_id, "user_id": user["_id"]})
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = updated_task.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.now() 

    result = await task_collection.update_one(
        {"task_id": task_id, "user_id": user["_id"]},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made to the task")
    updated_task_doc = await task_collection.find_one({"task_id": task_id, "user_id": user["_id"]})
    if not updated_task_doc:
        raise HTTPException(status_code=500, detail="Failed to retrieve updated task")

    return TaskOut(**updated_task_doc)

@router.delete("delete/{task_id}")
async def delete_task(task_id: str, user: dict = Depends(get_current_user)):
    task = await task_collection.delete_one({"task_id": task_id, "user_id": user["_id"]})
    if task.deleted_count == 0:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return {"message":"Task deleted successfully"}