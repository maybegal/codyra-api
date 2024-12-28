"""
This is the main entry point for the FastAPI server. It defines the API endpoints for providing feedback on coding challenges.
"""

import nest_asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from request import get_ai_response
from models import Challenge, Feedback
from typing import Dict, Optional


# Initialize the FastAPI app
app = FastAPI()

# Define the allowed origins for CORS
origins = ["https://codyra-api.vercel.app", "http://localhost"]

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
feedback_cache: Dict[str, Feedback] = {}


def get_cached_response(challenge: Challenge) -> Optional[Feedback]:
    """
    Retrieves a cached feedback response for a given challenge.
    """
    # Create a unique cache key based on the challenge attributes
    cache_key = f"{challenge.programming_language}:{challenge.question}:{challenge.answer}:{challenge.notes}"
    return feedback_cache.get(cache_key)


def set_cached_response(challenge: Challenge, response: Feedback):
    """
    Caches the feedback response for a given challenge.
    """
    # Create a unique cache key based on the challenge attributes
    cache_key = f"{challenge.programming_language}:{challenge.question}:{challenge.answer}:{challenge.notes}"
    feedback_cache[cache_key] = response


@app.post("/feedback/", response_model=Feedback)
async def get_feedback(challenge: Challenge):
    # Check cache first
    cached_response = get_cached_response(challenge)
    if cached_response:
        return cached_response

    try:
        feedback: Feedback = await get_ai_response(challenge)

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


def main() -> None:
    """
    Main entry point for the FastAPI server.
    """
    import uvicorn

    uvicorn.run(app)


if __name__ == "__main__":
    main()
