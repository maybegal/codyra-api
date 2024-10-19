from fastapi import FastAPI

app = FastAPI()


class Question:
    programming_language: str
    question: str
    answer: str
    notes: str = ""
    completed = False

    def __init__(self, programming_language: str, question: str, answer: str, notes: str = ""):
        self.programming_language = programming_language
        self.question = question
        self.answer = answer
        self.notes = notes
        self.completed = False

@app.post("/questions/", response_model=Question)
def create_question(question: Question):
    pass

@app.get("/")
def read():
    return {"hello": "world"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)