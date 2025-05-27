import logging
from groq import Groq
from typing import Optional, List, Dict, Any
from ..config import settings
from ..models import GroqChatRequest, GroqChatResponse

logger = logging.getLogger(__name__)


class GroqService:
    """Service class for interacting with the Groq API."""
    
    def __init__(self):
        """Initialize the Groq client."""
        self.client = Groq(api_key=settings.GROQ_API_KEY)
    
    async def chat_completion(self, request: GroqChatRequest) -> GroqChatResponse:
        """
        Generate a chat completion using Groq API.
        
        Args:
            request: The chat completion request
            
        Returns:
            GroqChatResponse: The response from Groq
            
        Raises:
            Exception: If the API call fails
        """
        try:
            # Prepare messages
            messages = []
            
            # Add system prompt if provided
            if request.system_prompt:
                messages.append({
                    "role": "system",
                    "content": request.system_prompt
                })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": request.message
            })
            
            # Make API call
            response = self.client.chat.completions.create(
                model=request.model,
                messages=messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                stream=False
            )
            
            # Extract response data
            content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            
            logger.info(f"Groq API call successful. Model: {request.model}, Tokens: {usage['total_tokens']}")
            
            return GroqChatResponse(
                content=content,
                model=request.model,
                usage=usage,
                finish_reason=finish_reason
            )
            
        except Exception as e:
            logger.error(f"Groq API call failed: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available Groq models.
        
        Returns:
            List of available model names
        """
        # Common Groq models (you can extend this list)
        return [
            "mixtral-8x7b-32768",
            "llama2-70b-4096",
            "gemma-7b-it",
            "llama3-70b-8192",
            "llama3-8b-8192"
        ]


# Global instance
groq_service = GroqService() 