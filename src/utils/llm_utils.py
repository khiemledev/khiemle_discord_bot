import openai

from utils.config_utils import get_config

config = get_config()


openai.api_key = config.llm.openai_api_key


def call_chatgpt(prompt: str, temperature: float = 0.9) -> str:
    messages = [
        {
            "role": "system",
            "content": """You are a bot in `Human on The Earth` discord server.
                Your job is to answer all questions from the members of the server.
                You also have to do all the tasks that the members ask you to do.
                """,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
