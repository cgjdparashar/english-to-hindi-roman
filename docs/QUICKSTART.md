# API Quick Reference

## Start Server
```bash
uv run uvicorn api.app:app --reload --host 127.0.0.1 --port 8000
```

## Access Points
- Swagger UI: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## cURL Examples

### Health Check
```bash
curl http://localhost:8000/health
```

### POST Translation
```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "hello how are you"}'
```



## Python Example
```python
import requests

response = requests.post(
    "http://localhost:8000/translate",
    json={"text": "hello how are you"}
)
print(response.json())
```

## Test API
```bash
uv run python api/test_api.py
```
