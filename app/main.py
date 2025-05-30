import os
import re
import httpx
import urllib.parse
from fastapi import FastAPI, HTTPException
from groq import Groq
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from .models import ChatRequest, ChatResponse, NewsSearchRequest, NewsSearchResponse, NewsArticle
from typing import List, Dict

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# In-memory conversation history
conversation_history: List[Dict[str, str]] = []

# Default settings
DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_SYSTEM_PROMPT = "You are my helpful and enthusiastic assistant. Provide accurate, relevant answers in a clear, concise, and conversational tone. Limit each response to the essential information needed to address my question (no more than a few sentences max)."

# Create FastAPI app
app = FastAPI(
    title="FastAPI Groq Chat",
    description="Simple chat API with conversation history",
    version="1.0.0"
)


async def search_news_web(keyword: str, max_results: int = 5):
    """
    Search for news articles using DuckDuckGo search.
    
    Args:
        keyword: The search keyword
        max_results: Maximum number of results to return
        
    Returns:
        List of NewsArticle objects
    """
    try:
        # Format the search query for news
        search_query = f"{keyword} news"
        encoded_query = urllib.parse.quote_plus(search_query)
        search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        # Make the HTTP request
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                search_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            )
            response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="result")
        
        articles = []
        for result in results[:max_results]:
            # Extract title, URL, and snippet
            title_elem = result.find("a", class_="result__a")
            snippet_elem = result.find("a", class_="result__snippet")
            
            if title_elem and snippet_elem:
                title = title_elem.text.strip()
                url = title_elem.get("href", "")
                
                # Clean up the URL (DuckDuckGo uses redirects)
                if url.startswith("/"):
                    url_match = re.search(r'uddg=([^&]+)', url)
                    if url_match:
                        url = urllib.parse.unquote(url_match.group(1))
                
                snippet = snippet_elem.text.strip()
                
                # Try to extract the source domain from the URL
                source = "Unknown"
                try:
                    source_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
                    if source_match:
                        source = source_match.group(1)
                except:
                    pass
                
                articles.append(NewsArticle(
                    title=title,
                    url=url,
                    snippet=snippet,
                    source=source
                ))
        
        return articles
    
    except httpx.RequestError as e:
        # Handle network errors
        raise HTTPException(status_code=503, detail=f"Error fetching news: {str(e)}")
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"Error processing news search: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "FastAPI Groq Chat with History",
        "docs": "/docs",
        "endpoints": {
            "chat": "POST /chat",
            "history": "GET /history", 
            "clear": "DELETE /history",
            "news-search": "POST /news-search"
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


@app.post("/news-search", response_model=NewsSearchResponse)
async def news_search(request: NewsSearchRequest):
    """
    Search for news articles based on a keyword and summarize them using LLM.
    """
    try:
        # Search for news articles
        articles = await search_news_web(request.keyword, request.max_results)
        
        if not articles:
            raise HTTPException(status_code=404, detail=f"No news found for keyword: {request.keyword}")
        
        # Prepare content for LLM summarization
        article_text = "\n\n".join([
            f"Title: {article.title}\nSource: {article.source}\nSnippet: {article.snippet}"
            for article in articles
        ])
        
        # Prepare system prompt for news summarization
        system_prompt = """
        You are a helpful news assistant. Analyze the following news articles and provide a concise summary.
        Focus on the key points, trends, and important information.
        Keep your summary clear, factual, and under 200 words.
        """
        
        # Prepare user message with the articles to summarize
        user_message = f"Please summarize these news articles about '{request.keyword}':\n\n{article_text}"
        
        # Call Groq API for summarization
        response = groq_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
        )
        
        # Get summary from LLM
        summary = response.choices[0].message.content
        
        # Return response
        return NewsSearchResponse(
            summary=summary,
            keyword=request.keyword,
            articles=articles,
            model=DEFAULT_MODEL,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"Error processing news search: {str(e)}")


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
        "llama-3.3-70b-versatile", 
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 
