from fastapi import APIRouter
from pydantic import BaseModel
from ..services.ai_service import AIService

router = APIRouter()
ai = AIService()

class AngleRequest(BaseModel):
    topic: str

@router.post("/generate")
async def generate(request: AngleRequest):
    print(f"Received topic: {request.topic}")
    result = await ai.generate_angles(request.topic)
    print(f"Generated: {result.get('topic')}")
    return result
