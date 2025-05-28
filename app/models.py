from pydantic import BaseModel
from typing import List, Dict


class ChatRequest(BaseModel):
    """Request model for chat - only requires a message."""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat completions."""
    content: str
    model: str
    usage: dict
    conversation_length: int 