from functools import cache

from langchain.agents import create_agent

from .model import create_model
from .prompts import SYSTEM_PROMPT

@cache
def get_agent():
    return create_agent(
        model=create_model(),
        system_prompt=SYSTEM_PROMPT,
    )
