# English to Hinglish Translator - AI Agent Instructions

## Project Architecture

This is a **comprehensive text processing and translation pipeline** with three main components:

1. **Core Translation Pipeline**: English → Hindi (via Google Translate) → Roman script (via ITRANS transliteration)
2. **File Processing Pipeline**: Split large files into manageable chunks with smart boundary detection
3. **REST API Interface**: FastAPI server exposing translation services

**Key Design Decision:** SSL verification is globally disabled in `utility/translator.py` to handle corporate proxy environments. This is intentional for the Google Translate API calls through `deep-translator`.

### Directory Structure
```
utility/          # Core utilities (translator.py, file processing, demos)
api/              # FastAPI application (app.py) and Pydantic models
tests/            # Direct Python test scripts (no pytest framework)
docs/             # Comprehensive documentation and guides
story/            # File processing workspace (input/ and output/ folders)
  ├── input/      # Raw story files for processing
  └── output/     # Split file chunks organized by story name
```

## Critical Workflows

### Running the API
```bash
# Development mode with auto-reload
uv run uvicorn api.app:app --host 127.0.0.1 --port 8000 --reload

# Access Swagger UI at http://localhost:8000/docs
```

### File Processing Workflows
```bash
# Split any file (absolute or relative paths)
python utility/generic_file_splitter.py "path/to/file.txt" --chunk-size 2000

# Process files programmatically from project root
python script_name.py  # (never from subdirectories due to import issues)

# Demo file processing features
python utility/demo_generic_splitter.py
python utility/demo_file_translator.py
```

### Running Tests
Tests are **direct Python scripts**, not pytest-based:
```bash
# Run from project root only (import dependencies)
python tests/test_translator.py
python tests/test_file_splitter.py
python tests/test_api_endpoint.py

# Set PYTHONPATH for scripts in subdirectories
$env:PYTHONPATH="$PWD"; python tests/some_test.py
```

### Installing Dependencies
This project uses **uv** (not pip/poetry):
```bash
uv add package-name
```

## Project-Specific Conventions

### Import Pattern for Translation Function
Always import from `utility.translator`, never from `main`:
```python
from utility.translator import english_to_hinglish
```

### Critical Path Handling Pattern for Scripts in Subdirectories
Scripts outside the project root need path setup:
```python
import sys
from pathlib import Path

# Add project root to Python path (required for utility imports)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now imports work
from utility.generic_file_splitter import split_any_file
```

### File Processing Auto-Detection Patterns
- **Input paths**: `story/input/filename.txt` → auto-outputs to `story/output/filename/`
- **Generic paths**: Any path → creates `output/` folder in same directory
- **Naming**: Uses filename stem (no extension) as folder name automatically

### SSL Handling
The translator **intentionally disables SSL verification** in `utility/translator.py`. **Do not "fix" this by re-enabling SSL** without understanding the corporate proxy context.

### API Response Schema
The `/translate` endpoint returns `TranslationResponse` with:
- `hinglish_text` (not `translated_text` - check `api/models.py`)
- `success` boolean flag
- Optional `error` field

### Translation Output Format
The transliteration uses **ITRANS scheme** producing output like:
- "hello" → "namaste"  
- "how are you" → "Apa kaise haiM" (capital letters for aspirated sounds)

## Integration Points

### External Dependencies
- **deep-translator**: Wraps Google Translate API (network-dependent, may fail with SSL issues)
- **indic-transliteration**: Local library, no network calls, uses `sanscript.DEVANAGARI` → `sanscript.ITRANS`

### Cross-Component Communication
Direct imports with no service layer - `api/app.py` imports from `utility/translator.py`. File processing utilities chain together:
```python
# Common integration pattern for processing + translation
result = split_any_file("input.txt")  # Split file
for i in range(1, result['files_created'] + 1):
    chunk_text = read_file(f"{i}.txt")
    translated = english_to_hinglish(chunk_text)
```

### File Processing Result Patterns
All file utilities return consistent result dictionaries:
```python
{
    "success": bool,
    "output_folder": str,  # Always provided
    "files_created": int,
    "total_chars": int,
    "error": str  # Only if success=False
}
```

## Common Pitfalls

1. **Import Errors**: If you see `ModuleNotFoundError: No module named 'utility'`, you're using old imports. Update to `from utility.translator import english_to_hinglish`.

2. **Path Resolution Issues**: Scripts in subdirectories (like `mytest/`) fail without proper path setup:
   ```python
   # Always add this for scripts outside project root
   project_root = Path(__file__).parent.parent
   sys.path.insert(0, str(project_root))
   ```

3. **File Splitting Context**: Use `split_any_file()` convenience function, not `split_file_generic()` directly. Auto-detection works best with `story/input/*.txt` → `story/output/*/` pattern.

4. **SSL Errors**: If translation fails with SSL certificate errors:
   - Check `docs/SSL_TROUBLESHOOTING.md`
   - Verify the SSL patches in `utility/translator.py` are intact
   - Try running `utility/fix_ssl.py` for diagnostics

5. **Empty Translations**: The function returns `""` for empty input by design (see `utility/translator.py:53-54`).

6. **Test Execution**: Tests print output to console and use basic assertions - they're meant to be run directly, not through a test runner.

## Development Tips

### File Processing Patterns
- **File splitting**: `split_any_file()` handles both absolute and relative paths with auto-detection
- **Batch processing**: Chain file splitting → translation for large document workflows
- **Smart chunking**: Files split at sentence boundaries (max 2000 chars, configurable)
- **Output organization**: Auto-creates `story/output/filename/1.txt, 2.txt...` structure

### API Integration
- The API supports CORS with `allow_origins=["*"]` - change this in production (`api/app.py:26`)
- Health check endpoint: `GET /health` (useful for monitoring)
- The translator maintains no state - each call is independent
- Error messages are returned as strings starting with "Translation error:" (see `utility/translator.py:71`)

### Demo Scripts for Learning
- `utility/demo_generic_splitter.py` - Shows all file splitting patterns
- `utility/demo_file_translator.py` - Demonstrates file translation workflows
- `tests/split_story_31_10.py` - Real-world example of processing large story files
