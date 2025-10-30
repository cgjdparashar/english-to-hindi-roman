"""
SSL Certificate Fix Helper Script

This script helps diagnose and fix SSL certificate issues for the translator.
Run this before using the main translation function.
"""

import ssl
import certifi
import os

print("SSL Certificate Configuration Helper")
print("=" * 60)

# Show current certificate location
print(f"\n1. Current certifi bundle location:")
print(f"   {certifi.where()}")

# Show SSL default context
print(f"\n2. Current SSL context configuration:")
context = ssl.create_default_context()
print(f"   Check hostname: {context.check_hostname}")
print(f"   Verify mode: {context.verify_mode}")

# Option 1: Use certifi bundle
print(f"\n3. Setting environment variable to use certifi:")
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
print(f"   SSL_CERT_FILE = {os.environ.get('SSL_CERT_FILE')}")
print(f"   REQUESTS_CA_BUNDLE = {os.environ.get('REQUESTS_CA_BUNDLE')}")

# Test if we can import and use deep-translator
print(f"\n4. Testing deep-translator import:")
try:
    from deep_translator import GoogleTranslator
    print(f"   ✓ Successfully imported GoogleTranslator")
    
    # Try a simple translation
    print(f"\n5. Testing translation (this may fail due to SSL):")
    translator = GoogleTranslator(source='en', target='hi')
    try:
        result = translator.translate("hello")
        print(f"   ✓ Translation successful!")
        print(f"   'hello' -> '{result}'")
        
        # Test transliteration
        from indic_transliteration import sanscript
        from indic_transliteration.sanscript import transliterate
        
        hinglish = transliterate(result, sanscript.DEVANAGARI, sanscript.ITRANS)
        print(f"   Hinglish: '{hinglish}'")
        
    except Exception as e:
        print(f"   ✗ Translation failed: {str(e)[:100]}...")
        print(f"\n   SOLUTION: Run this command in PowerShell:")
        print(f"   $env:REQUESTS_CA_BUNDLE = '{certifi.where()}'")
        print(f"   $env:SSL_CERT_FILE = '{certifi.where()}'")
        print(f"\n   Then run your script again.")
        
except ImportError as e:
    print(f"   ✗ Import failed: {e}")

print("\n" + "=" * 60)
print("\nQuick Fix Commands (PowerShell):")
print("-" * 60)
print(f"$env:SSL_CERT_FILE = '{certifi.where()}'")
print(f"$env:REQUESTS_CA_BUNDLE = '{certifi.where()}'")
print(f"$env:CURL_CA_BUNDLE = '{certifi.where()}'")
print("\nThen run: uv run python main.py")
