from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat completions."""
    message: str
    model: str = "llama-3.1-8b-instant"
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = 0.7
    system_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat completions."""
    content: str
    model: str
    usage: dict 