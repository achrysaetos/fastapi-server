import os
from fastapi import FastAPI, HTTPException
from groq import Groq
from dotenv import load_dotenv
from .models import ChatRequest, ChatResponse

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Create FastAPI app
app = FastAPI(
    title="FastAPI Groq Integration",
    description="Simple FastAPI app to query Groq models",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "FastAPI Groq Integration",
        "docs": "/docs",
        "chat_endpoint": "/chat"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with Groq models.
    
    Send a message and get an AI response using Groq's language models.
    """
    try:
        # Prepare messages
        messages = []
        
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        
        messages.append({"role": "user", "content": request.message})
        
        # Call Groq API
        response = groq_client.chat.completions.create(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Return response
        return ChatResponse(
            content=response.choices[0].message.content,
            model=request.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/models")
async def get_models():
    """Get available Groq models."""
    return [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile", 
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 