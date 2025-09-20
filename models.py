from typing import List, Optional
from pydantic import BaseModel

class ChatMessage(BaseModel):
    """Model for chat messages"""
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    """Model for chat response"""
    response: str
    conversation_id: Optional[str] = None

class HealthResponse(BaseModel):
    """Model for health check responses"""
    status: str
    message: str