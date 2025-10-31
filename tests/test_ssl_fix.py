"""
Direct test of translation function with SSL fix
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Force reload of utility module
if 'utility.translator' in sys.modules:
    del sys.modules['utility.translator']

from utility.translator import english_to_hinglish

print("Testing English to Hinglish translation...")
print("="*60)

test_cases = [
    "hello",
    "hello how are you",
    "what are you doing"
]

for text in test_cases:
    print(f"\nInput:  '{text}'")
    result = english_to_hinglish(text)
    print(f"Output: '{result}'")
    
    if result and not result.startswith("Translation error"):
        print("✅ SUCCESS - Translation working!")
    else:
        print("❌ FAILED - SSL issue persists")

print("\n" + "="*60)
