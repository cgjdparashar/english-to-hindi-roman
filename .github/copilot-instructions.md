# English to Hinglish Translator - AI Agent Instructions

## Project Architecture

This is a **two-stage translation pipeline** that converts English → Hindi (via Google Translate) → Roman script (via ITRANS transliteration). The core translator lives in `utility/translator.py` and is exposed via a FastAPI REST API in `api/`.

**Key Design Decision:** SSL verification is globally disabled in `utility/translator.py` to handle corporate proxy environments. This is intentional for the Google Translate API calls through `deep-translator`.

### Directory Structure
```
utility/          # Core translation logic (translator.py is the main entry point)
api/              # FastAPI application (app.py) and Pydantic models (models.py)
tests/            # All test files (manual tests, no pytest framework)
docs/             # Documentation including SSL troubleshooting and API guides
```

## Critical Workflows

### Running the API
```bash
# Development mode with auto-reload
uv run uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload

# Access Swagger UI at http://localhost:8000/docs
```

### Running Tests
Tests are **direct Python scripts**, not pytest-based. Run with:
```bash
uv run python tests/test_translator.py
uv run python tests/test_api_endpoint.py
```

### Installing Dependencies
This project uses **uv** (not pip/poetry). To add dependencies:
```bash
uv add package-name
```

## Project-Specific Conventions

### Import Pattern for Translation Function
Always import from `utility.translator`, never from `main`:
```python
from utility.translator import english_to_hinglish
```

### SSL Handling
The translator **intentionally disables SSL verification** at the module level in `utility/translator.py`:
- `urllib3` warnings suppressed
- `requests.Session.request` patched to set `verify=False`
- This is documented in `docs/SSL_TROUBLESHOOTING.md`

**Do not "fix" this by re-enabling SSL** without understanding the corporate proxy context.

### API Response Schema
The `/translate` endpoint returns `TranslationResponse` with:
- `hinglish_text` (not `translated_text` - check `api/models.py`)
- `success` boolean flag
- Optional `error` field

### Translation Output Format
The transliteration uses **ITRANS scheme**, which produces output like:
- "hello" → "namaste"
- "how are you" → "Apa kaise haiM" (note capital letters for aspirated sounds)

## Integration Points

### External Dependencies
- **deep-translator**: Wraps Google Translate API (network-dependent, may fail with SSL issues)
- **indic-transliteration**: Local library, no network calls, uses `sanscript.DEVANAGARI` → `sanscript.ITRANS`

### Cross-Component Communication
`api/app.py` imports directly from `utility/translator.py`. There's no service layer or dependency injection - it's a simple direct import pattern.

## Common Pitfalls

1. **Import Errors**: If you see `ModuleNotFoundError: No module named 'main'`, you're using old imports. Update to `from utility.translator import english_to_hinglish`.

2. **SSL Errors**: If translation fails with SSL certificate errors:
   - Check `docs/SSL_TROUBLESHOOTING.md`
   - Verify the SSL patches in `utility/translator.py` are intact
   - Try running `utility/fix_ssl.py` for diagnostics

3. **Empty Translations**: The function returns `""` for empty input by design (see `utility/translator.py:53-54`).

4. **Test Execution**: Tests print output to console and use basic assertions - they're meant to be run directly, not through a test runner.

## Development Tips

- The API supports CORS with `allow_origins=["*"]` - change this in production (`api/app.py:26`)
- Health check endpoint: `GET /health` (useful for monitoring)
- The translator maintains no state - each call is independent
- Error messages are returned as strings starting with "Translation error:" (see `utility/translator.py:71`)
