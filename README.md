# English to Hinglish (Hindi-Roman) Translator

A comprehensive Python application that converts English text to Hinglish (Hindi in Roman script) using open-source libraries. Now includes powerful file processing utilities for handling large text files.

## Features

### Core Translation
- Translates any English text to Hindi using `deep-translator`
- Transliterates Hindi (Devanagari) to Roman script (Hinglish) using `indic-transliteration`
- No hardcoded translations - fully dynamic translation
- REST API with FastAPI for web integration

### File Processing Utilities
- **File Splitter**: Split large text files (up to 300k characters) into smaller chunks
- **Generic File Splitter**: Universal file splitter supporting any file path (absolute/relative)
- **File Translator**: Translate entire text files to Hinglish
- **Smart Text Chunking**: Breaks text at sentence boundaries for better readability

### Testing & API
- Comprehensive test suite for all components
- Interactive API documentation with Swagger UI
- Health monitoring and error handling

## Libraries Used

- **deep-translator**: Provides translation from English to Hindi via Google Translate API
- **indic-transliteration**: Handles Devanagari to Roman script transliteration using ITRANS scheme

## Setup

### Prerequisites

- Python 3.12 or higher
- `uv` package manager

### Installation

1. Clone the repository
2. The project is already initialized with `uv`. Dependencies are managed automatically.

## Usage

### Basic Usage

```python
from utility.translator import english_to_hinglish

# Translate English to Hinglish
result = english_to_hinglish("hello how are you")
print(result)  # Output: namaste aap kaise hain

result = english_to_hinglish("what are you doing")
print(result)  # Output: aap kya kar rahe hain
```

### Run the Main Script

```bash
uv run python main.py
```

### Run Tests

```bash
# Translation tests
uv run python tests/test_translator.py

# File splitter tests
python tests/test_file_splitter.py

# API tests
uv run python tests/test_api_endpoint.py
```

### Run the API Server

```bash
# Start the FastAPI server
uv run uvicorn api.app:app --host 127.0.0.1 --port 8000

# Or with auto-reload for development
uv run uvicorn api.app:app --reload --host 127.0.0.1 --port 8000
```

Then access:
- **Swagger UI (Interactive API Docs):** http://localhost:8000/docs
- **API Health Check:** http://localhost:8000/health
- **ReDoc:** http://localhost:8000/redoc

### Test the API

```bash
# Run the API test suite
uv run python tests/test_api_endpoint.py

# Simple API test
python tests/test_api_simple.py
```

## File Processing Tools

### File Splitter Utility

Split large text files into smaller chunks for easier processing:

```bash
# Basic usage - split any file
python utility/generic_file_splitter.py "path/to/your/file.txt"

# Custom chunk size and output location
python utility/generic_file_splitter.py "C:/complete/path/file.txt" --chunk-size 1500 --folder-name "my_output"

# Works with both absolute and relative paths
python utility/generic_file_splitter.py "story/input/story.txt" --output-dir "story/output"
```

### File Translator

Translate entire text files to Hinglish:

```bash
# Translate a complete file
python utility/file_translator.py

# Process files in batch
python utility/demo_file_translator.py
```

### Programmatic Usage

```python
# Split any file from Python code
from utility.generic_file_splitter import split_any_file

result = split_any_file("C:/path/to/large_file.txt", max_chars_per_file=2000)
if result["success"]:
    print(f"Created {result['files_created']} files in {result['output_folder']}")

# Translate text files
from utility.translator import english_to_hinglish

text = "Your English text here"
hinglish_result = english_to_hinglish(text)
```

## API Endpoints

The API provides the following endpoints:

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Translation
- `POST /translate` - Translate text (JSON body)
  ```json
  {
    "text": "hello how are you"
  }
  ```

For complete API documentation, see [api/README.md](api/README.md)

## SSL Certificate Issues

If you encounter SSL certificate verification errors (common in corporate networks), you have a few options:

### Option 1: Install Certificates (Recommended for Production)

```bash
# Windows - Install certificates from your organization
# Contact your IT department for the certificate bundle
```

### Option 2: Set Environment Variable (Quick Fix)

```bash
# Windows PowerShell
$env:PYTHONHTTPSVERIFY = "0"
uv run python main.py

# Or permanently set in Windows
[System.Environment]::SetEnvironmentVariable('PYTHONHTTPSVERIFY', '0', 'User')
```

### Option 3: Use Certifi

```bash
# Install certifi and update certificates
uv add certifi
```

## Examples

| English Input | Hinglish Output |
|--------------|----------------|
| hello how are you | namaste aap kaise hain |
| what are you doing | aap kya kar rahe hain |
| good morning | shubh prabhaat |
| thank you | dhanyavaad |
| I love you | main tumse pyaar karata hoon |

## Project Structure

```
english-to-hindi-roman/
├── README.md                           # This file
├── pyproject.toml                      # Project dependencies
├── api/                                # REST API
│   ├── app.py                          # FastAPI application
│   ├── models.py                       # Pydantic models
│   └── README.md                       # API documentation
├── utility/                            # Core utilities
│   ├── translator.py                   # Main translation logic
│   ├── file_translator.py              # File translation utility
│   ├── file_splitter.py                # File splitting utility
│   ├── generic_file_splitter.py        # Universal file splitter
│   ├── demo_file_splitter.py           # File splitter demo
│   ├── demo_generic_splitter.py        # Generic splitter demo
│   ├── demo_transliteration.py         # Transliteration demo
│   ├── fix_ssl.py                      # SSL troubleshooting
│   ├── inputfile/                      # Sample input files
│   └── outputfile/                     # Sample output files
├── tests/                              # Test suite
│   ├── test_translator.py              # Translation tests
│   ├── test_file_splitter.py           # File splitter tests
│   ├── test_api_endpoint.py            # API endpoint tests
│   ├── test_api_simple.py              # Simple API tests
│   └── split_story_31_10.py            # Story splitting example
├── story/                              # Story processing workspace
│   ├── input/                          # Input story files
│   ├── output/                         # Processed story chunks
│   └── story1/                         # Sample processed stories
├── docs/                               # Documentation
│   ├── API_README.md                   # API documentation
│   ├── FILE_SPLITTER.md                # File splitter guide
│   ├── GENERIC_FILE_SPLITTER.md        # Generic splitter guide
│   ├── FILE_TRANSLATOR.md              # File translator guide
│   ├── SSL_TROUBLESHOOTING.md          # SSL configuration
│   ├── QUICKSTART.md                   # Quick start guide
│   └── VALIDATION_REPORT.md            # Validation results
└── ui/                                 # User interface (future)
```

## How It Works

### Translation Pipeline

1. **Text Input**: Accept English text (string or file)
2. **Translation**: Convert English to Hindi (Devanagari) using Google Translate via `deep-translator`
3. **Transliteration**: Transform Hindi script to Roman script using `indic-transliteration` with ITRANS scheme
4. **Output**: Return natural-sounding Hinglish text in Roman script

### File Processing Pipeline

1. **File Input**: Accept any text file (absolute or relative path)
2. **Smart Splitting**: Break large files into manageable chunks at sentence boundaries
3. **Organization**: Create structured output folders with numbered files
4. **Batch Processing**: Process multiple files or chunks in sequence
5. **Translation Integration**: Optionally translate processed chunks to Hinglish

### Key Components

- **Core Translator** (`utility/translator.py`): Main translation logic
- **File Splitter** (`utility/file_splitter.py`): Split files into chunks
- **Generic Splitter** (`utility/generic_file_splitter.py`): Universal file processing
- **File Translator** (`utility/file_translator.py`): Translate entire files
- **REST API** (`api/app.py`): Web service interface

## Testing

### Translation Tests
- Basic translation functionality
- Various input scenarios (greetings, sentences, phrases)
- Special cases and edge conditions
- Empty input and error handling

### File Processing Tests
- File splitting with different chunk sizes
- Path resolution (absolute/relative paths)
- Auto-detection of output directories
- Error handling for missing files
- Large file processing (up to 300k characters)

### API Tests
- Endpoint functionality
- Request/response validation
- Error handling and status codes
- Health check monitoring

### Run All Tests
```bash
# Core translation
python tests/test_translator.py

# File processing
python tests/test_file_splitter.py

# API functionality  
python tests/test_api_endpoint.py

# Demo all features
python utility/demo_generic_splitter.py
```

## Quick Start Examples

### Translate Simple Text
```python
from utility.translator import english_to_hinglish
result = english_to_hinglish("Hello, how are you?")
print(result)  # namaste, aap kaise hain?
```

### Split Large File
```bash
python utility/generic_file_splitter.py "story/input/large_story.txt"
```

### Process Files Programmatically
```python
from utility.generic_file_splitter import split_any_file
result = split_any_file("/path/to/file.txt", max_chars_per_file=2000)
```

### Use REST API
```bash
curl -X POST "http://localhost:8000/translate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Good morning"}'
```

## Documentation

- **[API Guide](docs/API_README.md)** - Complete API documentation
- **[File Splitter Guide](docs/FILE_SPLITTER.md)** - File splitting utility
- **[Generic Splitter Guide](docs/GENERIC_FILE_SPLITTER.md)** - Universal file processor
- **[File Translator Guide](docs/FILE_TRANSLATOR.md)** - File translation utility
- **[SSL Troubleshooting](docs/SSL_TROUBLESHOOTING.md)** - SSL configuration help
- **[Quick Start](docs/QUICKSTART.md)** - Get started quickly

## Use Cases

- **Content Translation**: Convert English articles/stories to Hinglish
- **Large File Processing**: Split books/documents for batch translation
- **API Integration**: Embed translation in web applications
- **Batch Processing**: Process multiple files automatically
- **Educational Tools**: Learn Hinglish transliteration patterns
- **Content Management**: Prepare text for multilingual applications

## Notes

- Translation quality depends on Google Translate's accuracy
- Transliteration follows ITRANS scheme for consistency
- File splitter handles up to 300,000 characters per file
- Smart text splitting preserves sentence boundaries
- SSL certificate configuration may be needed in corporate networks
- Internet connection required for translation (Google Translate API)
- Cross-platform compatibility (Windows, macOS, Linux)