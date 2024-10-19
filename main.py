from fastapi import FastAPI

app = FastAPI()


class Task:
    programming_language: str
    question: str
    answer: str
    notes: str = ""
    completed: bool = False

    def __init__(self, programming_language: str, question: str, answer: str, notes: str = ""):
        self.programming_language = programming_language
        self.question = question
        self.answer = answer
        self.notes = notes
        self.completed = False


tasks: list[Task] = []


@app.post("/questions/", response_model=Task)
def create_question(question: Task):
    pass


@app.get("/")
def read():
    return {"hello": "world"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)