# SSL Certificate Troubleshooting Guide

## Problem
You're experiencing SSL certificate verification errors when trying to use Google Translate API through the `deep-translator` library. This is common in corporate networks.

## Quick Solutions

### Solution 1: Use a Different Network
Try running the code on a different network (like your home WiFi or mobile hotspot) where SSL certificates aren't intercepted by corporate proxies.

### Solution 2: Install Corporate Certificates
Contact your IT department and request the corporate SSL certificate bundle. Then:

```powershell
# Set environment variable to point to your corporate cert bundle
$env:REQUESTS_CA_BUNDLE = "C:\path\to\your\corporate-certs.pem"
$env:SSL_CERT_FILE = "C:\path\to\your\corporate-certs.pem"
```

### Solution 3: Use Alternative Translation Service
Instead of Google Translate, use other translators available in `deep-translator`:

```python
from deep_translator import MicrosoftTranslator, MyMemoryTranslator

# Try Microsoft Translator
translator = MicrosoftTranslator(source='en', target='hi')

# Or MyMemory (no API key needed, but limited)
translator = MyMemoryTranslator(source='en', target='hi')
```

### Solution 4: Use Offline/Local Model
For production use, consider using a local translation model:

```bash
uv add transformers torch
```

Then use a model like `facebook/mbart-large-50-many-to-many-mmt` or similar for offline translation.

### Solution 5: Use API with Authentication
Use an official API service with proper authentication:

- Google Cloud Translation API (requires API key)
- Azure Translator (requires API key)
- DeepL API (requires API key)

## Testing Transliteration Only

Since the transliteration works perfectly (it's offline), you can test with pre-translated Hindi text:

```python
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# If you have Hindi text from another source
hindi_text = "नमस्ते"
hinglish = transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)
print(hinglish)  # Output: namaste
```

## Verification

Run `demo_transliteration.py` to verify the transliteration library works:

```bash
uv run python demo_transliteration.py
```

This should work without any SSL errors since it's completely offline.

## For Development/Testing

If you're just testing and don't need production-grade security:

```python
import urllib3
urllib3.disable_warnings()
```

But **NEVER** use this in production!
