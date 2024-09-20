from fastapi import APIRouter, Body
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from services.service_ai import get_chat_response
import time

router = APIRouter()

class MessageInput(BaseModel):
    message: str

def generate_response(user_input: str):
    response = get_chat_response(user_input)

    for word in response.split():
        yield word + " "
        time.sleep(0.01)

@router.post("/chat/")
async def chat(input: MessageInput):
    return StreamingResponse(generate_response(input.message), media_type="text/plain")
