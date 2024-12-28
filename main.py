"""
This is the main entry point for the FastAPI server. It defines the API endpoints for providing feedback on coding challenges.
"""

import nest_asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from request import create_user_prompt, get_ai_response, GRADE_PROMPT, CONTENT_PROMPT
from models import Challenge, FeedbackResponse
from typing import Dict, Optional


# Initialize the FastAPI app
app = FastAPI()

# Define the allowed origins for CORS
origins = ["https://codyra-api.vercel.app"]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Initialize a cache for feedback responses
feedback_cache: Dict[str, FeedbackResponse] = {}


def get_cached_response(challenge: Challenge) -> Optional[FeedbackResponse]:
    """
    Retrieves a cached feedback response for a given challenge.
    """
    # Create a unique cache key based on the challenge attributes
    cache_key = f"{challenge.programming_language}:{challenge.question}:{challenge.answer}:{challenge.notes}"
    return feedback_cache.get(cache_key)


def set_cached_response(challenge: Challenge, response: FeedbackResponse):
    """
    Caches the feedback response for a given challenge.
    """
    # Create a unique cache key based on the challenge attributes
    cache_key = f"{challenge.programming_language}:{challenge.question}:{challenge.answer}:{challenge.notes}"
    feedback_cache[cache_key] = response


def validate_grade(response: str) -> int:
    """
    Validates and converts the AI response to an integer grade.
    Raises an HTTPException if the grade is invalid.
    """
    try:
        grade = int(response)
        if not (0 <= grade <= 100):
            raise ValueError("Grade out of range")
        return grade
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid grade response: {str(e)}")


async def get_grade(challenge: Challenge) -> int:
    user_prompt = create_user_prompt(challenge)
    ai_response = await get_ai_response(GRADE_PROMPT, user_prompt)
    return validate_grade(ai_response)


async def get_content(challenge: Challenge) -> str:
    if CONTENT_PROMPT is None:
        raise HTTPException(status_code=500, detail="Prompt template is not loaded")

    user_prompt = create_user_prompt(challenge)
    ai_response = await get_ai_response(CONTENT_PROMPT, user_prompt)
    return ai_response


@app.post("/feedback/", response_model=FeedbackResponse)
async def get_feedback(challenge: Challenge):
    # Check cache first
    cached_response = get_cached_response(challenge)
    if cached_response:
        return cached_response

    try:
        grade = await get_grade(challenge)
        content = await get_content(challenge)

        feedback = FeedbackResponse(grade=grade, content=content)

        # Cache the response
        set_cached_response(challenge, feedback)

        return feedback

    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing feedback: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(_request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/cache/")
def get_cache():
    return feedback_cache


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
