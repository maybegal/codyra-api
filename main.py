import nest_asyncio

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from request import create_prompt, get_ai_response, grade_prompt
from models import Challenge, FeedbackResponse
from typing import Dict, Any

app = FastAPI()

origins = [
    "http://localhost:3000",  # For development
    "https://codyra-api.vercel.app"
]

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nest_asyncio.apply()

feedback_cache: Dict[str, FeedbackResponse] = {}


def get_cached_response(challenge: Challenge) -> FeedbackResponse:
    cache_key = f"{challenge.programming_language}:{challenge.question}:{challenge.answer}"
    return feedback_cache.get(cache_key)


def set_cached_response(challenge: Challenge, response: FeedbackResponse):
    cache_key = f"{challenge.programming_language}:{challenge.question}:{challenge.answer}"
    feedback_cache[cache_key] = response


def validate_grade(response: str) -> int:
    try:
        return int(response)
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response from AI service")


async def get_grade(challenge: Challenge) -> int:
    prompt = create_prompt(grade_prompt, challenge)
    ai_response = await get_ai_response(prompt)

    return validate_grade(ai_response)


async def get_content(challenge: Challenge) -> str:
    file = open("prompt.txt", "r")

    prompt = create_prompt(file.read(), challenge)
    ai_response = await get_ai_response(prompt)

    return ai_response


@app.post("/feedback/", response_model=FeedbackResponse)
async def get_feedback(challenge: Challenge):
    # Check cache first
    cached_response = get_cached_response(challenge)
    if cached_response:
        return cached_response

    try:
        grade = get_grade(challenge)
        content = get_content(challenge)

        feedback = FeedbackResponse(grade=grade, content=content)

        # Cache the response
        set_cached_response(challenge, feedback)

        return feedback

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/cache/")
def get_cache():
    return feedback_cache


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
