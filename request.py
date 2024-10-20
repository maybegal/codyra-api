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


default_prompt = """You are an expert programming tutor specializing in providing concise, accurate feedback on 
coding challenges. Your responses should be clear, direct, and tailored to the specific programming language and 
challenge presented. Focus solely on the task at hand without additional commentary or explanations unless explicitly 
requested."""

prompts = {
    "grade": "Assign an integer grade from 0 to 100 for the following solution. Base your grade strictly on code "
             "correctness, efficiency, and adherence to the problem requirements. Provide only the numerical grade "
             "without explanation.",
    "overview": "Identify and explain the single most crucial programming concept required to solve this challenge. "
                "Limit your response to two sentences focusing solely on the core idea.",
    "strategy": "Outline a step-by-step approach to solve this programming challenge. Provide a maximum of three "
                "concise bullet points describing the key steps.",
    "solution": "Describe the correct solution to this programming challenge in plain English. Use no more than three "
                "sentences and avoid any code or pseudo-code.",
    "code_solution": "Write the optimal code solution for this challenge in the specified programming language. "
                     "Provide only the code without comments or explanations.",
    "growth": "Identify the single most important area for improvement based on the user's solution. Suggest one "
              "specific, actionable practice exercise to address this area. Limit your response to two sentences."
}


def create_prompt(prompt: str, challenge: Challenge):
    challenge_prompt = f"Programming language: {challenge.programming_language}\n" \
           f"The question: {challenge.question}\n" \
           f"User's answer: {challenge.answer}\n" \
           f"Additional notes: {challenge.notes}"

    return default_prompt + "\n" + prompt + "\n\n" + challenge_prompt

