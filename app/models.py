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


class NewsSearchRequest(BaseModel):
    """Request model for news search."""
    keyword: str
    max_results: int = 5


class NewsArticle(BaseModel):
    """Model for a news article."""
    title: str
    url: str
    snippet: str
    source: str


class NewsSearchResponse(BaseModel):
    """Response model for news search."""
    summary: str
    keyword: str
    articles: List[NewsArticle]
    model: str
    usage: dict
