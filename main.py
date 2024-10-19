from fastapi import FastAPI, HTTPException
from request import get_response
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


class Challenge(BaseModel):
    programming_language: str
    question: str
    answer: str
    notes: Optional[str] = ""


class Feedback(BaseModel):
    grade: int
    overview: str
    strategy: str
    solution: str
    code_solution: str
    growth: str


@app.get("/", response_model=Challenge)
def get_feedback(challenge: Challenge) -> Feedback:
    feedback_data = get_response(challenge)

    feedback = Feedback(
        grade=feedback_data["grade"],
        overview=feedback_data["overview"],
        strategy=feedback_data["strategy"],
        solution=feedback_data["solution"],
        code_solution=feedback_data["code_solution"],
        growth=feedback_data["growth"]
    )

    return feedback


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)