from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
import logging

from ..models import GroqChatRequest, GroqChatResponse, ErrorResponse
from ..services.groq_service import groq_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/groq",
    tags=["Groq"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)


@router.post(
    "/chat",
    response_model=GroqChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate chat completion",
    description="Generate a chat completion using Groq's language models"
)
async def chat_completion(request: GroqChatRequest):
    """
    Generate a chat completion using Groq API.
    
    - **message**: The user's message to send to Groq
    - **model**: The Groq model to use (default: mixtral-8x7b-32768)
    - **max_tokens**: Maximum tokens to generate (1-32768)
    - **temperature**: Sampling temperature (0.0-2.0)
    - **system_prompt**: Optional system prompt to set context
    """
    try:
        response = await groq_service.chat_completion(request)
        return response
    except Exception as e:
        logger.error(f"Chat completion failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chat completion: {str(e)}"
        )


@router.get(
    "/models",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="Get available models",
    description="Get a list of available Groq models"
)
async def get_models():
    """
    Get a list of available Groq models.
    """
    try:
        models = groq_service.get_available_models()
        return models
    except Exception as e:
        logger.error(f"Failed to get models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve models: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the Groq service is healthy"
)
async def health_check():
    """
    Health check endpoint for Groq service.
    """
    return {"status": "healthy", "service": "groq"} 