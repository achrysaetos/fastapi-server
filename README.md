# FastAPI Groq Integration

A simple, clean FastAPI application to query Groq's language models.

## Features

- 🚀 Simple FastAPI app with auto-generated docs
- 🤖 Direct Groq API integration
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

Send a message to Groq and get an AI response.

**Request:**
```json
{
  "message": "Hello, how are you?",
  "model": "llama-3.1-8b-instant",
  "max_tokens": 1024,
  "temperature": 0.7,
  "system_prompt": "You are a helpful assistant."
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
  }
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

## Usage Examples

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "Explain Python in one sentence"}
)
print(response.json()["content"])
```

### cURL
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a haiku about coding"}'
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'What is FastAPI?' })
});
const result = await response.json();
console.log(result.content);
```

That's it! Simple and functional. 🚀 