import os

from fastapi import FastAPI
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

app = FastAPI()

agent = create_agent(
    model=ChatOpenAI(
        model=os.environ["DEEPSEEK_MODEL"],
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    ),
    system_prompt="你是一名简洁、可靠的 Python 学习助手。",
)

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(request: ChatRequest) -> dict[str, str]:
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": request.question}],
    })
    return {"answer": result["messages"][-1].content}
