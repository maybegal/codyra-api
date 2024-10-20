from g4f.client import Client
from models import Challenge
from typing import Optional


client = Client()


def load_prompt_file() -> Optional[str]:
    with open("prompt.txt", "r") as file:
        return file.read()


CONTENT_PROMPT: Optional[str] = load_prompt_file()

GRADE_PROMPT = """
Assign an integer grade from 0 to 100 for the following solution. Base your grade strictly on code 
correctness, efficiency, and adherence to the problem requirements. Provide only the numerical grade without 
explanation.
"""


async def get_ai_response(prompt: str) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    return chat_completion.choices[0].message.content.strip()


def create_prompt(prompt: str, challenge: Challenge):
    challenge_prompt = f"Programming language: {challenge.programming_language}\n" \
           f"The question: {challenge.question}\n" \
           f"User's answer: {challenge.answer}\n" \
           f"Additional notes: {challenge.notes}"

    if prompt == GRADE_PROMPT:
        return GRADE_PROMPT + "\n" + challenge_prompt

    return prompt + "\n" + challenge_prompt

