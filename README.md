# English to Hinglish (Hindi-Roman) Translator

A Python application that converts English text to Hinglish (Hindi in Roman script) using open-source libraries.

## Features

- Translates any English text to Hindi using `deep-translator`
- Transliterates Hindi (Devanagari) to Roman script (Hinglish) using `indic-transliteration`
- No hardcoded translations - fully dynamic translation
- Comprehensive test suite

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
from main import english_to_hinglish

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
uv run python tests/test_translator.py
```

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
├── main.py                 # Main translation module
├── tests/
│   └── test_translator.py  # Test suite
├── pyproject.toml          # Project dependencies
├── .python-version         # Python version specification
└── README.md              # This file
```

## How It Works

1. **Translation**: The `english_to_hinglish()` function first translates English text to Hindi (Devanagari script) using Google Translate via the `deep-translator` library.

2. **Transliteration**: The Hindi text is then transliterated from Devanagari to Roman script using the `indic-transliteration` library with the ITRANS scheme, which is commonly used for Hinglish.

3. **Output**: The result is natural-sounding Hinglish text in Roman script.

## Testing

The test suite includes:
- Basic translation tests
- Various input scenarios  
- Special cases (greetings, common words)
- Empty input handling
- Edge cases

## Notes

- The quality of translation depends on Google Translate's accuracy
- The transliteration follows the ITRANS scheme for consistency
- For production use, ensure proper SSL certificate configuration
- The application requires internet connection for translation (uses Google Translate API)