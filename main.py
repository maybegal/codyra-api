from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


class Task(BaseModel):
    id: Optional[UUID] = None
    programming_language: str
    question: str
    answer: str
    notes: Optional[str] = ""
    completed: bool = False


tasks: list[Task] = []


@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    return task


@app.get("/tasks/", response_model=list[Task])
def read_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task

    return HTTPException(status_code=404, detail="Task not found")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)