import json

from g4f.client import Client
from main import Challenge

client = Client()


def create_prompt(challenge: Challenge):
    # Read the prompt from prompt.txt
    with open('prompt.txt', 'r') as file:
        base_prompt = file.read()

    # Append the dynamic inputs from the Challenge object
    full_prompt = f"{base_prompt}\n\nThe programming language is: {challenge.programming_language}\n" \
                  f"The question posed is: {challenge.question}\n" \
                  f"The user’s submitted answer is: {challenge.answer}\n" \
                  f"{f'- Additional notes: {challenge.notes}' if challenge.notes else ''}"

    return full_prompt


def get_ai_response(challenge: Challenge) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": create_prompt(challenge)}],
    )

    return chat_completion.choices[0].message.content or ""


def get_response(challenge: Challenge) -> dict:
    ai_response = get_ai_response(challenge)

    try:
        json_response = json.loads(ai_response)
    except json.JSONDecodeError:
        return {
            "error": "Invalid response format from AI",
            "raw_response": ai_response
        }

    return json_response

