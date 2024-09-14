from fastapi import APIRouter
from pydantic import BaseModel
from services.service_ai import get_chat_response

router = APIRouter()

class MessageInput(BaseModel):
    message: str

@router.post("/chat/")
async def chat(input: MessageInput):
    print(f"User input: {input.message}")
    response = get_chat_response(input.message)
    return {"response": response}
