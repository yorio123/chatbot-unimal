from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import Chatbot

app = FastAPI(
    title="UNIMALBOT API",
    version="1.0.0",
    description="REST API Chatbot Universitas Malikussaleh"
)

bot = Chatbot()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "success": True,
        "message": "UNIMALBOT API is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    result = bot.reply(request.message)
    print(result)
    return result