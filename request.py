"""
This module handles interactions with the AI client to generate responses based on programming challenges.
"""

import json
from g4f.client import Client
from models import Challenge, Feedback
from typing import Optional
from fastapi import HTTPException

# Initialize the AI client
client = Client()


def load_prompt_file(path: str = "prompt.txt") -> Optional[str]:
    """
    Reads the content of given path and returns it as a string.
    Returns None if the file cannot be read.
    """
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return None


def create_user_prompt(challenge: Challenge) -> str:
    """
    Constructs a user prompt string from a Challenge object.
    """
    user_prompt = (
        f"Programming language: {challenge.programming_language}\n"
        f"The question: {challenge.question}\n"
        f"User's answer: {challenge.answer}"
    )

    if (challenge.notes is not None) and (challenge.notes != ""):
        user_prompt += f"\nAdditional notes: {challenge.notes}"

    return user_prompt


def validate_challenge(challenge: Challenge) -> None:
    """
    Validates that the Challenge object contains all required parameters.
    Raises an HTTPException if any required parameter is missing.
    """
    if not challenge.programming_language:
        raise HTTPException(status_code=400, detail="Programming language is required.")
    if not challenge.question:
        raise HTTPException(status_code=400, detail="Question is required.")
    if not challenge.answer:
        raise HTTPException(status_code=400, detail="Answer is required.")


async def get_ai_response(challenge: Challenge) -> Feedback:
    """
    Sends a request to the AI model with the given system and user prompts.
    Returns the AI's response as a Feedback object.
    """
    # Load the prompt from the file
    system_prompt: str = load_prompt_file()

    # Validate the challenge
    validate_challenge(challenge)

    # Construct the user prompt
    user_prompt: str = create_user_prompt(challenge)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

        ai_response = completion.choices[0].message.content

        feedback_data = json.loads(ai_response)
        feedback = Feedback(**feedback_data)
        return feedback

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500, detail="Error processing feedback: invalid JSON response"
        )
    except TypeError as e:
        raise HTTPException(
            status_code=500, detail="Error processing feedback: invalid response format"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
