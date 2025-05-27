import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Groq API configuration
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    DEFAULT_MODEL: str = "mixtral-8x7b-32768"
    MAX_TOKENS_LIMIT: int = 32768
    
    # FastAPI configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Groq Integration"
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present."""
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")
        return True


settings = Settings() 