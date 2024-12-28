"""
This module handles interactions with the AI client to generate responses based on programming challenges.
"""

from g4f.client import Client
from models import Challenge, Feedback
from typing import Optional

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


async def get_ai_response(user_prompt: str) -> str:
    """
    Sends a request to the AI model with the given system and user prompts.
    Returns the AI's response as a string.
    """
    # Load the prompt from the file
    system_prompt = load_prompt_file()

    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    # Return the AI's response, stripping any leading/trailing whitespace
    return chat_completion.choices[0].message.content.strip()


def create_user_prompt(challenge: Challenge) -> str:
    """
    Constructs a user prompt string from a Challenge object.
    """
    user_prompt = (
        f"Programming language: {challenge.programming_language}\n"
        f"The question: {challenge.question}\n"
        f"User's answer: {challenge.answer}\n"
        f"Additional notes: {challenge.notes}"
    )

    return user_prompt
