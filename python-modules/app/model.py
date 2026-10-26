import os

from langchain_openai import ChatOpenAI

def create_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.environ["DEEPSEEK_MODEL"],
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    )
