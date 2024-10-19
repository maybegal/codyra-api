import nest_asyncio

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from request import create_prompt, get_ai_response, prompts
from models import Challenge, FeedbackResponse
from typing import Dict, Any

app = FastAPI()

nest_asyncio.apply()

feedback_cache: Dict[str, Any] = {}


def get_cached_response(challenge: Challenge, prompt_type: str) -> Any:
    cache_key = f"{challenge.programming_language}:{challenge.question}:{challenge.answer}:{prompt_type}"
    return feedback_cache.get(cache_key)


def set_cached_response(challenge: Challenge, prompt_type: str, response: Any):
    cache_key = f"{challenge.programming_language}:{challenge.question}:{challenge.answer}:{prompt_type}"
    feedback_cache[cache_key] = response


def validate_ai_response(response: str, expected_type: type) -> Any:
    try:
        if expected_type == int:
            return int(response)
        return expected_type(response)
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response from AI service")


@app.post("/feedback/{feedback_type}", response_model=FeedbackResponse)
async def get_feedback(feedback_type: str, challenge: Challenge):
    if feedback_type not in prompts:
        raise HTTPException(status_code=400, detail="Invalid feedback type")

    # Check cache first
    cached_response = get_cached_response(challenge, feedback_type)
    if cached_response:
        return FeedbackResponse(feedback_type=feedback_type, content=cached_response)

    try:
        prompt = create_prompt(prompts[feedback_type], challenge)
        ai_response = await get_ai_response(prompt)

        # Validate and process AI response
        if feedback_type == "grade":
            processed_response = validate_ai_response(ai_response, int)
        else:
            processed_response = validate_ai_response(ai_response, str)

        # Cache the response
        set_cached_response(challenge, feedback_type, processed_response)

        return FeedbackResponse(feedback_type=feedback_type, content=processed_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)