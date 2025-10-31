# API Documentation

## English to Hinglish Translator API

A RESTful API service for translating English text to Hinglish (Hindi in Roman script).

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Health Check

#### GET `/`
Root endpoint that returns API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "message": "English to Hinglish Translator API is running"
}
```

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "message": "Service is running and ready to translate"
}
```

---

### 2. Translation Endpoint

#### POST `/translate`
Translate English text to Hinglish using JSON payload.

**Request Body:**
```json
{
  "text": "hello how are you"
}
```

**Success Response:**
```json
{
  "original_text": "hello how are you",
  "hinglish_text": "namaste Apa kaise ho",
  "success": true,
  "error": null
}
```

**Error Response:**
```json
{
  "original_text": "hello how are you",
  "hinglish_text": "",
  "success": false,
  "error": "Translation error: ..."
}
```

---

## Running the API

### Start the Server

```bash
# Using uvicorn directly
uv run uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

# Or run the app.py file
uv run python api/app.py
```

### Access the API

- **API Docs (Swagger UI):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## Usage Examples

### Using cURL

```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "hello how are you"}'
```

### Using Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/translate",
    json={"text": "hello how are you"}
)
print(response.json())
```

### Using JavaScript Fetch

```javascript
fetch('http://localhost:8000/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'hello how are you'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Error Handling

### HTTP Status Codes

- `200 OK` - Successful translation
- `400 Bad Request` - Invalid input (empty text, too long, etc.)
- `500 Internal Server Error` - Translation service error

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## CORS

The API is configured to allow CORS from all origins (`*`). For production, update the `allow_origins` in `api/app.py` to specific domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Rate Limiting

Currently, there's no rate limiting. For production use, consider adding rate limiting middleware.

---

## Testing the API

1. Start the server
2. Visit http://localhost:8000/docs for interactive API documentation
3. Try the endpoints directly from the Swagger UI
4. Or use the provided cURL/Python examples above

---

## Production Deployment

### Using Docker (recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

Consider adding configuration through environment variables for production:
- API keys (if using paid translation services)
- CORS origins
- SSL certificates path
- Rate limiting settings
