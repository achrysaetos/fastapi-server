from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class GroqChatRequest(BaseModel):
    """Request model for Groq chat completions."""
    message: str = Field(..., description="The user's message to send to Groq")
    model: str = Field(default="llama-3.1-8b-instant", description="The Groq model to use")
    max_tokens: Optional[int] = Field(default=1024, ge=1, le=32768, description="Maximum tokens to generate")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    system_prompt: Optional[str] = Field(default=None, description="Optional system prompt")


class GroqChatResponse(BaseModel):
    """Response model for Groq chat completions."""
    content: str = Field(..., description="The generated response content")
    model: str = Field(..., description="The model used for generation")
    usage: Dict[str, Any] = Field(..., description="Token usage information")
    finish_reason: str = Field(..., description="Reason why the generation finished")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Additional error details") 