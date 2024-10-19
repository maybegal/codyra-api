import json
from g4f.client import Client
from models import Challenge

client = Client()


def get_ai_response(prompt: str) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )

    return chat_completion.choices[0].message.content.strip()


default_prompt = ""

prompts = {
    "grade": "Please evaluate the following programming challenge and provide an integer grade (0-100) based on the accuracy and completeness of the user's solution:",
    "overview": "Provide an overview of the problem posed in the following programming challenge. Explain the core concept that the user needs to understand:",
    "strategy": "Based on the programming challenge below, provide a strategy that the user should follow to successfully solve this problem. Explain how they should approach it and what techniques they could use:",
    "solution": "Review the user's answer to the following programming challenge and provide a detailed explanation of what a correct solution would look like in pure English:",
    "code_solution": "Provide the correct code solution for the following programming challenge. Ensure that the solution is written in the specified programming language and that it addresses the problem accurately:",
    "growth": "Based on the user's performance on the following programming challenge, provide constructive feedback on how they can improve their understanding of the problem and related concepts. Offer suggestions for further practice or study areas:"
}


def create_prompt(prompt: str, challenge: Challenge):
    challenge_prompt = f"Programming language: {challenge.programming_language}\n" \
           f"The question: {challenge.question}\n" \
           f"User's answer: {challenge.answer}\n" \
           f"{f"Additional notes: {challenge.notes}" if challenge.notes else ""}"

    return default_prompt + "\n" + prompt + "\n\n" + challenge_prompt


def get_grade(challenge: Challenge):
    prompt = create_prompt(prompts["grade"], challenge)
    response = get_ai_response(prompt)

    return int(response)


def get_overview(challenge: Challenge):
    prompt = create_prompt(prompts["overview"], challenge)
    response = get_ai_response(prompt)

    return response


def get_strategy(challenge: Challenge):
    prompt = create_prompt(prompts["strategy"], challenge)
    response = get_ai_response(prompt)

    return response


def get_solution(challenge: Challenge):
    prompt = create_prompt(prompts["solution"], challenge)
    response = get_ai_response(prompt)

    return response


def get_code_solution(challenge: Challenge):
    prompt = create_prompt(prompts["code_solution"], challenge)
    response = get_ai_response(prompt)

    return response


def get_growth(challenge: Challenge):
    prompt = create_prompt(prompts["growth"], challenge)
    response = get_ai_response(prompt)

    return response
