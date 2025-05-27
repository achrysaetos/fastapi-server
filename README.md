# FastAPI Groq Integration

A production-ready FastAPI application that provides endpoints to interact with Groq's language models.

## Features

- 🚀 **FastAPI** with automatic API documentation
- 🤖 **Groq Integration** for AI text generation
- 📝 **Pydantic Models** for request/response validation
- 🔧 **Environment Configuration** management
- 📊 **Structured Logging** with proper error handling
- 🌐 **CORS** support for web applications
- 🏥 **Health Checks** for monitoring
- 🔒 **Input Validation** and sanitization

## Project Structure

```
fastapi-server/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── groq.py          # Groq API routes
│   └── services/
│       ├── __init__.py
│       └── groq_service.py  # Groq service logic
├── requirements.txt         # Python dependencies
├── env.example             # Environment variables example
└── README.md
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
cp env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

To get a Groq API key:
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Generate an API key

### 3. Run the Application

```bash
# Development mode with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Chat Completion

Generate text using Groq's language models.

**POST** `/api/v1/groq/chat`

```json
{
  "message": "Hello, how are you?",
  "model": "mixtral-8x7b-32768",
  "max_tokens": 1024,
  "temperature": 0.7,
  "system_prompt": "You are a helpful assistant."
}
```

**Response:**
```json
{
  "content": "Hello! I'm doing well, thank you for asking...",
  "model": "mixtral-8x7b-32768",
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 25,
    "total_tokens": 40
  },
  "finish_reason": "stop"
}
```

### Available Models

Get list of available Groq models.

**GET** `/api/v1/groq/models`

**Response:**
```json
[
  "mixtral-8x7b-32768",
  "llama2-70b-4096",
  "gemma-7b-it",
  "llama3-70b-8192",
  "llama3-8b-8192"
]
```

### Health Check

Check service health.

**GET** `/api/v1/groq/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "groq"
}
```

## Usage Examples

### Python Requests

```python
import requests

# Chat completion
response = requests.post(
    "http://localhost:8000/api/v1/groq/chat",
    json={
        "message": "Explain quantum computing in simple terms",
        "model": "mixtral-8x7b-32768",
        "max_tokens": 500,
        "temperature": 0.7
    }
)

result = response.json()
print(result["content"])
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/groq/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a haiku about coding",
    "model": "mixtral-8x7b-32768",
    "max_tokens": 100,
    "temperature": 0.8
  }'
```

### JavaScript/Fetch

```javascript
const response = await fetch('http://localhost:8000/api/v1/groq/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'What is machine learning?',
    model: 'mixtral-8x7b-32768',
    max_tokens: 300,
    temperature: 0.7
  })
});

const result = await response.json();
console.log(result.content);
```

## Configuration

The application supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | **Required** |

## Error Handling

The API provides structured error responses:

```json
{
  "error": "Error type",
  "detail": "Detailed error message"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid input)
- `422`: Validation error
- `500`: Internal server error

## Development

### Code Structure Best Practices

- **Separation of Concerns**: Models, services, and routes are separated
- **Dependency Injection**: Services are injected into routes
- **Error Handling**: Comprehensive error handling with logging
- **Validation**: Pydantic models for request/response validation
- **Configuration**: Environment-based configuration management

### Adding New Features

1. Add models in `app/models.py`
2. Implement service logic in `app/services/`
3. Create routes in `app/routers/`
4. Include router in `app/main.py`

## Production Deployment

For production deployment:

1. Set `allow_origins` in CORS middleware to specific domains
2. Use environment variables for configuration
3. Set up proper logging and monitoring
4. Use a production ASGI server like Gunicorn with Uvicorn workers
5. Implement rate limiting and authentication as needed

```bash
# Production command example
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## License

This project is licensed under the MIT License. 