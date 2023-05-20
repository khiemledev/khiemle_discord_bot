import openai

from utils.config_utils import get_config

config = get_config()


openai.api_key = config.llm.openai_api_key


def call_chatgpt(
    prompt: str,
    temperature: float = 0.9,
    instruction: str = None,
) -> str:
    """Call ChatGPT and return response in text"""

    if instruction is None:
        instruction = """You are a bot in `Human on The Earth` discord server.
                Your job is to answer all questions from the members of the server.
                You also have to do all the tasks that the members ask you to do.
                """  # noqa: E501

    messages = [
        {
            "role": "system",
            "content": instruction,
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


def call_chatgpt_bot_mentioned(history: str, message: str):
    instruction = f"""Bạn là bot trong server `Human on The Earth`. Bạn vừa được
    một người nào đó mention. Nhiệm vụ của bạn là phải trả lời người đó một
    cách vui vẻ và lịch sự. Bên dưới đây là nội dung của cuộc trò truyện,
    cuộc trò truyện được đặt trong dấu --- ---:
    ---
    {history}
    ---\n"""  # noqa: E501

    message = f"""
    Đây là tin nhắn của người mention bạn:
    ---
    {message}
    ---

    Vui lòng xuất ra nội dung tin nhắn theo định dạng sau:
    ---
    tin_nhắn_bạn_trả_lời_lại_người_mention_bạn
    ---

    Lưu ý không đề cập người gửi là ai trong tin nhắn của bạn và không bao gồm
    dấu <> trong câu trả lời.
    """

    return call_chatgpt(
        message,
        instruction=instruction,
        temperature=0.1,
    )
