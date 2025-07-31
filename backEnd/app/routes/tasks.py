from fastapi import APIRouter,Depends,HTTPException
from typing import List
from _uuid import uuid4
from models.task import TaskCreate

router = APIRouter()

temp_tasks_db = {}

@router.post("/", response_model = TaskCreate)
async def create_task(task: TaskCreate):
    task_id = str(uuid4())
    temp_tasks_db[task_id] = task
    return { "task_id": task_id, "task": task}

@router.get("/", response_model= List[dict])
async def get_tasks():
    return [{"task_id": taskID, "task": task} for taskID, task in temp_tasks_db.items()]

@router.get("/{task_id}",response_model = dict)
async def get_task(task_id: str):
    task = temp_tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail = "taslk not found")
    return {"task_if" : task_id, "task" : task}

@router.put("/{task_id}", response_model= dict)
async def update_task(task_id: str, task: TaskCreate):
    if task_id not in temp_tasks_db:
        raise HTTPException(status_code = 404, detail ="task not found" )
    temp_tasks_db[task_id] = task
    return {"task_id": task_id, "task": task}

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    if task_id not in temp_tasks_db:
        raise HTTPException(status_code = 404, detail = "task not found")
    del temp_tasks_db[task_id]
    return {"detail": "Task deleted successfully"}