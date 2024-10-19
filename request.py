from g4f.client import Client

client = Client()


def get_response() -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}],
    )

    return chat_completion.choices[0].message.content or ""


def get_grade(response: str):
    pass

