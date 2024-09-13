from fastapi import APIRouter
from app.services.chat_service import get_chat_response

router = APIRouter()

@router.post("/chat/")
async def chat(user_input: str):
    response = get_chat_response(user_input)
    return {"response": response}
