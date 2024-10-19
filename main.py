from fastapi import FastAPI, HTTPException
from request import create_prompt, get_ai_response, prompts
from models import Challenge

app = FastAPI()


@app.post("/feedback/grade", response_model=int)
def get_grade(challenge: Challenge) -> int:
    prompt = create_prompt(prompts["grade"], challenge)
    response = get_ai_response(prompt)

    return int(response)


@app.post("/feedback/overview", response_model=str)
def get_overview(challenge: Challenge) -> str:
    prompt = create_prompt(prompts["overview"], challenge)
    response = get_ai_response(prompt)

    return response


@app.post("/feedback/strategy", response_model=str)
def get_strategy(challenge: Challenge) -> str:
    prompt = create_prompt(prompts["strategy"], challenge)
    response = get_ai_response(prompt)

    return response


@app.post("/feedback/solution", response_model=str)
def get_solution(challenge: Challenge) -> str:
    prompt = create_prompt(prompts["solution"], challenge)
    response = get_ai_response(prompt)

    return response


@app.post("/feedback/code_solution", response_model=str)
def get_code_solution(challenge: Challenge) -> str:
    prompt = create_prompt(prompts["code_solution"], challenge)
    response = get_ai_response(prompt)

    return response


@app.post("/feedback/growth", response_model=str)
def get_growth(challenge: Challenge) -> str:
    prompt = create_prompt(prompts["growth"], challenge)
    response = get_ai_response(prompt)

    return response


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)