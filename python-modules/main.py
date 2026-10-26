from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import get_agent
from greeting import DEFAULT_GREETING, Greeter

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.get("/hello")
async def hello(name: str = "小微") -> dict[str, str]:
    return {
        "message": Greeter().greet(name),
        "default_greeting": DEFAULT_GREETING,
    }

@app.post("/chat")
async def chat(request: ChatRequest) -> dict[str, str]:
    result = await get_agent().ainvoke({
        "messages": [{"role": "user", "content": request.question}],
    })
    return {"answer": result["messages"][-1].content}
