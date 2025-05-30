# FastAPI Groq Chat

A simple FastAPI backend for chatting with Groq's language models with conversation history.

* Benefits of using Groq API over ChatGPT's built-in shortcut: immediate responses, conversational memory, smarter model, more control over instructions, no need to leave the app open on your phone, won't spam new chat topics on your sidebar in the web. 

* Benefits of calling Siri over triggering manually: more seamless and don't need to tap, but slower speaking rate

## Features

- 🚀 Simple FastAPI app with auto-generated docs
- 🤖 Direct Groq API integration
- 💬 Automatic conversation history management
- 📰 News search with AI summarization.
- 📝 Clean request/response models
- 🔧 Environment-based configuration

## Project Structure

```
fastapi-server/
├── app/
│   ├── main.py      # Main FastAPI application
│   └── models.py    # Request/response models
├── requirements.txt # Dependencies
├── env.example     # Environment template
└── README.md
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Environment

```bash
cp env.example .env
```

Edit `.env` and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key at [Groq Console](https://console.groq.com/)

### 3. Run the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Visit http://localhost:8000/docs for the interactive API documentation.

## API Endpoints

### POST `/chat`

Send a message and get an AI response. Conversation history is automatically maintained.

**Request:**
```json
{
  "message": "Hello, how are you?"
}
```

**Response:**
```json
{
  "content": "Hello! I'm doing well, thank you for asking...",
  "model": "llama-3.1-8b-instant",
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 25,
    "total_tokens": 40
  },
  "conversation_length": 2
}
```

### GET `/history`

Get the current conversation history and stats.

**Response:**
```json
{
  "conversation_history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
  ],
  "message_count": 2,
  "user_messages": 1,
  "assistant_messages": 1
}
```

### DELETE `/history`

Clear the conversation history to start fresh.

**Response:**
```json
{
  "message": "Conversation history cleared"
}
```

### GET `/models`

Get list of available Groq models.

**Response:**
```json
[
  "llama-3.1-8b-instant",
  "llama-3.1-70b-versatile",
  "mixtral-8x7b-32768",
  "gemma2-9b-it"
]
```

### POST `/news-search`

Search for news articles by keyword and get an AI-powered summary. Uses web search to find recent articles and Groq's LLM to generate concise summaries.

**Request:**
```json
{
  "keyword": "artificial intelligence",
  "max_results": 5
}
```

**Response:**
```json
{
  "summary": "AI-generated summary of the news articles about the keyword...",
  "keyword": "artificial intelligence",
  "articles": [
    {
      "title": "Article title here",
      "url": "https://example.com/article",
      "snippet": "Brief preview of the article content...",
      "source": "example.com"
    }
  ],
  "model": "llama-3.3-70b-versatile",
  "usage": {
    "prompt_tokens": 253,
    "completion_tokens": 124,
    "total_tokens": 377
  }
}
```

**Parameters:**
- `keyword` (required): The search term for finding news articles
- `max_results` (optional): Maximum number of articles to return (default: 5)

## Usage Examples

### Python
```python
import requests

# Start a conversation
response1 = requests.post(
    "http://localhost:8000/chat",
    json={"message": "My name is Alice"}
)
print(response1.json()["content"])

# Continue the conversation (remembers your name)
response2 = requests.post(
    "http://localhost:8000/chat", 
    json={"message": "What's my name?"}
)
print(response2.json()["content"])  # Should mention "Alice"

# Check conversation history
history = requests.get("http://localhost:8000/history")
print(f"Total messages: {history.json()['message_count']}")

# Clear history
requests.delete("http://localhost:8000/history")
```

### cURL
```bash
# Send a message
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me a joke"}'

# Continue conversation
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me another one"}'

# View history
curl "http://localhost:8000/history"

# Clear history
curl -X DELETE "http://localhost:8000/history"

# Search news
curl -X POST "http://localhost:8000/news-search" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "artificial intelligence", "max_results": 3}'
```

### JavaScript
```javascript
// Send a message
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Hello, I am learning JavaScript' })
});
const result = await response.json();
console.log(result.content);

// Ask a follow-up (AI remembers the context)
const followUp = await fetch('http://localhost:8000/chat', {
  method: 'POST', 
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Can you help me with arrays?' })
});
const followUpResult = await followUp.json();
console.log(followUpResult.content);
```

## How It Works

1. **Simple Input**: Just send a message string - no need to manage conversation history yourself
2. **Automatic History**: The server automatically maintains conversation context
3. **Persistent Context**: Each new message includes the full conversation history
4. **Easy Reset**: Clear history anytime with `DELETE /history`

## Default Settings

- **Model**: `llama-3.1-8b-instant` (fast and efficient)
- **Max Tokens**: 1024
- **Temperature**: 0.7 (balanced creativity)
- **System Prompt**: "You are a helpful assistant."

Perfect for building chatbots, AI assistants, or any conversational AI application! 🚀 
