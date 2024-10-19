from fastapi import FastAPI
from uuid import UUID, uuid4
app = FastAPI()


class Task:
    id: UUID
    programming_language: str
    question: str
    answer: str
    notes: str = ""
    completed: bool = False

    def __init__(self, programming_language: str, question: str, answer: str, notes: str = ""):
        self.id = uuid4()
        self.programming_language = programming_language
        self.question = question
        self.answer = answer
        self.notes = notes
        self.completed = False


tasks: list[Task] = []


@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task


@app.get("/tasks/", response_model=list[Task])
def read_tasks():
    return tasks


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)