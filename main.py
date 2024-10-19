from fastapi import FastAPI
from request import get_response
from models import Challenge, Feedback

app = FastAPI()


@app.get("/", response_model=Feedback)
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