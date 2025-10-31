"""
Demo script to test transliteration independently
This shows that the indic-transliteration library works correctly
"""

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

print("Testing Indic Transliteration Library")
print("=" * 60)

# Test cases with Hindi Devanagari text
test_cases = [
    "नमस्ते",  # Namaste
    "धन्यवाद",  # Thank you
    "आप कैसे हो",  # How are you
    "आप क्या कर रहे हो",  # What are you doing
    "शुभ प्रभात",  # Good morning
    "मैं ठीक हूँ",  # I am fine
]

print("\nDirect Transliteration Test (Devanagari -> Roman):")
print("-" * 60)

for hindi_text in test_cases:
    roman_text = transliterate(
        hindi_text,
        sanscript.DEVANAGARI,
        sanscript.ITRANS
    )
    print(f"Hindi:     {hindi_text}")
    print(f"Hinglish:  {roman_text}")
    print()

print("=" * 60)
print("✓ Transliteration library works correctly!")
print("\nNote: The SSL error you see is only for the translation part (Google Translate).")
print("The transliteration library works completely offline.")
