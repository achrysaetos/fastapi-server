import os
from fastapi import FastAPI, HTTPException
from groq import Groq
from dotenv import load_dotenv
from .models import ChatRequest, ChatResponse
from typing import List, Dict

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# In-memory conversation history
conversation_history: List[Dict[str, str]] = []

# Default settings
DEFAULT_MODEL = "llama-3.1-8b-instant"
DEFAULT_SYSTEM_PROMPT = "You are a helpful, honest, and knowledgeable assistant. Respond clearly, concisely, and accurately. Prioritize usefulness and truthfulness. Ask clarifying questions if needed."

# Create FastAPI app
app = FastAPI(
    title="FastAPI Groq Chat",
    description="Simple chat API with conversation history",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "FastAPI Groq Chat with History",
        "docs": "/docs",
        "endpoints": {
            "chat": "POST /chat",
            "history": "GET /history", 
            "clear": "DELETE /history"
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with Groq with conversation history.
    """
    try:
        # Add user message to history
        conversation_history.append({"role": "user", "content": request.message})
        
        # Prepare messages for API call (include system prompt + full history)
        messages = [{"role": "system", "content": DEFAULT_SYSTEM_PROMPT}] + conversation_history.copy()
        
        # Call Groq API
        response = groq_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
        )
        
        # Get assistant response
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": assistant_message})
        
        # Return response
        return ChatResponse(
            content=assistant_message,
            model=DEFAULT_MODEL,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            conversation_length=len(conversation_history)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/history")
async def get_history():
    """Get the current conversation history."""
    return {
        "conversation_history": conversation_history,
        "message_count": len(conversation_history),
        "user_messages": len([msg for msg in conversation_history if msg["role"] == "user"]),
        "assistant_messages": len([msg for msg in conversation_history if msg["role"] == "assistant"])
    }


@app.delete("/history")
async def clear_history():
    """Clear the conversation history."""
    global conversation_history
    conversation_history = []
    return {"message": "Conversation history cleared"}


@app.get("/models")
async def get_models():
    """Get available Groq models."""
    return [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile", 
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 