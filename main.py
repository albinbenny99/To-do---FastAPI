from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Define a Pydantic model for a Task
class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

# Initialize FastAPI
app = FastAPI()

# In-memory database for storing tasks
tasks = []

# Endpoint to create a new task
@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task.id = len(tasks) + 1
    tasks.append(task)
    return task

# Endpoint to retrieve all tasks
@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks

# Endpoint to retrieve a specific task by ID
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Endpoint to update a task
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for index, t in enumerate(tasks):
        if t.id == task_id:
            tasks[index] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Endpoint to delete a task
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
