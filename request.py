import json
from g4f.client import Client
from models import Challenge

client = Client()


async def get_ai_response(prompt: str) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    return chat_completion.choices[0].message.content.strip()

grade_prompt = """
Assign an integer grade from 0 to 100 for the following solution. Base your grade strictly on code 
correctness, efficiency, and adherence to the problem requirements. Provide only the numerical grade without 
explanation.
"""


def create_prompt(prompt: str, challenge: Challenge):
    challenge_prompt = f"Programming language: {challenge.programming_language}\n" \
           f"The question: {challenge.question}\n" \
           f"User's answer: {challenge.answer}\n" \
           f"Additional notes: {challenge.notes}"

    if prompt != prompts["grade"]:
        return default_prompt + "\n" + format_prompt + "\n" + prompt + "\n\n" + challenge_prompt

    return default_prompt + "\n" + prompt + "\n\n" + challenge_prompt

